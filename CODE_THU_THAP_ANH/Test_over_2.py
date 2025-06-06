import cv2
import time
import os

# === Cấu hình thông số ===
fps = 26
prepare_duration = 4   # CB: 4s chuẩn bị
sample_duration = 4    # KH: 4s giữ ký hiệu
rest_duration = 2      # NG: 2s nghỉ
switch_duration = 6    # DG: 6s đổi góc
samples_per_angle = 5  # Mỗi góc 5 ký hiệu
angles = 5             # Số góc quay
label = "A"            # Nhãn ký hiệu

# === Tạo thư mục nếu chưa có ===
output_dir = "output"
os.makedirs(output_dir, exist_ok=True)

video_filename = os.path.join(output_dir, f"{label}.mp4")
text_filename = os.path.join(output_dir, f"{label}.txt")

# === Khởi tạo camera và video writer ===
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    raise RuntimeError("Không mở được camera")

frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter(video_filename, fourcc, fps, (frame_width, frame_height))

# === Biến theo dõi ===
stage = 'prepare'
angle_index = 0
sample_index = 0
start_time = time.time()
stage_start_time = start_time
stage_log = []

print(f"--- Bắt đầu thu video cho nhãn: {label} ---")

while angle_index < angles:
    ret, frame = cap.read()
    if not ret:
        break

    current_time = time.time()
    elapsed = current_time - stage_start_time
    elapsed_total = current_time - start_time

    # Hiển thị trạng thái hiện tại lên khung hình
    cv2.putText(frame, f"Stage: {stage.upper()}", (20, 50),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
    cv2.putText(frame, f"Angle: {angle_index + 1}/{angles}", (20, 90),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)
    cv2.putText(frame, f"Sample: {sample_index + 1}/{samples_per_angle}", (20, 130),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)

    # Ghi khung hình vào file video
    out.write(frame)
    cv2.imshow('Recording', frame)

    # ===== Điều khiển các giai đoạn =====
    if stage == 'prepare':
        if elapsed >= prepare_duration:
            print(f"{elapsed_total:.2f}s - CB kết thúc")
            stage_log.append((elapsed_total, 'CB'))
            stage = 'sample'
            stage_start_time = current_time

    elif stage == 'sample':
        if elapsed >= sample_duration:
            print(f"{elapsed_total:.2f}s - KH kết thúc")
            stage_log.append((elapsed_total, 'KH'))
            stage = 'rest'
            stage_start_time = current_time

    elif stage == 'rest':
        if elapsed >= rest_duration:
            print(f"{elapsed_total:.2f}s - NG kết thúc")
            stage_log.append((elapsed_total, 'NG'))
            sample_index += 1
            if sample_index >= samples_per_angle:
                sample_index = 0
                stage = 'switch'
            else:
                stage = 'sample'
            stage_start_time = current_time

    elif stage == 'switch':
        if elapsed >= switch_duration:
            print(f"{elapsed_total:.2f}s - DG kết thúc")
            stage_log.append((elapsed_total, 'DG'))
            angle_index += 1
            if angle_index >= angles:
                break
            stage = 'prepare'
            stage_start_time = current_time

    # Nhấn ESC để thoát sớm
    if cv2.waitKey(1) & 0xFF == 27:
        print("Thoát sớm bằng phím ESC.")
        break

# === Kết thúc ===
cap.release()
out.release()
cv2.destroyAllWindows()

# === Ghi log thời gian các pha vào file ===
with open(text_filename, 'w') as f:
    for time_val, label in stage_log:
        f.write(f"{time_val:.2f}s - {label}\n")

print(f"Đã lưu video: {video_filename}")
print(f"Đã ghi log thời gian các giai đoạn: {text_filename}")
