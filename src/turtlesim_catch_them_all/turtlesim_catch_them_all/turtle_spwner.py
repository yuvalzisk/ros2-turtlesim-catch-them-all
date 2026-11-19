#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from turtlesim.srv import Spawn
from functools import partial
from turtlesim.srv import Kill
import random
import math
from my_robot_interfaces.msg import Turtle
from my_robot_interfaces.msg import TurtleArray
from my_robot_interfaces.srv import CatchTurtle


class TurtleSpwnerNode(Node):  
    def __init__(self):
        super().__init__("TurtleSpwner")  
        self.declare_parameter("turtle_name_prefix" , "turtle")
        self.declare_parameter("spwan_freq" , 1.0)
        self.spwan_frequency = self.get_parameter("spwan_freq").value
        self.alive_turtels = []
        self.alive_turtels_publisher = self.create_publisher(TurtleArray , "alive_turtle" , 10)
        self.spawn_client = self.create_client(Spawn , "/spawn")
        self.catch_turtle_service = self.create_service(CatchTurtle , "catch_turtle" , self.callback_catch_turtle)
        self.spawn_turtle_timer = self.create_timer(1.0/self.spwan_frequency,self.spawn_new_turtle)
        self.kill_client = self.create_client(Kill , "/kill")
        self.turtle_name_counter = 0
        self.turtle_name_prefix = self.get_parameter("turtle_name_prefix").value


    def callback_catch_turtle(self , req:CatchTurtle.Request , res:CatchTurtle.Response):
        self.call_kill_service(req.name)
        res.success = True
        return res


    def publish_alive_turtle(self):
        msg = TurtleArray()
        msg.turtles = self.alive_turtels
        self.alive_turtels_publisher.publish(msg)


    def spawn_new_turtle(self):
        self.turtle_name_counter+=1
        name = self.turtle_name_prefix + str(self.turtle_name_counter)
        x = random.uniform(0.0 ,11.0)
        y = random.uniform(0.0 ,11.0)
        theta = random.uniform(0.0 , 2*math.pi)
        self.call_spawn_service(name,x,y,theta)





    def call_spawn_service(self , turtle_name , x , y , theta):
        while not self.spawn_client.wait_for_service(1.0):
            self.get_logger().warn("Waiting for spwan service")

        req = Spawn.Request()
        req.x = x
        req.y = y
        req.name = turtle_name
        req.theta =theta

        future = self.spawn_client.call_async(req)
        future.add_done_callback(partial(self.callback_call_spwan_service,request = req ))


    def callback_call_spwan_service(self , future , request: Spawn.Request):
        response: Spawn.Response = future.result()
        if response.name != "":
            self.get_logger().info("New alive turtle: " + response.name )
            new_turtle = Turtle()
            new_turtle.name = response.name
            new_turtle.x = request.x
            new_turtle.y = request.y
            new_turtle.theta = request.theta
            self.alive_turtels.append(new_turtle)
            self.publish_alive_turtle()


    def call_kill_service(self, turtle_name):
        while not self.kill_client.wait_for_service(1.0):
                    self.get_logger().warn("Waiting for kill service")

        req = Kill.Request()
        req.name = turtle_name

        future = self.kill_client.call_async(req)
        future.add_done_callback(partial(self.callback_call_kill_service , turtle_name = turtle_name))


    def callback_call_kill_service(self , future , turtle_name):
         for(i , turtle) in enumerate(self.alive_turtels):
              if turtle.name == turtle_name:
                   del self.alive_turtels[i]
                   self.publish_alive_turtle()
                   break
            


def main(args=None):
    rclpy.init(args=args)
    node = TurtleSpwnerNode()  
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == "__main__":
    main()