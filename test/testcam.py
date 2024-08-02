import cv2
import mediapipe as mp
import numpy as np
import pickle
from collections import deque
from statistics import mode

# Khởi tạo Mediapipe
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

# Đường dẫn đến file mô hình đã huấn luyện
model_path = 'asl3_model.pkl'


# Hàm để trích xuất landmarks từ một ảnh
def extract_landmarks(image):
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    with mp_hands.Hands(static_image_mode=True, max_num_hands=1, min_detection_confidence=0.5) as hands:
        results = hands.process(image_rgb)

        if results.multi_hand_landmarks:
            hand_landmarks = results.multi_hand_landmarks[0]
            landmarks = []
            for lm in hand_landmarks.landmark:
                landmarks.extend([lm.x, lm.y, lm.z])
            return landmarks
        else:
            return None


# Tải mô hình đã huấn luyện
with open(model_path, 'rb') as f:
    model = pickle.load(f)

# Mở webcam
cap = cv2.VideoCapture(0)

# Khởi tạo hàng đợi để lưu trữ kết quả dự đoán
prediction_queue = deque(maxlen=10)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Trích xuất landmarks từ khung hình
    landmarks = extract_landmarks(frame)
    if landmarks:
        landmarks = np.array(landmarks).reshape(1, -1)  # Định dạng lại cho mô hình dự đoán
        prediction = model.predict(landmarks)
        predicted_sign = prediction[0]
        prediction_queue.append(predicted_sign)

        # Lấy ký hiệu được dự đoán nhiều nhất trong hàng đợi
        most_common_sign = mode(prediction_queue)

        # Hiển thị dự đoán lên khung hình
        cv2.putText(frame, f'Predicted ASL sign: {most_common_sign}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1,
                    (0, 255, 0), 2, cv2.LINE_AA)

    # Hiển thị khung hình
    cv2.imshow('ASL Sign Prediction', frame)

    # Nhấn 'q' để thoát
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Giải phóng tài nguyên
cap.release()
cv2.destroyAllWindows()
