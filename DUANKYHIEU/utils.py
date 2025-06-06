import json
import os

# Hàm load label map (nếu bạn lưu ra file json)
def load_label_map(path="label_map.json"):
    if not os.path.exists(path):
        raise FileNotFoundError(f"Không tìm thấy file label map: {path}")
    with open(path, 'r', encoding='utf-8') as f:
        label_map = json.load(f)
    return label_map

# Hàm chuyển telex sang tiếng Việt (đơn giản, mẫu)
def telex_to_vietnamese(telex_str):
    # Ví dụ demo: Bạn cần code theo quy tắc telex của bạn
    # Đây là chỗ bạn viết code logic chuyển đổi
    # Hoặc import từ module xử lý của bạn nếu đã có
    return telex_str  # tạm thời trả về nguyên gốc

# Hàm ghi log (nếu muốn)
def write_log(message, filename="app.log"):
    with open(filename, 'a', encoding='utf-8') as f:
        f.write(message + "\n")
