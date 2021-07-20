import cv2
import mediapipe as mp


class HandDetector:

    def __init__(
        self,
        static_image_mode: bool = False,
        max_num_hands: int = 2,
        min_detection_confidence: float = 0.5,
        min_tracking_confidence: float = 0.5
    ):
        self.static_image_mode = static_image_mode
        self.max_num_hands = max_num_hands
        self.min_detection_confidence = min_detection_confidence
        self.min_tracking_confidence = min_tracking_confidence

        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=self.static_image_mode,
            max_num_hands=self.max_num_hands,
            min_detection_confidence=self.min_detection_confidence,
            min_tracking_confidence=self.min_tracking_confidence
        )

        self.mp_draw = mp.solutions.drawing_utils
        self.DrawingSpec = self.mp_draw.DrawingSpec

    def find_hands(self, img, draw_hand=True):
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(img_rgb)
        if (self.results.multi_hand_landmarks):
            for hand_number, hand_landmark in enumerate(self.results.multi_hand_landmarks):
                if draw_hand:
                    self.draw_landmarks(
                        img,
                        hand_landmark,
                        self.mp_hands.HAND_CONNECTIONS
                    )

                    # for point in self.mp_hands.HandLandmark:
                    #     normalized_handmark = hand_landmark.landmark[point]
                    #     pixel_coordinates_landmark = self.mp_draw._normalized_to_pixel_coordinates(
                    #         normalized_handmark.x,
                    #         normalized_handmark.y,
                    #         w,
                    #         h
                    #     )

                    #     radius = abs(int(20*normalized_handmark.y)) + 1

                    #     cv2.circle(img, pixel_coordinates_landmark,
                    #                radius, (radius*4, radius*4, radius*4), -1)

        return img

    def draw_landmarks(self, img, landmarks, connections):
        h, w, _ = img.shape
        radius = 2
        color = (0,0,0)
        thickness = 5
        idx_to_coordinates = {}
        for idx, landmark in enumerate(landmarks.landmark):
            landmark_px = self.mp_draw._normalized_to_pixel_coordinates(landmark.x, landmark.y,
                                                           w, h)
            if landmark_px:
                idx_to_coordinates[idx] = landmark_px

        if connections:
            num_landmarks = len(landmarks.landmark)
            for connection in connections:
                start_idx = connection[0]
                end_idx = connection[1]
                if not (0 <= start_idx < num_landmarks and 0 <= end_idx < num_landmarks):
                    raise ValueError(f'Landmark index is out of range. Invalid connection '
                                    f'from landmark #{start_idx} to landmark #{end_idx}.')
                if start_idx in idx_to_coordinates and end_idx in idx_to_coordinates:
                    x_medio = (
                        idx_to_coordinates[start_idx][0] + idx_to_coordinates[end_idx][0])/2
                    y_medio = (
                        idx_to_coordinates[start_idx][1] + idx_to_coordinates[end_idx][1])/2
                    color = y_medio*255/h,0,x_medio*255/h
                    cv2.line(img, idx_to_coordinates[start_idx],
                            idx_to_coordinates[end_idx], color,
                            thickness)
            # Draws landmark points after finishing the connection lines, which is
            # aesthetically better.
            for landmark_px in idx_to_coordinates.values():
                color = landmark_px[1]*255/h,0,landmark_px[0]*255/h
                cv2.circle(img, landmark_px, radius,
                        color, thickness)


    def find_position(self, img):
        h, w, _ = img.shape

        resultado_landmarks = []

        try:
            for chosen_hand in self.results.multi_hand_landmarks:
                hand_landmark = {}
                for _id, landmark in enumerate(chosen_hand.landmark):
                    cx, cy = int(landmark.x * w), int(landmark.y * h)
                    hand_landmark[_id] = cx, cy
                resultado_landmarks.append(hand_landmark)
            return resultado_landmarks
        except:
            return []
