import sys
import os
import shutil
import cv2
import pytesseract
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QFileDialog, QLabel, QPushButton, QVBoxLayout, QWidget, QScrollArea, QTextEdit, QHBoxLayout, QVBoxLayout
)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
import numpy as np
from datetime import datetime


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

        self.thumbnail_area = QScrollArea()
        self.thumbnail_area.setVisible(False)
        self.thumbnail_widget = QWidget()
        self.thumbnail_layout = QHBoxLayout()
        self.thumbnail_widget.setLayout(self.thumbnail_layout)
        self.thumbnail_area.setWidget(self.thumbnail_widget)
        self.thumbnail_area.setWidgetResizable(True)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.upload_button)
        layout.addWidget(self.exit_button)
        layout.addWidget(self.result_label)
        layout.addWidget(self.scroll_area)
        layout.addWidget(QLabel("Extracted Text:"))
        layout.addWidget(self.text_label)
        layout.addWidget(QLabel("Extracted Icons:"))
        layout.addWidget(self.thumbnail_area)
        layout.addWidget(QLabel("Log Messages:"))
        layout.addWidget(self.log_box)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def upload_image(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Choose Image", "", "Images (*.png *.jpg *.jpeg *.bmp)")
        if file_path:
            self.label.setText("Processing the image, please wait...")
            processed_image_path, extracted_text, log_messages, icon_paths = self.process_image(file_path)
            self.display_results(processed_image_path, extracted_text, log_messages, icon_paths)
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
        icon_paths = []

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
                icon_paths.append(icon_filename)
                log_messages.append(f"Saved icon: {icon_filename}")
                print(f"Saved icon: {icon_filename}")
                icon_count += 1

        # Save the processed image
        processed_image_path = "processed_image.png"
        cv2.imwrite(processed_image_path, icon_img)

        return processed_image_path, extracted_text, log_messages, icon_paths

    def display_results(self, processed_image_path, extracted_text, log_messages, icon_paths):
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

        # Display thumbnails of extracted icons
        self.thumbnail_layout.setAlignment(Qt.AlignLeft)
        for icon_path in icon_paths:
            thumbnail_widget = QWidget()
            thumbnail_layout = QVBoxLayout()
            thumbnail_widget.setLayout(thumbnail_layout)

            thumbnail_label = QLabel()
            pixmap = QPixmap(icon_path).scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            thumbnail_label.setPixmap(pixmap)

            close_button = QPushButton("✖")
            close_button.setFixedSize(20, 20)
            close_button.clicked.connect(lambda _, path=icon_path, widget=thumbnail_widget: self.remove_icon(path, widget))

            move_button = QPushButton("Move")
            move_button.setFixedSize(50, 20)
            move_button.clicked.connect(lambda _, path=icon_path: self.move_icon(path))

            thumbnail_layout.addWidget(thumbnail_label)
            thumbnail_layout.addWidget(close_button, alignment=Qt.AlignCenter)
            thumbnail_layout.addWidget(move_button, alignment=Qt.AlignCenter)

            self.thumbnail_layout.addWidget(thumbnail_widget)

        self.thumbnail_area.setVisible(True)

        # Display log messages
        self.log_box.setVisible(True)
        self.log_box.setPlainText("\n".join(log_messages))

        self.label.setText("Upload another image or exit the application.")

    def remove_icon(self, icon_path, thumbnail_widget):
        try:
            if os.path.exists(icon_path):
                os.remove(icon_path)
                log_message = f"Removed icon file: {icon_path}"
            else:
                log_message = f"File not found: {icon_path}"

            self.log_box.append(log_message)
            print(log_message)

        except Exception as e:
            log_message = f"Error removing file {icon_path}: {str(e)}"
            self.log_box.append(log_message)
            print(log_message)

        self.thumbnail_layout.removeWidget(thumbnail_widget)
        thumbnail_widget.deleteLater()

    def move_icon(self, icon_path):
        destination_path = QFileDialog.getExistingDirectory(self, "Select Destination Folder")
        if destination_path:
            try:
                timestamp = datetime.now().strftime("%Y%m%d%H%M%S%f")
                file_extension = os.path.splitext(icon_path)[-1]
                new_file_name = f"icon_{timestamp}{file_extension}"
                destination_file = os.path.join(destination_path, new_file_name)
                shutil.move(icon_path, destination_file)
                log_message = f"Moved icon file to: {destination_file}"
                self.log_box.append(log_message)
                print(log_message)
            except Exception as e:
                log_message = f"Error moving file {icon_path}: {str(e)}"
                self.log_box.append(log_message)
                print(log_message)
        else:
            self.log_box.append("Move operation cancelled.")

    def close_app(self):
        print("Exiting application...")
        QApplication.quit()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = IconTextExtractorApp()
    main_window.show()
    sys.exit(app.exec_())
