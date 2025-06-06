import cv2
import os
import time

def save_frame(frame, sample_folder, frame_count):
    resized = cv2.resize(frame, (224, 224))  # Resize để lưu
    frame_filename = os.path.join(sample_folder, f"frame_{frame_count}.png")
    cv2.imwrite(frame_filename, resized)


def process_video(fps=15, frame_size=(640, 480), output_folder="D:/testkyhieu"):
    cap = cv2.VideoCapture(1)
    if not cap.isOpened():
        print("Không thể mở webcam.")
        return

    stages = {
        'prepare': {'color': (0, 255, 0), 'time': 5},
        'symbol': {'color': (0, 0, 255), 'time': 3},
        'rest': {'color': (255, 0, 0), 'time': 2},
        'switch': {'color': (0, 128, 255), 'time': 6},
    }

    stage_log = []
    sample_count = 0
    frame_count = 0
    stage = 'prepare'
    stage_start_time = time.time()

    angle_count = 0
    dataset_folder = os.path.join(output_folder, "KyHieuTEST")
    if not os.path.exists(dataset_folder):
        os.makedirs(dataset_folder)

    total_samples = 60
    samples_per_angle = 10

    # Thông số theo dõi fps trung bình
    frame_times = []
    last_fps_print = time.time()

    while sample_count < total_samples:
        start_time = time.time()
        ret, frame = cap.read()
        if not ret:
            break

        current_time = time.time()
        elapsed = current_time - stage_start_time
        display_frame = frame.copy()

        cv2.putText(display_frame, f'Sample: {sample_count + 1}/{total_samples}', (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

        if stage == 'prepare':
            remaining = stages[stage]['time'] - elapsed
            cv2.putText(display_frame, f'Chuan bi: {int(remaining)}s', (160, 240),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.6, stages[stage]['color'], 4)
            if elapsed >= stages[stage]['time']:
                stage_log.append(f"CB{elapsed:.2f}")
                stage = 'symbol'
                stage_start_time = current_time

        elif stage == 'symbol':
            remaining = stages[stage]['time'] - elapsed
            cv2.putText(display_frame, f'Giu ky hieu: {int(remaining)}s', (120, 240),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.6, stages[stage]['color'], 4)

            sample_folder = os.path.join(dataset_folder, f"sample_{sample_count + 1}")
            if not os.path.exists(sample_folder):
                os.makedirs(sample_folder)

            save_frame(frame, sample_folder, frame_count)
            frame_count += 1

            if elapsed >= stages[stage]['time']:
                stage_log.append(f"KH{elapsed:.2f}")
                stage = 'rest'
                stage_start_time = current_time
                sample_count += 1

        elif stage == 'rest':
            remaining = stages[stage]['time'] - elapsed
            cv2.putText(display_frame, f'Nghi: {int(remaining)}s', (200, 240),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.6, stages[stage]['color'], 4)
            if elapsed >= stages[stage]['time']:
                stage_log.append(f"NG{elapsed:.2f}")
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
                stage_log.append(f"DG{elapsed:.2f}")
                stage = 'symbol'
                stage_start_time = current_time

        show_frame = cv2.resize(display_frame, (960, 720))  # Hoặc bất kỳ kích thước nào bạn thích
        cv2.imshow('Camera', show_frame)


        # Tính FPS trung bình mỗi 10 giây
        frame_times.append(time.time())
        if time.time() - last_fps_print >= 10:
            valid_times = [t for t in frame_times if time.time() - t <= 10]
            avg_fps = len(valid_times) / 10.0
            print(f"[FPS trung bình ~ 10s]: {avg_fps:.2f} fps")
            last_fps_print = time.time()
            frame_times = valid_times  # Giữ lại frame time gần nhất

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        # Chờ sao cho đạt fps yêu cầu
        elapsed_frame_time = time.time() - start_time
        wait_time = max(0, (1.0 / fps) - elapsed_frame_time)
        time.sleep(wait_time)

    txt_filename = os.path.join(dataset_folder, "KyHieuTEST.txt")
    with open(txt_filename, 'w') as f:
        for log in stage_log:   
            f.write(f"{log}\n")

    print(f"Hoàn tất. Dữ liệu lưu tại: {txt_filename}")
    cap.release()
    cv2.destroyAllWindows()

# Gọi hàm
output_folder = 'D:/testkyhieu'
process_video(output_folder=output_folder)
