#include "rclcpp/rclcpp.hpp"
#include "example_interfaces/msg/int64.hpp"
#include <cstdint>


using namespace std::chrono_literals;

class number_publisher : public rclcpp::Node
{
    public:
    number_publisher():Node("number_publisher") 
    {
        publisher_ = this-> create_publisher<example_interfaces::msg::Int64>("/number" ,10);
        timer_ = this->create_wall_timer(1.0s,std::bind(&number_publisher::publishNews ,this));
        RCLCPP_INFO(this->get_logger(), "number_publisher been started");
    }
    private:


        void publishNews(){
            auto msg = example_interfaces::msg::Int64();
            msg.data = counter;
            publisher_->publish(msg);
        }

        rclcpp::Publisher<example_interfaces::msg::Int64>::SharedPtr publisher_;
        rclcpp::TimerBase::SharedPtr timer_;
        std::int64_t counter = 2;


};

int main (int argc , char **argv)
{
    rclcpp::init(argc ,argv);
    auto node =  std::make_shared<number_publisher>();
    rclcpp::spin(node);
    rclcpp::shutdown();
    return 0;
}