import cv2
import numpy as np
from tensorflow.keras.models import load_model

# Tải mô hình đã huấn luyện
model = load_model('/content/drive/MyDrive/Dataset/gesture_model.h5')

# Mở webcam
cap = cv2.VideoCapture(0)  # Nếu dùng webcam gắn ngoài, có thể thay số 0 bằng 1

# Kiểm tra webcam
if not cap.isOpened():
    print("Không thể mở webcam")
    exit()

# Khởi tạo MediaPipe Hands (hoặc có thể dùng các phương pháp khác để phát hiện tay)
import mediapipe as mp

mp_hands = mp.solutions.hands
hands = mp_hands.Hands()

# Dòng màu sắc và font để hiển thị kết quả
font = cv2.FONT_HERSHEY_SIMPLEX

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Chuyển frame sang RGB để xử lý với MediaPipe
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Phát hiện bàn tay
    results = hands.process(rgb_frame)

    # Kiểm tra nếu có bàn tay trong frame
    if results.multi_hand_landmarks:
        for landmarks in results.multi_hand_landmarks:
            # Vẽ các điểm khớp bàn tay lên frame
            mp.solutions.drawing_utils.draw_landmarks(frame, landmarks, mp_hands.HAND_CONNECTIONS)

            # Lấy keypoints từ các điểm khớp
            keypoints = []
            for landmark in landmarks.landmark:
                keypoints.append([landmark.x, landmark.y, landmark.z])
            
            # Chuyển keypoints thành mảng NumPy
            keypoints_array = np.array(keypoints).flatten()  # Làm phẳng keypoints

            # Đảm bảo rằng số lượng keypoints phù hợp với mô hình
            keypoints_array = np.expand_dims(keypoints_array, axis=0)  # Thêm batch dimension

            # Dự đoán từ mô hình
            prediction = model.predict(keypoints_array)
            predicted_label = np.argmax(prediction, axis=1)[0]

            # Hiển thị nhãn dự đoán
            cv2.putText(frame, f'Predicted: {predicted_label}', (10, 30), font, 1, (0, 255, 0), 2, cv2.LINE_AA)

    # Hiển thị video trong thời gian thực
    cv2.imshow("Gesture Recognition", frame)

    # Nhấn 'q' để thoát
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Giải phóng tài nguyên
cap.release()
cv2.destroyAllWindows()
