import math
from typing import Optional

import rclpy
from rclpy.node import Node

from sensor_msgs.msg import JointState
from serial_motor_msgs.msg import EncoderTicks


class WheelJointStateNode(Node):
    def __init__(self) -> None:
        super().__init__('wheel_joint_state_node')

        self.declare_parameter('ticks_per_revolution', 537.6)
        self.declare_parameter('encoder_topic', '/encoder_ticks')
        self.declare_parameter('joint_states_topic', '/joint_states')
        self.declare_parameter(
            'left_joint_names',
            ['front_left_wheel_joint', 'back_left_wheel_joint']
        )
        self.declare_parameter(
            'right_joint_names',
            ['front_right_wheel_joint', 'back_right_wheel_joint']
        )

        self.ticks_per_revolution = float(
            self.get_parameter('ticks_per_revolution').value
        )
        self.encoder_topic = str(self.get_parameter('encoder_topic').value)
        self.joint_states_topic = str(self.get_parameter('joint_states_topic').value)
        self.left_joint_names = list(self.get_parameter('left_joint_names').value)
        self.right_joint_names = list(self.get_parameter('right_joint_names').value)

        if self.ticks_per_revolution <= 0.0:
            raise ValueError('ticks_per_revolution must be positive')

        self.left_wheel_position = 0.0
        self.right_wheel_position = 0.0
        self.prev_left_ticks: Optional[int] = None
        self.prev_right_ticks: Optional[int] = None

        self.joint_state_pub = self.create_publisher(
            JointState,
            self.joint_states_topic,
            10,
        )
        self.encoder_sub = self.create_subscription(
            EncoderTicks,
            self.encoder_topic,
            self.encoder_callback,
            10,
        )

        self.get_logger().info('Wheel joint state node started')

    def encoder_callback(self, msg: EncoderTicks) -> None:
        left_ticks = int(msg.left_ticks)
        right_ticks = int(msg.right_ticks)

        if self.prev_left_ticks is None:
            self.prev_left_ticks = left_ticks
            self.prev_right_ticks = right_ticks
            self.publish_joint_state()
            return

        delta_left_ticks = left_ticks - self.prev_left_ticks
        delta_right_ticks = right_ticks - self.prev_right_ticks

        self.prev_left_ticks = left_ticks
        self.prev_right_ticks = right_ticks

        radians_per_tick = (2.0 * math.pi) / self.ticks_per_revolution
        self.left_wheel_position += delta_left_ticks * radians_per_tick
        self.right_wheel_position += delta_right_ticks * radians_per_tick

        self.publish_joint_state()

    def publish_joint_state(self) -> None:
        msg = JointState()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.name = self.left_joint_names + self.right_joint_names
        msg.position = [
            self.left_wheel_position,
            self.left_wheel_position,
            self.right_wheel_position,
            self.right_wheel_position,
        ]
        msg.velocity = []
        msg.effort = []

        self.joint_state_pub.publish(msg)


def main(args=None) -> None:
    rclpy.init(args=args)
    node = None

    try:
        node = WheelJointStateNode()
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        if node is not None:
            node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()