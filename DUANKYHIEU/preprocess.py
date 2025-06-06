import os
import cv2
import numpy as np
import mediapipe as mp

mp_hands = mp.solutions.hands

def extract_landmarks_from_image(img_path, hands):
    img = cv2.imread(img_path)
    if img is None:
        return None
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(img_rgb)
    if not results.multi_hand_landmarks:
        return None
    # Lấy tay đầu tiên, 21 điểm
    landmarks = results.multi_hand_landmarks[0]
    keypoints = []
    for lm in landmarks.landmark:
        keypoints.append([lm.x, lm.y, lm.z])
    return np.array(keypoints)  # shape (21,3)

def process_sample(sample_folder, max_timesteps=46, feature_dim=126):
    hands = mp_hands.Hands(static_image_mode=True, max_num_hands=1)

    frames = []
    idx = 0
    while True:
        frame_path = os.path.join(sample_folder, f"frame_{idx}.png")
        if not os.path.isfile(frame_path):
            break
        keypoints = extract_landmarks_from_image(frame_path, hands)
        if keypoints is not None and keypoints.shape == (21,3):
            frames.append(keypoints)
        idx += 1
    hands.close()

    if len(frames) < 2:
        print(f"⚠️ Sample {sample_folder} có ít hơn 2 frame có landmark, bỏ qua")
        return None

    # Tính delta
    raw = np.stack(frames[1:], axis=0)
    delta = np.stack([frames[i] - frames[i-1] for i in range(1, len(frames))], axis=0)

    # Flatten thành (N-1, 63)
    raw_flat = raw.reshape(raw.shape[0], -1)
    delta_flat = delta.reshape(delta.shape[0], -1)

    combined = np.concatenate([raw_flat, delta_flat], axis=1)  # (N-1, 126)

    orig_timesteps = combined.shape[0]

    # Padding ở đầu
    if orig_timesteps < max_timesteps:
        pad_len = max_timesteps - orig_timesteps
        pad_array = np.zeros((pad_len, feature_dim), dtype=np.float32)
        combined_padded = np.vstack([pad_array, combined])
    else:
        combined_padded = combined[-max_timesteps:]

    # Lưu kết quả processed
    processed_folder = os.path.join(sample_folder, "processed")
    os.makedirs(processed_folder, exist_ok=True)
    save_path = os.path.join(processed_folder, os.path.basename(sample_folder) + ".npy")
    np.save(save_path, combined_padded)
    print(f"Đã lưu dữ liệu processed của {sample_folder} tại {save_path}")

    return save_path

if __name__ == "__main__":
    # Test chạy
    sample_path = "mediadelta/sample_1"
    process_sample(sample_path)
