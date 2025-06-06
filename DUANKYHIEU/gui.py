import tkinter as tk
from PIL import Image, ImageTk
import cv2
import os
import numpy as np
import time
from preprocess import process_sample  # hàm xử lý sample mediaPipe + delta + padding + lưu npy

class GestureAppGui:
    def __init__(self, window, window_title, model):
        self.window = window
        self.window.title(window_title)
        self.model = model

        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            raise RuntimeError("Không mở được webcam")

        # Giao diện
        self.label_video = tk.Label(window)
        self.label_video.pack()

        self.status_var = tk.StringVar(value="Chờ bắt đầu")
        self.label_status = tk.Label(window, textvariable=self.status_var, font=("Arial", 16))
        self.label_status.pack()

        self.result_text = tk.Text(window, height=3, font=("Arial", 14))
        self.result_text.pack(fill="x", padx=5, pady=5)
        self.result_text.config(state=tk.DISABLED)

        self.btn_frame = tk.Frame(window)
        self.btn_frame.pack()

        self.btn_start = tk.Button(self.btn_frame, text="Bắt đầu", command=self.start)
        self.btn_start.pack(side=tk.LEFT)

        self.btn_stop = tk.Button(self.btn_frame, text="Dừng", command=self.stop)
        self.btn_stop.pack(side=tk.LEFT)

        self.btn_continue = tk.Button(self.btn_frame, text="Tiếp tục", command=self.continue_)
        self.btn_continue.pack(side=tk.LEFT)

        # Trạng thái ban đầu
        self.running = False
        self.stop_requested = False

        self.stage = None
        self.stage_start_time = None
        self.cycle_step = 0

        self.sample_folder = None
        self.frame_count = 0

        # Thời gian từng giai đoạn (giây)
        self.prepare_time = 3
        self.hold_time = 3
        self.rest_time = 2

        self.window.after(0, self.update_frame)

    def start(self):
        self.running = True
        self.stop_requested = False
        self.cycle_step = 1
        self.clear_result()
        self.sample_folder = None
        self.frame_count = 0
        self._change_stage('prepare')

    def stop(self):
        self.stop_requested = True  # Dừng sau giai đoạn hiện tại

    def continue_(self):
        if not self.running:
            self.running = True
            self.stop_requested = False
            self._change_stage('prepare')  # Bắt đầu lại từ chuẩn bị, không xóa kết quả

    def clear_result(self):
        self.result_text.config(state=tk.NORMAL)
        self.result_text.delete('1.0', tk.END)
        self.result_text.config(state=tk.DISABLED)

    def append_result(self, text):
        self.result_text.config(state=tk.NORMAL)
        current_text = self.result_text.get('1.0', 'end-1c')  # Lấy nội dung KHÔNG bao gồm ký tự newline cuối
        new_text = current_text + text  # Nối sát hoặc có thể thêm dấu cách: current_text + " " + text
        self.result_text.delete('1.0', tk.END)
        self.result_text.insert(tk.END, new_text)
        self.result_text.config(state=tk.DISABLED)

    def save_frame(self, frame):
        if self.sample_folder is None:
            base_dir = "mediadelta"
            os.makedirs(base_dir, exist_ok=True)
            self.sample_folder = os.path.join(base_dir, f"sample_{self.cycle_step}")
            os.makedirs(self.sample_folder, exist_ok=True)
            self.frame_count = 0

        resized = cv2.resize(frame, (224, 224))
        filename = os.path.join(self.sample_folder, f"frame_{self.frame_count}.png")
        cv2.imwrite(filename, resized)
        self.frame_count += 1

    def _change_stage(self, new_stage):
        self.stage = new_stage
        self.stage_start_time = time.time()
        if new_stage == 'prepare':
            self.status_var.set(f"Chuẩn bị: {self.prepare_time}s")
        elif new_stage == 'hold':
            self.status_var.set(f"Giữ ký hiệu: {self.hold_time}s")
        elif new_stage == 'rest':
            self.status_var.set(f"Nghỉ: {self.rest_time}s")

    def update_frame(self):
        ret, frame = self.cap.read()
        if ret:
            # Hiển thị video
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame_rgb)
            imgtk = ImageTk.PhotoImage(image=img)
            self.label_video.imgtk = imgtk
            self.label_video.configure(image=imgtk)

            if self.running and not self.stop_requested:
                elapsed = time.time() - self.stage_start_time

                if self.stage == 'prepare':
                    remaining = max(0, int(self.prepare_time - elapsed))
                    self.status_var.set(f"Chuẩn bị: {remaining}s")
                    if elapsed >= self.prepare_time:
                        self._change_stage('hold')

                elif self.stage == 'hold':
                    remaining = max(0, int(self.hold_time - elapsed))
                    self.status_var.set(f"Giữ ký hiệu: {remaining}s")
                    self.save_frame(frame)
                    if elapsed >= self.hold_time:
                        self._change_stage('rest')
                        # Xử lý mẫu không chặn giao diện
                        self.window.after(10, self.process_current_sample_async)

                elif self.stage == 'rest':
                    remaining = max(0, int(self.rest_time - elapsed))
                    self.status_var.set(f"Nghỉ: {remaining}s")
                    if elapsed >= self.rest_time:
                        if self.stop_requested:
                            self.running = False
                            self.status_var.set("Đã dừng.")
                        else:
                            self.cycle_step += 1
                            self.sample_folder = None
                            self.frame_count = 0
                            self._change_stage('prepare')

            elif self.running and self.stop_requested:
                # Dừng sau giai đoạn hiện tại
                if self.stage == 'rest' and (time.time() - self.stage_start_time >= self.rest_time):
                    self.running = False
                    self.status_var.set("Đã dừng.")

        self.window.after(66, self.update_frame)  # ~15fps

    def process_current_sample_async(self):
        if self.sample_folder is None:
            return
        processed_path = process_sample(self.sample_folder)
        if processed_path is not None:
            input_data = np.load(processed_path)
            result = self.model.predict(input_data)
            # Giả định result trả về chuỗi ký tự hoặc list ký tự
            # Bạn chỉnh lại tùy mô hình
            self.append_result(result)
        else:
            self.append_result("[Không đủ dữ liệu để dự đoán]")
