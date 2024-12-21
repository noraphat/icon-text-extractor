#pip install PyQt5
#pip install PyQt5-tools
#pip install pillow
#pip install opencv-python
#pip install opencv-python-headless
#pip install pytesseract
#brew install tesseract


import sys
import cv2
import pytesseract
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QFileDialog, QLabel, QPushButton, QVBoxLayout, QWidget, QScrollArea, QTextEdit
)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
import numpy as np


class IconTextExtractorApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Icon and Text Extractor")
        self.setGeometry(100, 100, 1000, 800)

        # UI Elements
        self.label = QLabel("Upload an image to extract icons and text")
        self.label.setAlignment(Qt.AlignCenter)

        self.upload_button = QPushButton("Upload Image")
        self.upload_button.clicked.connect(self.upload_image)

        self.exit_button = QPushButton("Exit Application")
        self.exit_button.clicked.connect(self.close_app)

        self.result_label = QLabel("Processed Image:")
        self.result_label.setAlignment(Qt.AlignCenter)
        self.result_label.setVisible(False)

        self.text_label = QTextEdit()
        self.text_label.setReadOnly(True)
        self.text_label.setVisible(False)

        self.log_box = QTextEdit()
        self.log_box.setReadOnly(True)
        self.log_box.setVisible(False)

        self.scroll_area = QScrollArea()
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setScaledContents(True)
        self.scroll_area.setWidget(self.image_label)
        self.scroll_area.setVisible(False)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.upload_button)
        layout.addWidget(self.exit_button)
        layout.addWidget(self.result_label)
        layout.addWidget(self.scroll_area)
        layout.addWidget(QLabel("Extracted Text:"))
        layout.addWidget(self.text_label)
        layout.addWidget(QLabel("Log Messages:"))
        layout.addWidget(self.log_box)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def upload_image(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Choose Image", "", "Images (*.png *.jpg *.jpeg *.bmp)")
        if file_path:
            self.label.setText("Processing the image, please wait...")
            processed_image_path, extracted_text, log_messages = self.process_image(file_path)
            self.display_results(processed_image_path, extracted_text, log_messages)
        else:
            self.label.setText("No file selected.")

    def process_image(self, file_path):
        print(f"Processing file: {file_path}")
        img = cv2.imread(file_path)

        # Convert to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Threshold to detect shapes
        _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)


        # Extract Text using Tesseract OCR with Thai and English language support
        custom_config = r'--oem 3 --psm 4 -l tha+eng'
        extracted_text = pytesseract.image_to_string(img, config=custom_config)
        print("Extracted Text:\n", extracted_text)

        # Cleaning the text (optional)
        def clean_text(text):
            return ''.join(char for char in text if char.isalnum() or char.isspace())
        extracted_text = clean_text(extracted_text)

        # Find contours for icons
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        icon_img = img.copy()
        icon_count = 0
        log_messages = []

        for contour in contours:
            # Approximate bounding box
            x, y, w, h = cv2.boundingRect(contour)
            area = cv2.contourArea(contour)

            # Filter small areas
            if area > 500:
                # Check if the shape is circular
                (cx, cy), radius = cv2.minEnclosingCircle(contour)
                circularity = 4 * np.pi * (area / (cv2.arcLength(contour, True) ** 2))
                if 0.7 < circularity < 1.2:  # Circle
                    cv2.circle(icon_img, (int(cx), int(cy)), int(radius), (0, 255, 0), 2)
                    cropped_icon = img[y:y+h, x:x+w]
                else:  # Rectangle
                    cv2.rectangle(icon_img, (x, y), (x+w, y+h), (255, 0, 0), 2)
                    cropped_icon = img[y:y+h, x:x+w]

                # Save cropped icon
                icon_filename = f"icon_{icon_count}.png"
                cv2.imwrite(icon_filename, cropped_icon)
                log_messages.append(f"Saved icon: {icon_filename}")
                print(f"Saved icon: {icon_filename}")
                icon_count += 1

        # Save the processed image
        processed_image_path = "processed_image.png"
        cv2.imwrite(processed_image_path, icon_img)

        return processed_image_path, extracted_text, log_messages

    def display_results(self, processed_image_path, extracted_text, log_messages):
        # Display processed image
        pixmap = QPixmap(processed_image_path)
        if not pixmap.isNull():
            self.result_label.setVisible(True)
            self.scroll_area.setVisible(True)
            self.image_label.setPixmap(pixmap)
            self.scroll_area.setWidgetResizable(True)
        else:
            print("Failed to load processed image.")

        # Display extracted text
        self.text_label.setVisible(True)
        self.text_label.setPlainText(extracted_text)

        # Display log messages
        self.log_box.setVisible(True)
        self.log_box.setPlainText("\n".join(log_messages))

        self.label.setText("Upload another image or exit the application.")

    def close_app(self):
        print("Exiting application...")
        QApplication.quit()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = IconTextExtractorApp()
    main_window.show()
    sys.exit(app.exec_())
