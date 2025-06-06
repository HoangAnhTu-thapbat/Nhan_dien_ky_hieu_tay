import cv2
import os
import numpy as np

# Đọc thông tin thời gian từ tệp .txt
def read_stage_times(txt_file):
    stage_times = []
    with open(txt_file, 'r') as f:
        # Đọc dòng và tách các phần bằng dấu phẩy
        line = f.read().strip()
        if line:
            parts = line.split(',')
            for part in parts:
                try:
                    stage, time_str = part.split(' ')
                    stage_times.append((stage, float(time_str)))  # Lưu thông tin giai đoạn và thời gian
                except ValueError:
                    print(f"Warning: Dòng không hợp lệ hoặc có định dạng không đúng: {part}")
        else:
            print("Warning: Tệp trống hoặc không có dữ liệu!")
    return stage_times

# Cắt video theo các giai đoạn với KH làm gốc
def cut_video_by_KH(video_filename, stage_times, output_folder, fps=20):
    cap = cv2.VideoCapture(video_filename)
    if not cap.isOpened():
        print(f"Không thể mở video: {video_filename}")
        return

    # Lấy tên video (không bao gồm phần mở rộng) làm tên thư mục đầu ra
    video_name = os.path.splitext(os.path.basename(video_filename))[0]

    # Tạo thư mục Dataset nếu chưa có
    dataset_folder = os.path.join(output_folder, video_name)
    if not os.path.exists(dataset_folder):
        os.makedirs(dataset_folder)

    frame_count = 0
    sample_count = 0

    # Lưu thông tin về các đoạn video
    stage_log = []

    # Lặp qua các mốc thời gian để cắt video
    for i in range(1, len(stage_times)):
        # Xác định thời gian bắt đầu (giai đoạn trước KH) và kết thúc của video đoạn
        start_time = stage_times[i-1][1]  # Thời gian mốc trước (không phân biệt CB, NG, DG)
        end_time = stage_times[i][1]  # Thời gian KH hiện tại

        # Chuyển video đến vị trí bắt đầu
        cap.set(cv2.CAP_PROP_POS_FRAMES, start_time * fps)

        # Tạo thư mục cho mỗi video con
        sample_folder = os.path.join(dataset_folder, f"sample_{sample_count + 1}")
        if not os.path.exists(sample_folder):
            os.makedirs(sample_folder)

        frame_list = []
        while True:
            ret, frame = cap.read()
            if not ret or frame_count >= (end_time - start_time) * fps:
                break
            # Lưu frame vào thư mục video mẫu
            frame_filename = os.path.join(sample_folder, f"frame_{frame_count}.png")
            cv2.imwrite(frame_filename, frame)
            frame_list.append(frame)
            frame_count += 1

        # Lưu thông tin về mốc thời gian và giai đoạn
        stage_log.append(f"KH{end_time:.2f}")

        # Tăng mẫu video
        sample_count += 1

    # Giải phóng tài nguyên
    cap.release()

    # Lưu thông tin giai đoạn vào tệp .txt
    txt_filename = os.path.join(dataset_folder, f"{video_name}.txt")  # Đổi tên tệp text theo tên video
    with open(txt_filename, 'w') as f:
        for log in stage_log:
            f.write(f"{log}\n")

    print(f"Quá trình hoàn tất. Dữ liệu đã được lưu tại {txt_filename}")

# Đọc các mốc thời gian từ tệp .txt
def process_single_video(video_filename, txt_file, output_folder):
    # Đọc các mốc thời gian từ tệp .txt
    stage_times = read_stage_times(txt_file)

    # Cắt video theo các giai đoạn KH và lưu kết quả
    cut_video_by_KH(video_filename, stage_times, output_folder)

# Cấu hình: Lấy tên video và tệp .txt từ tên video
video_filename = 'KyHieuA.mp4'  # Ví dụ video đầu vào
txt_file = 'KyHieuA.txt'  # Ví dụ tệp .txt chứa thông tin giai đoạn
output_folder = 'D:/dataset'  # Chỉ định thư mục đầu ra để lưu các video mẫu

# Chạy code cho một video cụ thể
process_single_video(video_filename, txt_file, output_folder)
