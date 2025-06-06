import cv2
import os
import time

# Hàm lưu frame vào thư mục
def save_frame(frame, sample_folder, frame_count):
    frame_filename = os.path.join(sample_folder, f"frame_{frame_count}.png")
    cv2.imwrite(frame_filename, frame)

# Quay video và lưu dữ liệu từ sample_31 đến sample_60
def process_video(fps=20, frame_size=(640, 480), output_folder="D:/testkyhieu"):
    cap = cv2.VideoCapture(1)  # Mở webcam
    if not cap.isOpened():
        print("Không thể mở webcam.")
        return

    # Cấu hình các giai đoạn
    stages = {
        'prepare': {'color': (0, 255, 0), 'time': 5},
        'symbol': {'color': (0, 0, 255), 'time': 4},
        'rest': {'color': (255, 0, 0), 'time': 2},
        'switch': {'color': (0, 128, 255), 'time': 6},
    }

    sample_count = 0
    frame_count = 0
    stage = 'prepare'
    stage_start_time = time.time()
    dataset_folder = os.path.join(output_folder, "KyHieuA")

    if not os.path.exists(dataset_folder):
        print("Thư mục KyHieuA chưa tồn tại.")
        return

    total_samples = 30              # Ghi thêm 30 mẫu
    start_index = 31               # Bắt đầu từ sample_31
    samples_per_angle = 10         # Mỗi góc 10 mẫu

    while sample_count < total_samples:
        ret, frame = cap.read()
        if not ret:
            break

        current_time = time.time()
        elapsed = current_time - stage_start_time
        display_frame = frame.copy()

        # Hiển thị số mẫu
        cv2.putText(display_frame, f'Sample: {start_index + sample_count}/{start_index + total_samples - 1}', (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

        if stage == 'prepare':
            remaining = stages[stage]['time'] - elapsed
            cv2.putText(display_frame, f'Chuan bi: {int(remaining)}s', (160, 240),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.6, stages[stage]['color'], 4)
            if elapsed >= stages[stage]['time']:
                stage = 'symbol'
                stage_start_time = current_time

        elif stage == 'symbol':
            remaining = stages[stage]['time'] - elapsed
            cv2.putText(display_frame, f'Giu ky hieu: {int(remaining)}s', (120, 240),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.6, stages[stage]['color'], 4)

            # Tạo thư mục mẫu tiếp theo
            sample_folder = os.path.join(dataset_folder, f"sample_{start_index + sample_count}")
            if not os.path.exists(sample_folder):
                os.makedirs(sample_folder)

            # Lưu frame
            save_frame(frame, sample_folder, frame_count)
            frame_count += 1

            if elapsed >= stages[stage]['time']:
                stage = 'rest'
                stage_start_time = current_time
                sample_count += 1

        elif stage == 'rest':
            remaining = stages[stage]['time'] - elapsed
            cv2.putText(display_frame, f'Nghi: {int(remaining)}s', (200, 240),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.6, stages[stage]['color'], 4)
            if elapsed >= stages[stage]['time']:
                # Đổi góc sau mỗi 10 mẫu
                if sample_count % samples_per_angle == 0 and sample_count < total_samples:
                    stage = 'switch'
                else:
                    stage = 'symbol'
                stage_start_time = current_time

        elif stage == 'switch':
            remaining = stages[stage]['time'] - elapsed
            cv2.putText(display_frame, f'Doi goc: {int(remaining)}s', (180, 240),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.6, stages[stage]['color'], 4)
            if elapsed >= stages[stage]['time']:
                stage = 'symbol'
                stage_start_time = current_time

        cv2.imshow('Camera', display_frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    print(f"Hoàn tất thu thêm 30 mẫu. Dữ liệu nằm trong {dataset_folder}")
    cap.release()
    cv2.destroyAllWindows()

# Gọi hàm
output_folder = 'D:/testkyhieu'
process_video(output_folder=output_folder)