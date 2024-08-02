import numpy as np
import os
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import pickle

# Đường dẫn đến thư mục chứa landmarks
data_dir = 'D:/test1/NCKH4/test/npy'


# Hàm đọc dữ liệu từ các file .npy
def load_data(data_dir):
    X = []
    y = []
    for root, dirs, files in os.walk(data_dir):
        for filename in files:
            if filename.endswith('.npy'):
                label = os.path.basename(root)  # Lấy nhãn từ tên thư mục chứa file
                landmarks = np.load(os.path.join(root, filename))
                X.append(landmarks)
                y.append(label)
    return np.array(X), np.array(y)


# Load dữ liệu
X, y = load_data(data_dir)

# Chia dữ liệu thành tập huấn luyện và tập kiểm tra
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Huấn luyện mô hình
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Dự đoán và đánh giá mô hình
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f'Accuracy: {accuracy * 100:.2f}%')

# Lưu mô hình đã huấn luyện
with open('asl3_model.pkl', 'wb') as f:
    pickle.dump(model, f)
