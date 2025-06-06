import cv2
import time

# Cấu hình
fps_limit = 20
frame_size = (640, 480)
symbol_name = 'kyhieuA'  # Đặt tên ký hiệu tại đây
output_filename = f'{symbol_name}.mp4'
text_filename = f'{symbol_name}.txt'  # Tệp lưu thông tin giai đoạn

# Ghi file .mp4
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter(output_filename, fourcc, fps_limit, frame_size)

# Mở webcam
cap = cv2.VideoCapture(1)
if not cap.isOpened():
    print("Không thể mở webcam")
    exit()

# Thời gian từng phần
prepare_duration = 5     # Thêm thời gian chuẩn bị 5 giây
sample_duration = 4
rest_duration = 2
switch_duration = 6

total_samples = 30
samples_per_angle = 10
angles = 3

sample_count = 0
frame_count = 0
stage = 'prepare'  # Bắt đầu từ giai đoạn chuẩn bị

stage_start_time = time.time()
angle_count = 0

# Lưu giai đoạn vào file text
stage_log = []

print(f"Quay ký hiệu: {symbol_name}")
print("Nhấn 'q' để thoát sớm.")

# Tính thời gian thực tế đã trôi qua từ khi bắt đầu quay
real_time_start = time.time()

while True:
    ret, frame = cap.read()
    if not ret:
        break

    current_time = time.time()
    elapsed = current_time - stage_start_time

    display_frame = frame.copy()

    if stage == 'prepare':
        remaining = prepare_duration - elapsed
        cv2.putText(display_frame, f'Chuan bi: {int(remaining)}s', (160, 240),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.6, (0, 255, 0), 4)

        if elapsed >= prepare_duration:
            # Ghi thời gian thực tế kết thúc giai đoạn chuẩn bị
            stage_log.append(f"CB{current_time - real_time_start:.2f}")
            print(f"Thời gian thực tế đã trôi qua: {current_time - real_time_start:.2f}s - Giai đoạn chuẩn bị kết thúc")
            stage = 'symbol'
            stage_start_time = current_time

    elif stage == 'symbol':
        remaining = sample_duration - elapsed
        cv2.putText(display_frame, f'Giu ky hieu: {int(remaining)}s', (120, 240),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.6, (0, 0, 255), 4)
        out.write(frame)

        if elapsed >= sample_duration:
            # Ghi thời gian thực tế kết thúc giai đoạn ký hiệu
            stage_log.append(f"KH{current_time - real_time_start:.2f}")
            print(f"Thời gian thực tế đã trôi qua: {current_time - real_time_start:.2f}s - Giai đoạn ký hiệu kết thúc")
            stage = 'rest'
            stage_start_time = current_time

    elif stage == 'rest':
        remaining = rest_duration - elapsed
        cv2.putText(display_frame, f'Nghi: {int(remaining)}s', (200, 240),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.6, (255, 0, 0), 4)
        out.write(frame)

        if elapsed >= rest_duration:
            # Ghi thời gian thực tế kết thúc giai đoạn nghỉ
            stage_log.append(f"NG{current_time - real_time_start:.2f}")
            print(f"Thời gian thực tế đã trôi qua: {current_time - real_time_start:.2f}s - Giai đoạn nghỉ kết thúc")
            sample_count += 1
            if sample_count >= total_samples:
                break
            if sample_count % samples_per_angle == 0:
                if angle_count < angles - 1:
                    stage = 'switch'
                    stage_start_time = current_time
                    angle_count += 1
                else:
                    stage = 'symbol'
                    stage_start_time = current_time
            else:
                stage = 'symbol'
                stage_start_time = current_time

    elif stage == 'switch':
        remaining = switch_duration - elapsed
        cv2.putText(display_frame, f'Doi goc: {int(remaining)}s', (180, 240),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.6, (0, 128, 255), 4)
        out.write(frame)

        if elapsed >= switch_duration:
            # Ghi thời gian thực tế kết thúc giai đoạn đổi góc
            stage_log.append(f"DG{current_time - real_time_start:.2f}")
            print(f"Thời gian thực tế đã trôi qua: {current_time - real_time_start:.2f}s - Giai đoạn đổi góc kết thúc")
            stage = 'symbol'
            stage_start_time = current_time

    cv2.imshow('Camera', display_frame)
    frame_count += 1

    if cv2.waitKey(1) & 0xFF == ord('q'):
        print("Đã thoát sớm.")
        break

# Lưu thông tin chuyển giai đoạn vào tệp text theo thời gian thực tế
with open(text_filename, 'w') as f:
    f.write(','.join(stage_log))


# Thống kê
duration = time.time() - real_time_start
fps = frame_count / duration
print(f"Tổng frame: {frame_count}, FPS trung bình: {fps:.2f}")
print(f"Tổng thời gian thực tế: {duration:.2f} giây")

cap.release()
out.release()
cv2.destroyAllWindows()
