import cv2

# Mở camera (0 là mặc định)
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Không mở được camera")
    exit()

# Lấy các thông tin cấu hình
width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
fps = cap.get(cv2.CAP_PROP_FPS)  # FPS lý thuyết
format_code = int(cap.get(cv2.CAP_PROP_FORMAT))  # Mã định dạng
brightness = cap.get(cv2.CAP_PROP_BRIGHTNESS)
contrast = cap.get(cv2.CAP_PROP_CONTRAST)
saturation = cap.get(cv2.CAP_PROP_SATURATION)

# In ra cấu hình
print("📷 Cấu hình Camera hiện tại:")
print(f"🔹 Độ phân giải: {int(width)} x {int(height)}")
print(f"🔹 FPS (lý thuyết): {fps}")
print(f"🔹 Format code: {format_code}")
print(f"🔹 Độ sáng (brightness): {brightness}")
print(f"🔹 Tương phản (contrast): {contrast}")
print(f"🔹 Độ bão hòa (saturation): {saturation}")

# Đóng camera
cap.release()
