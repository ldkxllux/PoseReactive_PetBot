import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2
import sys
import os
from ultralytics import YOLO

class VideoPublisherNode(Node):
    def __init__(self, video_path):
        super().__init__('video_publisher_node')
        self.publisher = self.create_publisher(Image, '/oakd/rgb/preview/image_raw', 10)
        self.bridge = CvBridge()
        self.cap = cv2.VideoCapture(video_path)

        if not self.cap.isOpened():
            self.get_logger().error(f'Cannot open video: {video_path}')
            return

        model_path = os.path.expanduser('~/PoseReactive_PetBot/best.pt')
        self.display_model = YOLO(model_path)

        fps = self.cap.get(cv2.CAP_PROP_FPS)
        timer_period = 1.0 / fps if fps > 0 else 0.033

        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.get_logger().info(f'Publishing video: {video_path} at {fps} FPS')
        self.get_logger().info('Displaying skeleton-annotated preview window')

    def timer_callback(self):
        ret, frame = self.cap.read()
        if not ret:
            # Loop video
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            ret, frame = self.cap.read()

        if ret:
            msg = self.bridge.cv2_to_imgmsg(frame, encoding='bgr8')
            self.publisher.publish(msg)
            results = self.display_model(frame, verbose=False)
            annotated = results[0].plot()
            h, w = annotated.shape[:2]
            target_w = 400
            target_h = int(h * (target_w / w))
            display_frame = cv2.resize(annotated, (target_w, target_h))
            cv2.namedWindow('Dog Pose Recognition', cv2.WINDOW_NORMAL)
            cv2.resizeWindow('Dog Pose Recognition', target_w, target_h)
            cv2.imshow('Dog Pose Recognition', display_frame)
            cv2.waitKey(1)

    def destroy_node(self):
        cv2.destroyAllWindows()
        super().destroy_node()

def main(args=None):
    rclpy.init(args=args)

    if len(sys.argv) < 2:
        print('Usage: video_publisher_node <video_path>')
        return

    video_path = sys.argv[1]
    node = VideoPublisherNode(video_path)
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()