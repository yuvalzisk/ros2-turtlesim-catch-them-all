#include "rclcpp/rclcpp.hpp"
#include "my_robot_interfaces/msg/hardware_status.hpp"

using namespace std::chrono_literals;

class HardwareStatusPublisherNode : public rclcpp::Node
{
public:
    HardwareStatusPublisherNode() : Node("HardwareStatusPublisher")
    {
        pub_ = this->create_publisher<my_robot_interfaces::msg::HardwareStatus>("hardwarestatus" ,10);
        timer_ = this->create_wall_timer(1s,std::bind(&HardwareStatusPublisherNode::publishhardwarestatus ,this ));
        RCLCPP_INFO(this->get_logger() , "hardware status publisher has been statred");
        


    }

private:
    void publishhardwarestatus()
    {
        auto msg = my_robot_interfaces::msg::HardwareStatus();
        msg.are_motors_ready = false;
        msg.debug_message = "motors are too hot ";
        msg.temp = 46.7;
        pub_->publish(msg);
    }
    rclcpp::TimerBase::SharedPtr timer_;
    rclcpp::Publisher<my_robot_interfaces::msg::HardwareStatus>::SharedPtr pub_;    
};



int main(int argc , char **argv){
    rclcpp::init(argc,argv);
    auto node = std::make_shared<HardwareStatusPublisherNode>();
    rclcpp::spin(node);
    rclcpp::shutdown();
    return 0;
}
