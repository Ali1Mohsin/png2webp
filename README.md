# png2webp (v1.0)

A lightweightdesktop application designed for efficient batch conversion of PNG images to the WebP format. 

一款轻量级的桌面应用程序，专为高效批量将 PNG 图像批量转换为 WebP 格式而设计。



## ✨ Key Features
- **Batch Processing**: Convert thousands of images by selecting a folder or specific multiple files.
- **Ultra-Large Image Support**: Successfully processes images exceeding 600M+ pixels (Decompression Bomb safe).
- **Intelligent Memory Management**: Active garbage collection to ensure stability during heavy workloads.
- **Adjustable Parameters**: Fine-tune compression quality (1-100) or toggle between Lossy and Lossless modes.
- **Clean UI**: A compact, modern interface built with `ttkbootstrap` and a professional "Flatly" theme.
- **Portable**: No installation required when used as a standalone EXE.

## 🛠 Tech Stack
- **Language**: Python 3.8+
- **Image Engine**: Pillow (PIL)
- **GUI Framework**: Tkinter & ttkbootstrap
- **Memory Optimization**: Python `gc` module

## 🚀 Getting Started

### Installation from Source
If you want to run the script directly:

1. **Clone the repository**:
   ```bash
   git clone [https://github.com/yourusername/png2webp.git](https://github.com/yourusername/png2webp.git)
   cd png2webp
   ```

2. **Install dependencies**:
   ```bash
   pip install Pillow ttkbootstrap
   ```

3. **Run the application**:
   ```bash
   python png2webp_gui.py
   ```

### Packaging to EXE (Windows)
To create a standalone executable that doesn't require Python to be installed:

1. **Install PyInstaller**:
   ```bash
   pip install pyinstaller
   ```

2. **Build the EXE**:
   ```bash
   pyinstaller --noconsole --onefile --collect-all ttkbootstrap --name "PNG_to_WebP_Converter_v1.0" png2webp_gui.py
   ```
The generated file will be located in the `dist/` folder.


## 📖 How to Use

1. **Select Source**: Click "文件" (Files) to select specific PNGs or "目录" (Folder) to scan an entire directory.

2. **Set Output**: Use "浏览" (Browse) to choose your destination folder.

3. **Configure**:

   * Slide "压缩质量" (Quality) to your desired level (integer only).

   * Enter a "文件名后缀" (Suffix) if you wish to distinguish the new files.

   * Enable "无损模式" (Lossless Mode) for pixel-perfect conversion (note: memory-intensive for massive files).

4. **Convert**: Click the "Start Conversion Task" button.

5. **Finish**: Once completed, the output folder will automatically open if the toggle is enabled.

## ⚠️ Important Notes

**Memory Usage**: For images over 500 megapixels, ensure your system has at least 16GB of RAM.

**Large Files**: Avoid "Lossless Mode" on extremely large files (e.g., 600M+ pixels) to prevent memory allocation errors.

## ⚖️ License

Distributed under the MIT License. See LICENSE for more information.


