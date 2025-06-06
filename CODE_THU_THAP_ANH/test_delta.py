import os
import numpy as np

def process_and_pad(in_root="D:/dulieumediapipe", out_root="D:/DLHL", max_timesteps=46, feature_dim=126):
    for label in os.listdir(in_root):
        label_in = os.path.join(in_root, label)
        if not os.path.isdir(label_in):
            continue
        label_out = os.path.join(out_root, label)
        os.makedirs(label_out, exist_ok=True)

        for sample in os.listdir(label_in):
            sample_in = os.path.join(label_in, sample)
            if not os.path.isdir(sample_in):
                continue
            sample_out = os.path.join(label_out, sample)
            os.makedirs(sample_out, exist_ok=True)

            # Load frames theo thứ tự frame_1.npy, frame_2.npy, ...
            frames = []
            idx = 1
            while True:
                frame_path = os.path.join(sample_in, f"frame_{idx}.npy")
                if not os.path.isfile(frame_path):
                    break
                frames.append(np.load(frame_path))
                idx += 1

            if len(frames) < 2:
                print(f"⚠️ Sample {sample} có ít hơn 2 frame, bỏ qua")
                continue

            # Tính delta và raw (bỏ frame đầu)
            raw = np.stack(frames[1:], axis=0)                  # (N-1,21,3)
            delta = np.stack([frames[i] - frames[i-1] for i in range(1, len(frames))], axis=0)

            raw_flat = raw.reshape(raw.shape[0], -1)            # (N-1, 63)
            delta_flat = delta.reshape(delta.shape[0], -1)      # (N-1, 63)

            combined = np.concatenate([raw_flat, delta_flat], axis=1)  # (N-1, 126)

            orig_timesteps = combined.shape[0]

            # Padding pre (ở đầu)
            if orig_timesteps < max_timesteps:
                pad_len = max_timesteps - orig_timesteps
                pad_array = np.zeros((pad_len, feature_dim), dtype=np.float32)
                combined_padded = np.vstack([pad_array, combined])  # padding vào đầu
            else:
                combined_padded = combined[-max_timesteps:]  # cắt nếu quá dài

            print(f"Sample {sample}: timestep gốc = {orig_timesteps}, shape sau padding = {combined_padded.shape}")

            # Lưu file combined đã padding
            out_path = os.path.join(sample_out, f"{sample}.npy")
            np.save(out_path, combined_padded)

if __name__ == "__main__":
    process_and_pad()
