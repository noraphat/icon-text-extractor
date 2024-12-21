
# 🎨 Icon and Text Extractor

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python&logoColor=white)
![PyQt5](https://img.shields.io/badge/PyQt5-GUI-green?logo=qt)
![OpenCV](https://img.shields.io/badge/OpenCV-ImageProcessing-orange?logo=opencv)

Icon and Text Extractor is a simple Python application that allows you to extract **icons** and **text** from images with ease. It uses PyQt5 for the user interface and OpenCV for image processing. Whether you're working with icons, circular shapes, rectangular shapes, or text, this project can handle it all!

---

## ✨ Features
- **Icon Detection**:
  - Detects both circular and rectangular icons.
  - Saves extracted icons into separate files.
- **Text Extraction**:
  - Extracts structured text using Tesseract OCR.
  - Handles multi-column and paragraph layouts.
- **Interactive GUI**:
  - Upload images and view results in a user-friendly interface.
  - Log messages to track saved icons and processing status.
- **Processed Image Display**:
  - Highlights detected icons with bounding boxes.

---

## 🛠️ Requirements
Ensure you have the following installed:
- **Python 3.8+**
- **PyQt5**
- **OpenCV**
- **Pytesseract**

---

## 🚀 Installation
### Step 1: Clone the repository
   ```bash
   git clone https://github.com/noraphat/icon-text-extractor.git
   cd icon-text-extractor
   ```

### Step 2: Install the required dependencies
   ```bash
   pip install -r requirements.txt
   ```

### Step 3: Install Tesseract OCR
#### macOS:
   ```bash
   brew install tesseract
   ```
#### Mac:
1. Ensure Tesseract OCR is installed on your system:
   - For macOS:
     ```bash
     brew install tesseract
     ```
2. Verify installation:
   ```bash
   tesseract --version
   ```
#### Windows:
1. Download Tesseract OCR from [Tesseract OCR Windows Installer](https://github.com/UB-Mannheim/tesseract/wiki).
2. Install Tesseract in a directory like `C:\Program Files\Tesseract-OCR`.
3. Add the Tesseract installation directory to your **System PATH**:
   - Open **Environment Variables**.
   - Under **System Variables**, find `Path` and click **Edit**.
   - Add the directory: `C:\Program Files\Tesseract-OCR`.
4. Verify installation:
   ```bash
   tesseract --version
   ```

5. Configure `pytesseract` in the script:
   Add this line to your Python script before using `pytesseract`:
   ```python
   pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
   ```

### Step 4: Run the application
   ```bash
   python icon_text_extractor.py
   ```

---

## 🎯 Usage
1. Open the application.
2. Click **Upload Image** to select an image.
3. View extracted icons and text in the GUI.
4. Check the **Log Messages** section for details about saved icons.
5. Click **Exit Application** to close the program.

---

## 📂 Project Structure
```plaintext
icon-text-extractor/
│
├── icon_text_extractor.py   # Main application script
├── processed_image.png      # Example of a processed image
├── icon_0.png               # Example extracted icon
├── README.md                # Project documentation
└── requirements.txt         # Python dependencies
```

---

## 🧑‍💻 Technologies Used
- **Python** for backend processing.
- **PyQt5** for GUI design.
- **OpenCV** for image and icon detection.
- **Tesseract OCR** for text extraction.

---

## 🛡️ License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## 🌟 Contributions
Contributions are welcome! Feel free to submit a pull request or open an issue to discuss improvements.

---

## 📧 Contact
If you have any questions or suggestions, feel free to reach out at **noraphat@gmail.com**.

---
