import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from std_msgs.msg import Float32MultiArray
import json
import serial
from serial import SerialException

class arduinosender(Node):
    def __init__(self, port, baudrate):
        super().__init__(arduinosender)
        #self.publisher_=self.create_publisher(String, 'topic', 10)
        self.ser=serial.Serial(port=port, baudrate=baudrate, timeout=0.1)
        self.subscription = self.create_subscription(Float32MultiArray,'wheel_speeds', self.listener_callback, 10)

    def listener_callback(self, msg):
        data = {
            "left_speed": msg.data[0],
            "right_speed": msg.data[1]
        }
        try:
            self.send(data)
        except SerialException as e:
                print("ERROR ", e)
                

    def send(self, message, encodetype="ascii"):

        self.ser.reset_input_buffer()
        jsoned_data=json.dumps(message)
        
        self.ser.write((jsoned_data + "\n").encode(encodetype))

    def close(self):
        if self.ser.is_open:
            self.ser.close()
        


def main():
    rclpy.init()                                          # initialize ROS2
    bob = arduinosender(port="/dev/ttyUSB0", baudrate=9600)
    
    try:
        rclpy.spin(bob)                                   # keeps node alive, listening for messages
    except KeyboardInterrupt:
        pass
    finally:
        bob.close()
        rclpy.shutdown()
        
if __name__ == '__main__':
    main()