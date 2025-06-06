import cv2
import mediapipe as mp
import numpy as np
import os

input_base_path = "D:/testkyhieu"
output_base_path = "D:/dulieumediapipe"

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=True, max_num_hands=1, min_detection_confidence=0.5)

def get_hand_keypoints(frame):
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)

    if results.multi_hand_landmarks:
        landmarks = results.multi_hand_landmarks[0]
        keypoints = [[lm.x, lm.y, lm.z] for lm in landmarks.landmark]
        if len(keypoints) == 21:
            return np.array(keypoints, dtype=np.float32)
    return None

def process_keypoints_for_symbol(symbol_name):
    symbol_input_path = os.path.join(input_base_path, symbol_name)
    symbol_output_path = os.path.join(output_base_path, symbol_name)
    os.makedirs(symbol_output_path, exist_ok=True)

    for sample_folder in os.listdir(symbol_input_path):
        sample_folder_path = os.path.join(symbol_input_path, sample_folder)
        if not os.path.isdir(sample_folder_path):
            continue

        sample_output_path = os.path.join(symbol_output_path, sample_folder)
        os.makedirs(sample_output_path, exist_ok=True)

        frame_counter = 1  # Bắt đầu đánh số frame lại từ 1 cho mỗi sample

        for filename in sorted(os.listdir(sample_folder_path)):
            if filename.lower().endswith((".png", ".jpg", ".jpeg")):
                frame_path = os.path.join(sample_folder_path, filename)
                frame = cv2.imread(frame_path)
                if frame is None:
                    print(f"⚠️ Không đọc được file {filename}, bỏ qua")
                    continue

                keypoints = get_hand_keypoints(frame)
                if keypoints is not None:
                    save_path = os.path.join(sample_output_path, f"frame_{frame_counter}.npy")
                    np.save(save_path, keypoints)
                    print(f"Đã lưu keypoints {save_path}")
                    frame_counter += 1  # Chỉ tăng khi lưu thành công
                else:
                    print(f"Không phát hiện bàn tay trong {filename}, bỏ qua frame đó")

if __name__ == "__main__":
    for symbol_name in os.listdir(input_base_path):
        symbol_path = os.path.join(input_base_path, symbol_name)
        if os.path.isdir(symbol_path):
            print(f"Đang xử lý ký hiệu: {symbol_name}")
            process_keypoints_for_symbol(symbol_name)

    print("Xong toàn bộ việc trích xuất keypoints!")
