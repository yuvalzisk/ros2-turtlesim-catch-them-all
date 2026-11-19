#!/usr/bin/env python3 
import rclpy
from rclpy.node import Node
from my_robot_interfaces.srv import SetLed

class BatteryNode(Node):
    def __init__(self):
        super().__init__("battery")
        self.battery_state = "full"
        self.last_time_battery_state_changed = self.get_curr_time_sec()
        self_battery_timer = self.create_timer(0.1 , self.check_battery_state)
        self.set_led_client = self.create_client(SetLed , "set_led")
        self.get_logger().info("battery nose has been started ......")




    def get_curr_time_sec(self):
        seconds , nanoseconds = self.get_clock().now().seconds_nanoseconds()
        return seconds + nanoseconds / 1000000000.0

    def check_battery_state(self):
        time_now = self.get_curr_time_sec()
        if self.battery_state == "full":
            if time_now - self.last_time_battery_state_changed > 4.0:
                self.battery_state = "empty"
                self.get_logger().info("need to chharge!!!")
                self.call_set_led(2,1)
                self.last_time_battery_state_changed = time_now
        elif self.battery_state == "empty":
            if time_now -self.last_time_battery_state_changed > 6.0:
                self.battery_state = "full"
                self.call_set_led(2,0)
                self.get_logger().info("battery us full now")
                self.last_time_battery_state_changed = time_now

    def call_set_led(self , led_number , state):
        while not self.set_led_client.wait_for_service(1.0):
            self.get_logger().warn("Waiting for set led service")
        request = SetLed.Request()
        request.led_number =led_number
        request.state = state

        future = self.set_led_client.call_async(request)
        future.add_done_callback(self.callback_call_set_led)


    def callback_call_set_led(self ,future):
        response : SetLed.Response = future.result()
        if response.success:
            self.get_logger().info("led_is_on")
        else:
            self.get_logger().info("led_is_off")



def main(args=None):
    rclpy.init(args=args)
    node = BatteryNode()
    rclpy.spin(node)
    rclpy.shutdown()



if __name__ == "__main__":
    main()