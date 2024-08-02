import cv2
import mediapipe as mp
import numpy as np
import os

# Khởi tạo Mediapipe
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

# Đường dẫn đến thư mục chứa ảnh
image_dir = 'D:/test1/NCKH4/test/data2'
output_dir = 'D:/test1/NCKH4/test/npy'

# Tạo các thư mục con trong output_dir nếu chưa tồn tại
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
# Thêm các thư mục cho các chữ cái và các ký tự đặc biệt
categories = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ") + ["del", "space", "nothing"]
for category in categories:
    category_dir = os.path.join(output_dir, category)

    if not os.path.exists(category_dir):
        os.makedirs(category_dir)


# Hàm để trích xuất landmarks từ một ảnh
def extract_landmarks(image_path):
    image = cv2.imread(image_path)
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


# Lặp qua tất cả các thư mục và file ảnh để trích xuất landmarks
for root, dirs, files in os.walk(image_dir):
    for filename in files:
        if filename.endswith('.jpg'):
            image_path = os.path.join(root, filename)
            landmarks = extract_landmarks(image_path)
            if landmarks:
                # Tên file landmarks, có thể gán nhãn dựa trên tên thư mục
                label = os.path.basename(root)  # Thư mục chứa ảnh sẽ là nhãn
                if label in categories:
                    label_dir = os.path.join(output_dir, label)
                else:
                    label_dir = os.path.join(output_dir, "unknown")  # Thư mục dự phòng cho nhãn không xác định
                    if not os.path.exists(label_dir):
                        os.makedirs(label_dir)
                output_file = os.path.join(label_dir, f'{label}_{filename[:-4]}.npy')
                np.save(output_file, np.array(landmarks))
                print(f'Landmarks từ {filename} trong thư mục {label} đã được lưu vào {output_file}')
