import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from std_msgs.msg import String
from cv_bridge import CvBridge
import json
from ultralytics import YOLO
import os

class PoseDetectorNode(Node):
    def __init__(self):
        super().__init__('pose_detector_node')
        self.get_logger().info('PoseDetectorNode started')
        
        # Load fine-tuned dog pose model
        model_path = os.path.expanduser('~/PoseReactive_PetBot/best.pt')
        self.model = YOLO(model_path)
        self.bridge = CvBridge()
        
        self.subscription = self.create_subscription(
            Image,
            '/oakd/rgb/preview/image_raw',
            self.image_callback,
            10)
        
        self.publisher = self.create_publisher(String, '/pet_keypoints', 10)
        self.get_logger().info('Subscribed to camera topic, using dog pose model')

    def image_callback(self, msg):
        frame = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
        results = self.model(frame, verbose=False)
        
        output_data = {
            'keypoints': [],
            'box_height': None,
            'box_width': None
        }
        
        for result in results:
            if result.keypoints is not None and len(result.boxes) > 0:
                kps = result.keypoints.data.cpu().numpy()  # [N, 24, 3] (x, y, conf)
                boxes = result.boxes.xyxy.cpu().numpy()  # [N, 4]
                
                if len(kps) > 0:
                    output_data['keypoints'] = kps[0].tolist()
                    box = boxes[0]
                    output_data['box_height'] = float(box[3] - box[1])
                    output_data['box_width'] = float(box[2] - box[0])
        
        msg_out = String()
        msg_out.data = json.dumps(output_data)
        self.publisher.publish(msg_out)

def main(args=None):
    rclpy.init(args=args)
    node = PoseDetectorNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()