import cv2

# Mở video
cap = cv2.VideoCapture(1)

# Kiểm tra nếu video đã mở thành công
if not cap.isOpened():
    print("Không thể mở video")
    exit()

# Lấy độ phân giải của video (width và height)
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

print(f"Độ phân giải của video là: {width}x{height}")

# Đọc và hiển thị video
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Hiển thị video
    cv2.imshow("Video", frame)

    # Kiểm tra để thoát khi nhấn 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Giải phóng tài nguyên
cap.release()
cv2.destroyAllWindows()
