# Hand Gesture Recognition bằng Học Máy

## Mô tả dự án
Dự án triển khai hệ thống nhận diện cử chỉ tay sử dụng học máy (LSTM) và thư viện MediaPipe của Google. Quy trình gồm:

1. **Thu thập dữ liệu**:  
   - Sử dụng webcam và OpenCV để quay video cử chỉ theo từng mẫu, chia thành bốn giai đoạn:  
     - Chuẩn bị (3s)  
     - Giữ ký hiệu (3s, lưu ảnh mỗi frame, resize 224×224)  
     - Nghỉ (2s)  
     - Đổi góc (sau mỗi 10 mẫu, 6s)  
   - Kết quả: Thư mục đầu ra chứa các folder `sample_i/` với các ảnh `frame_j.png`.

2. **Tiền xử lý & trích xuất đặc trưng**:  
   - Dùng **MediaPipe Hands** để trích xuất 21 landmark (x, y, z) cho mỗi khung ảnh, lưu dưới dạng `.npy` (shape (21, 3)).  
   - Tính **delta** giữa các khung liên tiếp:  
     - `raw = stack(frames[1:], axis=0)` (shape (N-1, 21, 3))  
     - `delta = [frames[i] - frames[i-1] for i in 1..N-1]` (shape (N-1, 21, 3))  
     - `raw_flat = raw.reshape((N-1), 63)`  
     - `delta_flat = delta.reshape((N-1), 63)`  
     - `combined = concatenate([raw_flat, delta_flat], axis=1)` → shape (N-1, 126)  
   - **Padding/Cắt** chuỗi thành độ dài cố định 46 timesteps:  
     - Nếu (N-1) < 46: thêm zeros lên đầu → shape (46, 126)  
     - Nếu (N-1) ≥ 46: giữ 46 dòng cuối  
   - Lưu file `.npy` (46×126) cho mỗi sample.

3. **Huấn luyện mô hình LSTM**:  
   - Kiến trúc:  
     1. `Masking(mask_value=0., input_shape=(46, 126))`  
     2. `LSTM(64)`  
     3. `Dense(64, activation='relu')`  
     4. `Dense(32, activation='softmax')`  
   - Optimizer: `Adam`  
   - Loss: `sparse_categorical_crossentropy`  
   - Callbacks: `EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=True)` và `ModelCheckpoint('best_model.h5', monitor='val_loss', save_best_only=True)`  
   - Phân loại 32 ký hiệu (map sang số nguyên 0–31).  
   - Kết quả thực nghiệm (test set): ~95% accuracy, thời gian xử lý mỗi mẫu ~1.8 giây trên CPU.

4. **Ứng dụng real-time (GUI)**:  
   - Giao diện Tkinter:  
     - Khung video, Label trạng thái, Text widget hiển thị kết quả, 3 nút: **Bắt đầu**, **Dừng**, **Tiếp tục**.  
   - Khi nhấn **Bắt đầu**:  
     1. Chạy chu trình **Chuẩn bị → Giữ ký hiệu → Nghỉ**.  
     2. Lưu ảnh trong giai đoạn “Giữ ký hiệu” vào folder `sample_i/`.  
     3. Sau khi xong giai đoạn giữ, gọi hàm **process_sample(sample_folder)**:  
        - Trích xuất landmark, tính delta, flatten, padding  
        - Lưu file `<sample_i>.npy` (46×126)  
        - Load mảng input và gọi `model.predict(...)` để dự đoán ký hiệu  
        - Append kết quả (ký tự) vào Text widget  
   - Nút **Dừng**: dừng thu mẫu (sau khi giai đoạn nghỉ hiện tại kết thúc).  
   - Nút **Tiếp tục**: tiếp tục thu mẫu mới mà không xóa kết quả cũ.



5. **Chạy ứng dụng**
   - Tìm đến thư mục dự án và chạy Main.py
---

Liên hệ
Người thực hiện: Hoàng Anh Tú

Email: hoangtu.dainam@gmail.com

GitHub: [https://github.com/HoangAnhTu-thapbat/Nhan_dien_ky_hieu_tay/](https://github.com/HoangAnhTu-thapbat/Nhan_dien_ky_hieu_tay/)

Khoa: Khoa Công Nghệ Thông Tin, Trường Đại học Đại Nam

