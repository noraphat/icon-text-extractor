import os
import cv2
import pytesseract

# กำหนด Path ของโฟลเดอร์ที่เก็บไอคอน
icon_folder = "./"


def is_text_image(image_path):
    """ตรวจสอบว่าไฟล์เป็นภาพที่มีข้อความหรือไม่"""
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # ใช้ Tesseract OCR ตรวจสอบข้อความ
    text = pytesseract.image_to_string(gray, config="--psm 6")
    print(f"Extracted Text from {image_path}: {text.strip()}")

    # ถ้าพบข้อความภาษาอังกฤษหรือตัวเลข ให้ถือว่าเป็น "text image"
    if any(char.isalnum() for char in text):
        return True
    return False

def clean_icon_folder(folder_path):
    """ลบไฟล์ที่ไม่ใช่ไอคอนจริง"""
    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        if os.path.isfile(file_path):
            try:
                if is_text_image(file_path):
                    print(f"Deleting {file_path} (Detected as Text Image)")
                    os.remove(file_path)
                else:
                    print(f"Keeping {file_path} (Detected as Icon)")
            except Exception as e:
                print(f"Error processing {file_path}: {e}")

# เรียกใช้งานฟังก์ชัน
clean_icon_folder(icon_folder)
