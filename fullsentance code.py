import csv
import copy
import cv2 as cv
import mediapipe as mp
import pyttsx3
from textblob import TextBlob
from model import KeyPointClassifier
from app_files import calc_landmark_list, draw_info_text, draw_landmarks, get_args, pre_process_landmark


def draw_multiline_text(image, text, origin, font, scale, color, thickness, line_height=30, max_width=600):
    x, y = origin
    words = text.split(' ')
    line = ''
    for word in words:
        test_line = line + word + ' '
        text_size = cv.getTextSize(test_line, font, scale, thickness)[0]
        if text_size[0] > max_width:
            cv.putText(image, line, (x, y), font, scale, color, thickness, cv.LINE_AA)
            line = word + ' '
            y += line_height
        else:
            line = test_line
    cv.putText(image, line, (x, y), font, scale, color, thickness, cv.LINE_AA)
    return image


def process_sign_to_sentence(sign):
    if sign.lower() == "space":
        return " "
    elif sign.lower() == "clear":
        return ""
    elif sign.lower() == "aapple":  # map custom label to actual letter
        return "A"
    else:
        return sign


def correct_sentence(raw_sentence):
    try:
        blob = TextBlob(raw_sentence)
        return str(blob.correct())
    except:
        return raw_sentence


def main():
    args = get_args()

    cap_device = args.device
    cap_width = args.width
    cap_height = args.height
    use_static_image_mode = args.use_static_image_mode
    min_detection_confidence = args.min_detection_confidence
    min_tracking_confidence = args.min_tracking_confidence

    cap = cv.VideoCapture(cap_device)
    cap.set(cv.CAP_PROP_FRAME_WIDTH, cap_width)
    cap.set(cv.CAP_PROP_FRAME_HEIGHT, cap_height)

    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(
        static_image_mode=use_static_image_mode,
        max_num_hands=2,
        min_detection_confidence=min_detection_confidence,
        min_tracking_confidence=min_tracking_confidence,
    )

    keypoint_classifier = KeyPointClassifier()

    with open('model/keypoint_classifier/keypoint_classifier_label.csv', encoding='utf-8-sig') as f:
        keypoint_classifier_labels = csv.reader(f)
        keypoint_classifier_labels = [row[0] for row in keypoint_classifier_labels]

    sentence = ""
    prev_sign_id_left = None
    prev_sign_id_right = None
    engine = pyttsx3.init()

    while True:
        key = cv.waitKey(10)
        if key == 27:
            break
        elif key == ord('c'):
            sentence = ""
        elif key == ord('s'):
            if sentence.strip() != "":
                corrected = correct_sentence(sentence)
                print(f"[Corrected] {corrected}")
                engine.say(corrected)
                engine.runAndWait()

        ret, image = cap.read()
        if not ret:
            break
        image = cv.flip(image, 1)
        debug_image = copy.deepcopy(image)

        image = cv.cvtColor(image, cv.COLOR_BGR2RGB)
        image.flags.writeable = False
        results = hands.process(image)
        image.flags.writeable = True

        if results.multi_hand_landmarks and results.multi_handedness:
            for hand_landmarks, handedness in zip(results.multi_hand_landmarks, results.multi_handedness):
                landmark_list = calc_landmark_list(debug_image, hand_landmarks)
                pre_processed_landmark_list = pre_process_landmark(landmark_list)
                hand_sign_id = keypoint_classifier(pre_processed_landmark_list)
                sign = keypoint_classifier_labels[hand_sign_id]

                hand_label = handedness.classification[0].label  # 'Left' or 'Right'
                debug_image = draw_landmarks(debug_image, landmark_list)
                debug_image = draw_info_text(debug_image, handedness, sign)

                if hand_label == "Left":
                    if hand_sign_id != prev_sign_id_left:
                        addition = process_sign_to_sentence(sign)
                        if sign.lower() == "clear":
                            sentence = ""
                        else:
                            sentence += addition
                        prev_sign_id_left = hand_sign_id
                elif hand_label == "Right":
                    if hand_sign_id != prev_sign_id_right:
                        addition = process_sign_to_sentence(sign)
                        if sign.lower() == "clear":
                            sentence = ""
                        else:
                            sentence += addition
                        prev_sign_id_right = hand_sign_id

        draw_multiline_text(
            debug_image,
            f'Sentence: {sentence}',
            origin=(10, 40),
            font=cv.FONT_HERSHEY_SIMPLEX,
            scale=0.8,
            color=(0, 255, 0),
            thickness=2,
            line_height=35,
            max_width=debug_image.shape[1] - 20
        )

        cv.imshow('Two-Hand Gesture Recognition', debug_image)

    cap.release()
    cv.destroyAllWindows()


if __name__ == '__main__':
    main()
