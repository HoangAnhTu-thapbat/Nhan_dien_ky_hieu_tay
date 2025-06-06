import os

def count_images_in_all_subfolders(root_folder, image_extensions={'.png', '.jpg', '.jpeg'}):
    total_images = 0
    for dirpath, _, filenames in os.walk(root_folder):
        image_files = [f for f in filenames if os.path.splitext(f)[1].lower() in image_extensions]
        count = len(image_files)
        if count > 0:
            print(f"{dirpath}: {count} ảnh")
        total_images += count

    print(f"\n👉 Tổng số ảnh: {total_images}")
    return total_images

# Sử dụng
folder_path = "D:/testkyhieu"  # Sửa lại nếu đường dẫn khác
count_images_in_all_subfolders(folder_path)
