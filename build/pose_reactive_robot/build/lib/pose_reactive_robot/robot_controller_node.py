import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from geometry_msgs.msg import Twist

class RobotControllerNode(Node):
    def __init__(self):
        super().__init__('robot_controller_node')
        self.get_logger().info('RobotControllerNode started')

        self.subscription = self.create_subscription(
            String,
            '/pet_state',
            self.state_callback,
            10)

        self.cmd_pub = self.create_publisher(Twist, '/cmd_vel', 10)
        self.fsm_state = 'Sleep'
        self.get_logger().info('FSM initial state: Sleep')

        # Publish continuously at fixed rate so the controller doesn't time out
        self.timer = self.create_timer(0.05, self.execute_fsm)  # 20 Hz

    def state_callback(self, msg):
        if self.fsm_state != msg.data:
            self.get_logger().info(f'FSM state: {msg.data}')
        self.fsm_state = msg.data

    def execute_fsm(self):
        twist = Twist()

        if self.fsm_state == 'Approach':
            twist.linear.x = 0.3
            twist.angular.z = 0.0
        elif self.fsm_state == 'Follow':
            twist.linear.x = 0.35
            twist.angular.z = 0.0
        elif self.fsm_state == 'Retreat':
            twist.linear.x = -0.45
            twist.angular.z = 0.0
        elif self.fsm_state == 'Sleep':
            twist.linear.x = 0.0
            twist.angular.z = 0.0

        self.cmd_pub.publish(twist)

def main(args=None):
    rclpy.init(args=args)
    node = RobotControllerNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()