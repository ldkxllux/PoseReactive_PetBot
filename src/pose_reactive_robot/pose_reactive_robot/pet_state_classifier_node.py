import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import json
import time
from collections import deque

class PetStateClassifierNode(Node):
    def __init__(self):
        super().__init__('pet_state_classifier_node')
        self.get_logger().info('PetStateClassifierNode started')

        self.subscription = self.create_subscription(
            String,
            '/pet_keypoints',
            self.keypoints_callback,
            10)

        self.publisher = self.create_publisher(String, '/pet_state', 10)

        self.box_height_history = deque(maxlen=15)
        self.smoothed_change_rate = 0.0
        self.smoothing_alpha = 0.3
        self.last_seen_time = time.time()
        self.last_state = 'Sleep'
        self.smoothed_face_score = 0.0
        self.smoothed_tail_score = 0.0
        self.last_facing_front = True

        # Face keypoints: nose, chin, left_eye, right_eye, left_ear_base, right_ear_base
        self.face_indices = [16, 17, 20, 21, 14, 15]
        # Tail keypoints: tail_start, tail_end
        self.tail_indices = [12, 13]

        # Movement threshold: above this absolute change rate, the dog is "moving"
        self.MOVEMENT_THRESHOLD = 0.025
        self.NO_DETECTION_TIMEOUT = 5.0

    def keypoints_callback(self, msg):
        data = json.loads(msg.data)
        keypoints = data.get('keypoints', [])
        box_height = data.get('box_height', None)

        current_time = time.time()

        if not keypoints or box_height is None:
            if current_time - self.last_seen_time > self.NO_DETECTION_TIMEOUT:
                state = 'Sleep'
            else:
                state = self.last_state
            self.publish_state(state)
            return

        self.last_seen_time = current_time

        # Reference height from ~0.8s ago for a stronger signal
        self.box_height_history.append((current_time, box_height))
        reference_height = None
        for t, h in self.box_height_history:
            if current_time - t >= 0.8:
                reference_height = h

        if reference_height is not None and reference_height > 0:
            raw_change_rate = (box_height - reference_height) / reference_height
        else:
            raw_change_rate = 0.0

        self.smoothed_change_rate = (
            self.smoothing_alpha * raw_change_rate
            + (1 - self.smoothing_alpha) * self.smoothed_change_rate
        )
        change_rate = self.smoothed_change_rate

        
        # Determine facing direction using smoothed average visibility scores
        face_scores = [keypoints[i][2] for i in self.face_indices if i < len(keypoints)]
        tail_scores = [keypoints[i][2] for i in self.tail_indices if i < len(keypoints)]
        raw_face_score = sum(face_scores) / len(face_scores) if face_scores else 0.0
        raw_tail_score = sum(tail_scores) / len(tail_scores) if tail_scores else 0.0

        self.smoothed_face_score = (
            self.smoothing_alpha * raw_face_score
            + (1 - self.smoothing_alpha) * self.smoothed_face_score
        )
        self.smoothed_tail_score = (
            self.smoothing_alpha * raw_tail_score
            + (1 - self.smoothing_alpha) * self.smoothed_tail_score
        )
        face_score = self.smoothed_face_score
        tail_score = self.smoothed_tail_score

        # Require a clear margin to avoid flickering between facing states
        FACING_MARGIN = 0.05
        if face_score > tail_score + FACING_MARGIN:
            facing_front = True
        elif tail_score > face_score + FACING_MARGIN:
            facing_front = False
        else:
            facing_front = self.last_facing_front  # keep previous decision if ambiguous
        self.last_facing_front = facing_front

        is_moving = abs(change_rate) > self.MOVEMENT_THRESHOLD

        # 4-state FSM:
        # facing front + still      -> Approach
        # facing front + moving     -> Retreat
        # facing away  + moving     -> Follow
        # facing away  + still      -> Sleep
        if facing_front and not is_moving:
            state = 'Approach'
        elif facing_front and is_moving:
            state = 'Retreat'
        elif not facing_front and is_moving:
            state = 'Follow'
        else:
            state = 'Sleep'

        self.get_logger().info(
            f'change_rate={change_rate:.4f}, facing_front={facing_front}, '
            f'face_score={face_score:.3f}, tail_score={tail_score:.3f}, state={state}'
        )
        self.publish_state(state)

    def publish_state(self, state):
        self.last_state = state
        msg_out = String()
        msg_out.data = state
        self.publisher.publish(msg_out)
        self.get_logger().info(f'Pet state: {state}')

def main(args=None):
    rclpy.init(args=args)
    node = PetStateClassifierNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()