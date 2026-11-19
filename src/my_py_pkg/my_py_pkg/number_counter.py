#!/usr/bin/env python3 
import rclpy
from rclpy.node import Node
from example_interfaces.msg import Int64
from example_interfaces.srv import SetBool   

class number_counter(Node):
    def __init__(self):

        super().__init__("number_counter")
        self.subscriber_ = self.create_subscription(Int64,"/number",self.callback_number_,10)
        self.counter = 0
        self.publisher_ = self.create_publisher(Int64,"/number_count",10)
        self.reset_counter_service = self.create_service(SetBool ,"reset_counter" ,self.callback_reset_counter)
        self.get_logger().info("number_counter ......")


    def callback_number_(self, msg:Int64):
         self.counter+=msg.data
         new_msg = Int64()
         new_msg.data = self.counter
         self.publisher_.publish(new_msg)

    def callback_reset_counter(self , request:SetBool.Request , response:SetBool.Response):
        if request.data:
            self.counter = 0
            response.success = True
            response.message = "ok i reset"
        else:
            response.success = False
            response.message = "same same"

        return response


def main(args=None):
    rclpy.init(args=args)
    node = number_counter()
    rclpy.spin(node)
    rclpy.shutdown()



if __name__ == "__main__":
    main()