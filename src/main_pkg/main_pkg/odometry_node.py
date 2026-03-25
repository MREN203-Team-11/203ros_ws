import math
from typing import Optional

import rclpy
from rclpy.node import Node

from nav_msgs.msg import Odometry
from geometry_msgs.msg import TransformStamped, Quaternion
from tf2_ros import TransformBroadcaster

from serial_motor_msgs.msg import EncoderTicks


class OdometryNode(Node):
    def __init__(self) -> None:
        super().__init__('odometry_node')

        # Parameters
        self.declare_parameter('ticks_per_revolution', 537.6)
        self.declare_parameter('wheel_radius', 0.060325)      # meters
        self.declare_parameter('wheel_base', 0.238125)        # meters
        self.declare_parameter('odom_frame_id', 'odom')
        self.declare_parameter('base_frame_id', 'base_link')
        self.declare_parameter('encoder_topic', '/encoder_ticks')
        self.declare_parameter('odom_topic', '/odom')
        self.declare_parameter('publish_tf', True)

        self.ticks_per_revolution = float(
            self.get_parameter('ticks_per_revolution').value
        )
        self.wheel_radius = float(self.get_parameter('wheel_radius').value)
        self.wheel_base = float(self.get_parameter('wheel_base').value)
        self.odom_frame_id = str(self.get_parameter('odom_frame_id').value)
        self.base_frame_id = str(self.get_parameter('base_frame_id').value)
        self.encoder_topic = str(self.get_parameter('encoder_topic').value)
        self.odom_topic = str(self.get_parameter('odom_topic').value)
        self.publish_tf = bool(self.get_parameter('publish_tf').value)

        # State
        self.x = 0.0
        self.y = 0.0
        self.yaw = 0.0

        self.prev_left_ticks: Optional[int] = None
        self.prev_right_ticks: Optional[int] = None
        self.prev_arduino_ms: Optional[int] = None

        self.odom_pub = self.create_publisher(Odometry, self.odom_topic, 10)
        self.encoder_sub = self.create_subscription(
            EncoderTicks,
            self.encoder_topic,
            self.encoder_callback,
            10,
        )

        self.tf_broadcaster = TransformBroadcaster(self)

        self.get_logger().info('Odometry node started')

    def encoder_callback(self, msg: EncoderTicks) -> None:
        left_ticks = int(msg.left_ticks)
        right_ticks = int(msg.right_ticks)
        arduino_ms = int(msg.arduino_ms)

        # First message just initializes previous state
        if self.prev_left_ticks is None:
            self.prev_left_ticks = left_ticks
            self.prev_right_ticks = right_ticks
            self.prev_arduino_ms = arduino_ms
            return

        delta_left_ticks = left_ticks - self.prev_left_ticks
        delta_right_ticks = right_ticks - self.prev_right_ticks
        delta_ms = arduino_ms - self.prev_arduino_ms

        # Update previous state immediately
        self.prev_left_ticks = left_ticks
        self.prev_right_ticks = right_ticks
        self.prev_arduino_ms = arduino_ms

        # Protect against bad timing
        if delta_ms <= 0:
            self.get_logger().warn('Non-positive encoder dt; skipping update')
            return

        dt = delta_ms / 1000.0

        # Convert ticks to wheel travel
        meters_per_tick = (2.0 * math.pi * self.wheel_radius) / self.ticks_per_revolution
        d_left = delta_left_ticks * meters_per_tick
        d_right = delta_right_ticks * meters_per_tick

        # Diff-drive kinematics
        d_center = 0.5 * (d_left + d_right)
        d_yaw = (d_right - d_left) / self.wheel_base

        # Midpoint integration
        heading_mid = self.yaw + 0.5 * d_yaw
        self.x += d_center * math.cos(heading_mid)
        self.y += d_center * math.sin(heading_mid)
        self.yaw = self.normalize_angle(self.yaw + d_yaw)

        # Velocities
        linear_velocity = d_center / dt
        angular_velocity = d_yaw / dt

        now = self.get_clock().now().to_msg()

        # Publish odometry
        odom = Odometry()
        odom.header.stamp = now
        odom.header.frame_id = self.odom_frame_id
        odom.child_frame_id = self.base_frame_id

        odom.pose.pose.position.x = self.x
        odom.pose.pose.position.y = self.y
        odom.pose.pose.position.z = 0.0
        odom.pose.pose.orientation = self.yaw_to_quaternion(self.yaw)

        odom.twist.twist.linear.x = linear_velocity
        odom.twist.twist.angular.z = angular_velocity

        # Basic placeholder covariances
        odom.pose.covariance = [
            0.01, 0.0,  0.0,  0.0,  0.0,  0.0,
            0.0,  0.01, 0.0,  0.0,  0.0,  0.0,
            0.0,  0.0,  99999.0, 0.0,  0.0,  0.0,
            0.0,  0.0,  0.0,  99999.0, 0.0,  0.0,
            0.0,  0.0,  0.0,  0.0,  99999.0, 0.0,
            0.0,  0.0,  0.0,  0.0,  0.0,  0.03,
        ]
        odom.twist.covariance = [
            0.02, 0.0,  0.0,  0.0,  0.0,  0.0,
            0.0,  0.02, 0.0,  0.0,  0.0,  0.0,
            0.0,  0.0,  99999.0, 0.0,  0.0,  0.0,
            0.0,  0.0,  0.0,  99999.0, 0.0,  0.0,
            0.0,  0.0,  0.0,  0.0,  99999.0, 0.0,
            0.0,  0.0,  0.0,  0.0,  0.0,  0.05,
        ]

        self.odom_pub.publish(odom)

        if self.publish_tf:
            t = TransformStamped()
            t.header.stamp = now
            t.header.frame_id = self.odom_frame_id
            t.child_frame_id = self.base_frame_id
            t.transform.translation.x = self.x
            t.transform.translation.y = self.y
            t.transform.translation.z = 0.0
            t.transform.rotation = self.yaw_to_quaternion(self.yaw)
            self.tf_broadcaster.sendTransform(t)

    @staticmethod
    def yaw_to_quaternion(yaw: float) -> Quaternion:
        q = Quaternion()
        q.x = 0.0
        q.y = 0.0
        q.z = math.sin(yaw / 2.0)
        q.w = math.cos(yaw / 2.0)
        return q

    @staticmethod
    def normalize_angle(angle: float) -> float:
        return math.atan2(math.sin(angle), math.cos(angle))


def main(args=None) -> None:
    rclpy.init(args=args)
    node = OdometryNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()