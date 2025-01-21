# Infinite_Storage_Glitcher

A Python-based tool for converting files to videos and back. This program leverages GPU acceleration and preserves metadata such as the creation and modification dates of the files.

---

## 📜 Description

## This program is currently only compatible with macOS on Apple M1/M2.

`Infinite_Storage_Glitcher` enables:
- **Convert file to video:** 
  - Files are converted into a black-and-white video.
  - The binary data of the file is stored in the frames of the video.
  - Metadata such as creation and modification dates are embedded in the video.

- **Reconstruct file from video:**
  - The program reads the frames from the video and reconstructs the original file.
  - Metadata is extracted from the video and applied to the file.

---

## 🛠️ Dependencies

### **System Requirements**
- **Python**: Version 3.10 (GPU Support requires this version).
- **MacOS**: With Apple Silicon (M1/M2) for GPU accleration.
- **FFmpeg**: Required for video processing.
- **Homebrew**: Package manager macOS
  
---
Install Homebrew for macOS from [here](https://brew.sh).
### **Python-Libraries**
The required libraries can be installed with the following command:

```bash
pip install numpy torch tqdm opencv-python
```
Install FFmpeg via Homebrew:
```bash
brew install ffmpeg
```

---

## 🚀 Installation & Execution
1.	Clone the repository:

```bash
git clone https://github.com/user1334/Infinite_Storage_Glitcher.git
cd Infinite_Storage_Glitcher
```
2.	Start the program:

```bash
python3 converter.py
```

3.	Select an option:
  - 1: Convert file to video.
  - 2: Reconstruct file from video.

4.	Follow the prompts:
	
  - Option 1 (File → Video):
  - Input: Path/to/file.example.
  - Output: Path to the target video.
  - Option 2 (Video → File):
  - Input: Path/to/file.example.
  - Output: Path to the target file.

## 📋 Examples

Convert file to video:

```bash
python3 converter.py
Enter 1 or 2: 1
Enter the path to the desired file: /path/to/file.txt
Enter the path for the output video (without .mov): /path/to/video
```

Reconstruct file from video:

```bash
python3 converter.py
Enter 1 or 2: 2
Enter the path to the video: /path/to/video.mov
Enter the path for the output file: /path/to/reconstructed/file.txt
```

## ✨ Features
  - GPU Acceleration: Utilizes the Metal API on macOS for fast processing.
  - Metadata Preservation: Maintains creation and modification dates between file and video.
  - Efficient Processing: Supports large files with optimized memory management.
  - Progress Indicator: Displays progress during video and file processing.

## 🧪 Future Improvements
  - Support for additional platforms and GPUs.
  - Support for large files on MacBooks with 8 GB RAM.



