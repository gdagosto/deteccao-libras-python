from src.hand_tracking import HandDetector


class LibrasDetector(HandDetector):

    symbols_list = []

    def __init__(
        self,
        static_image_mode: bool = False,
        max_num_hands: int = 2,
        min_detection_confidence: float = 0.5,
        min_tracking_confidence: float = 0.5
    ):
        super().__init__(
            static_image_mode,
            max_num_hands,
            min_detection_confidence,
            min_tracking_confidence)

    def split_fingers(self, landmark_positions):
        num_dedos = 0
        dedos = []
        while num_dedos < 5:
            dedos.append((
                landmark_positions[num_dedos*4 + 1],
                landmark_positions[num_dedos*4 + 2],
                landmark_positions[num_dedos*4 + 3],
                landmark_positions[num_dedos*4 + 4]
            ))
            num_dedos += 1
        return dedos

    def is_raised_finger(self, finger, debug=False):
        # mx = 0
        my = 0
        for position in finger:
            # mx += position[0]
            my += position[1]

        # mx /= len(finger)
        my /= len(finger)

        # if(debug): print(finger, mx, my)
        if (debug):
            print(finger, my)

        # Apenas para cima
        return finger[1][1] > my and finger[2][1] < my

        # return finger[1][0] > mx and finger[1][1] < my and finger[2][0] < mx and finger[2][1] > my

    def find_raised_fingers(self, landmark_positions):
        fingers = self.split_fingers(landmark_positions)
        raised_fingers = 0
        for finger in fingers:
            raised_fingers += self.is_raised_finger(finger)

        return raised_fingers

    def find_symbols(self, landmark_positions):

        # Letra A
        landmark_positions[8][1]
