import time
import serial
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from serial_motor_msgs.msg import EncoderTicks


class MotorSerialNode(Node):
    def __init__(self):
        super().__init__('motor_serial_node')

        # Parameters
        self.declare_parameter('serial_port', '/dev/ttyUSB0')
        self.declare_parameter('baudrate', 115200)
        self.declare_parameter('serial_read_rate', 100.0)

        serial_port = self.get_parameter('serial_port').value
        baudrate = self.get_parameter('baudrate').value
        serial_read_rate = self.get_parameter('serial_rate_rate', 100).value

        # Open serial connection
        try:
            self.ser = serial.Serial(
                port=serial_port,
                baudrate=baudrate,
                timeout=0.0
            )

            time.sleep(2.0)
            self.ser.reset_input_buffer()
            self.ser.reset_output_buffer()

            self.get_logger().info(f'Opened serial port {serial_port} at {baudrate} baud')
        except serial.SerialException as e:
            self.get_logger().error(f'Failed to open serial port {serial_port}: {e}')
            raise

        # Subscribe to cmd_vel
        self.cmd_vel_sub = self.create_subscription(
            Twist,
            '/cmd_vel',
            self.cmd_vel_callback,
            10
        )

        # Time to poll serial for encoder messages
        self.serial_timer = self.create_timer(
            1.0 / serial_read_rate,
            self.read_serial_line
        )

    def cmd_vel_callback(self, msg: Twist) -> None:
        linear_velocity = msg.linear.x
        angular_velocity = msg.angular.z

        command = f'CMD,{linear_velocity:.4f},{angular_velocity:.4f}\n'

        try:
            self.ser.write(command.encode('utf-8'))
            self.get_logger().debug(f'Sent: {command.strip()}')
        except serial.SerialException as e:
            self.get_logger().error(f'Failed to write to serial: {e}')

    def read_serial_line(self) -> None:
        try:
            if self.ser.in_waiting <= 0:
                return
            
            raw_line = self.ser.readline()
            if not raw_line:
                return
            
            line = raw_line.decode('utf-8', errors='replace').strip()
            if not line:
                return
            
            # Ignore boot/debug lines that are not encoder packets
            if not line.startswith('ENC,'):
                self.get_logger().debug(f'Ignored serial line: {line}')
                return
            
            parts = line.split(',')
            if len(parts) != 4:
                self.get_logger().warn(f'Malformed encoder line: {line}')
                return
            
            prefix, left_str, right_str, arduino_ms = parts

            if prefix != 'ENC':
                self.get_logger().warn(f'Bad prefix in line: {line}')
                return
            
            left_ticks = int(left_str)
            right_ticks = int(right_str)
            arduino_ms = int(arduino_ms)

            msg = EncoderTicks()
            msg.left_ticks = left_ticks
            msg.right_ticks = right_ticks
            msg.arduino_ms = arduino_ms

            self.encoder_pub.publish(msg)
            self.get_logger().debug(
                f'Published encoder ticks: L={left_ticks}, R={right_ticks}, arduino_ms={arduino_ms}'
            )
        
        except ValueError:
            self.get_logger().warn(f'Failed to parse encoder integers from line: {line}')
        
        except serial.SerialException as e:
            self.get_logger().error(f'Serial read error: {e}')

        except Exception as e:
            self.get_logger().error(f'Unexpected error while reading serial: {e}')
            

    def destroy_node(self):
        if hasattr(self, 'ser') and self.ser.is_open:
            self.ser.close()
            self.get_logger().info('Closed serial port')
        super().destroy_node()


def main(args=None):
    rclpy.init(args=args)
    node = None

    try:
        node = MotorSerialNode()
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        if node is not None:
            node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()