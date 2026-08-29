import cv2
import mediapipe as mp
import numpy as np
import math
import time

# Initialize mediapipe pose
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)
mp_draw = mp.solutions.drawing_utils

# Video feed
cap = cv2.VideoCapture(0)

def get_angle(a, b, c):
    """Calculate angle between 3 points"""
    a = np.array(a)
    b = np.array(b)
    c = np.array(c)
    radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
    angle = np.abs(radians*180.0/np.pi)
    if angle > 180.0:
        angle = 360 - angle
    return angle

def get_distance(p1, p2):
    return math.hypot(p1[0] - p2[0], p1[1] - p2[1])

while True:
    ret, frame = cap.read()
    if not ret:
        break
    h, w, _ = frame.shape

    # Flip for mirror view
    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = pose.process(rgb)

    if result.pose_landmarks:
        mp_draw.draw_landmarks(frame, result.pose_landmarks, mp_pose.POSE_CONNECTIONS)
        landmarks = result.pose_landmarks.landmark

        # Get key points
        left_shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x * w,
                         landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y * h]
        right_shoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x * w,
                          landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y * h]
        left_hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x * w,
                    landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y * h]
        right_hip = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x * w,
                     landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y * h]
        nose = [landmarks[mp_pose.PoseLandmark.NOSE.value].x * w,
                landmarks[mp_pose.PoseLandmark.NOSE.value].y * h]
        left_hand = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x * w,
                     landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y * h]
        right_hand = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x * w,
                      landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y * h]

        # Center of torso
        torso_y = (left_shoulder[1] + right_shoulder[1] + left_hip[1] + right_hip[1]) / 4

        # FALL DETECTION: check if torso is horizontal (shoulders & hips at same Y level)
        shoulder_diff = abs(left_shoulder[1] - right_shoulder[1])
        hip_diff = abs(left_hip[1] - right_hip[1])
        avg_shoulder_height = (left_shoulder[1] + right_shoulder[1]) / 2
        avg_hip_height = (left_hip[1] + right_hip[1]) / 2

        if shoulder_diff < 30 and hip_diff < 30 and avg_shoulder_height > h * 0.6:
            cv2.putText(frame, "FALL DETECTED!", (50, 100), cv2.FONT_HERSHEY_SIMPLEX,
                        1.2, (0, 0, 255), 4)

        # FIGHT DETECTION (simplified): Hands moving rapidly near another person (simulated by distance)
        hand_distance = get_distance(left_hand, right_hand)
        hand_to_nose = get_distance(left_hand, nose) + get_distance(right_hand, nose)

        if hand_distance < 150 and hand_to_nose < 300:
            cv2.putText(frame, "POSSIBLE FIGHTING!", (50, 150), cv2.FONT_HERSHEY_SIMPLEX,
                        1.2, (0, 255, 255), 4)

    cv2.imshow("Pose-Based Behavior Detection", frame)
    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
