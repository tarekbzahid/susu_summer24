# SUSU Summer 2024 - Industrial AI & Computer Vision Platform

A comprehensive Summer 2024 research and development project integrating multiple AI/ML technologies for industrial automation, video surveillance, and human-computer interaction. This platform combines real-time video stream monitoring, hand gesture detection, object detection for factory environments, and conversational AI capabilities.

## Table of Contents

- [Overview](#overview)
- [Key Features](#key-features)
- [Project Structure](#project-structure)
- [Technologies Used](#technologies-used)
- [Installation](#installation)
- [Usage](#usage)
  - [RTSP Stream Monitoring](#rtsp-stream-monitoring)
  - [Video Recording](#video-recording)
  - [Hand Landmark Detection](#hand-landmark-detection)
  - [Object Detection](#object-detection)
  - [Chatbot](#chatbot)
- [Configuration](#configuration)
- [Models](#models)
- [Contributing](#contributing)

---

## Overview

This project serves as an integrated platform for industrial automation and surveillance, combining:

- **Real-time Video Surveillance**: Monitor multiple RTSP camera streams simultaneously with health checks and FPS metrics
- **Hand Gesture Recognition**: Extract and track hand landmarks for gesture-based interaction
- **Industrial Object Detection**: Detect and classify machines and objects in factory environments using state-of-the-art YOLO models
- **Conversational AI**: GPT-2 based chatbot for natural language interaction

The system is designed for scalability and can process multiple video streams concurrently while performing real-time AI inference.

---

## Key Features

### Video Surveillance & Streaming
- Multi-stream RTSP monitoring with connection status checks
- Automated video recording with time-based scheduling
- Real-time FPS calculation and stream health metrics
- Support for 2x2 grid display of multiple feeds

### Hand Gesture Detection
- MediaPipe-based hand landmark detection (21 points per hand)
- Support for tracking up to 2 hands simultaneously
- Export hand landmarks to CSV format with XYZ coordinates
- Real-time hand tracking across multiple RTSP streams

### Object Detection & Segmentation
- Factory-specific machine and object detection
- Support for YOLOv5 and YOLOv8 models (nano, small, medium variants)
- Semantic segmentation capabilities
- Custom dataset creation and training pipelines
- Real-time object tracking

### AI Chatbot
- GPT-2 based conversational interface
- Natural language processing capabilities
- PyTorch and Transformers implementation

---

## Project Structure

```
susu_summer24/
│
├── haigs_app/                      # Main application for hand detection & RTSP streaming
│   ├── stream.py                   # Monitor RTSP streams and calculate FPS
│   ├── record.py                   # Record RTSP streams with scheduling
│   ├── extract_hand_landmarks.py   # Extract hand landmarks from videos
│   ├── infer.py                    # YOLO inference on images
│   ├── feeds.txt                   # RTSP camera feed URLs configuration
│   ├── requirements.txt            # Python dependencies
│   ├── trained_model.pt            # Pre-trained hand detection model
│   └── readme_stream.txt           # Setup instructions
│
├── object_detection/               # Object detection module
│   ├── train.ipynb                 # Model training pipeline
│   ├── obj_detect.ipynb            # Object detection inference
│   ├── infer.ipynb                 # Inference demonstrations
│   ├── rt_ob_track.ipynb           # Real-time object tracking
│   ├── make_ds.ipynb               # Dataset creation utilities
│   ├── sam2.ipynb                  # Segment Anything Model 2
│   ├── yolov5su.pt                 # YOLOv5 small-ultralytics model (18.6 MB)
│   ├── yolov8n.pt                  # YOLOv8 nano model (6.5 MB)
│   ├── yolov8s.pt                  # YOLOv8 small model (22.6 MB)
│   ├── yolov8n-seg.pt              # YOLOv8 nano segmentation model (7 MB)
│   ├── factory_dataset/            # Training datasets
│   │   └── yolo_dataset/
│   │       ├── dataset_v0/         # Initial dataset version
│   │       ├── dataset_semantic/   # Semantic segmentation dataset
│   │       └── frames/             # Raw training frames
│   └── runs/                       # Training results and weights
│
├── video_streaming/                # Video streaming and hand tracking tests
│   ├── stream_test_with_hand.py    # Multi-stream hand tracking (2x2 grid)
│   ├── hand_tracking.ipynb         # Hand tracking experiments
│   ├── rtsp_stream_test.py         # RTSP connectivity testing
│   └── scratch*.py                 # Development/testing scripts
│
└── chat_bot/                       # Chatbot module
    └── chatbot.ipynb               # GPT-2 based chatbot implementation
```

---

## Technologies Used

| Component | Technologies |
|-----------|-------------|
| **Programming Language** | Python 3.x |
| **Computer Vision** | OpenCV, MediaPipe, Ultralytics (YOLOv5/v8) |
| **Deep Learning** | PyTorch, TensorFlow/Keras |
| **NLP** | Transformers (GPT-2) |
| **Video Processing** | VLC, OpenCV VideoCapture |
| **Data Science** | NumPy, Pandas, Matplotlib |
| **Development** | Jupyter Notebook |

---

## Installation

### Prerequisites

- Python 3.8 or higher
- VLC Media Player (for RTSP streaming)
- CUDA-compatible GPU (recommended for real-time inference)

### Step 1: Clone the Repository

```bash
git clone https://github.com/tarekbzahid/susu_summer24.git
cd susu_summer24
```

### Step 2: Install Dependencies

For the main HAIGS application:

```bash
cd haigs_app
pip install -r requirements.txt
```

For object detection (install Ultralytics YOLO):

```bash
pip install ultralytics torch torchvision
```

For the chatbot:

```bash
pip install transformers torch
```

### Step 3: Install VLC

**Windows:**
- Download and install from [VLC official website](https://www.videolan.org/vlc/)
- Default installation path: `C:\Program Files\VideoLAN\VLC`

**Linux:**
```bash
sudo apt-get update
sudo apt-get install vlc
```

**macOS:**
```bash
brew install vlc
```

---

## Usage

### RTSP Stream Monitoring

Monitor multiple RTSP camera streams and calculate their frame rates:

```bash
cd haigs_app
python stream.py --feeds_file feeds.txt --refresh_time_min 10
```

**Parameters:**
- `--feeds_file`: Path to the file containing RTSP stream URLs (default: `feeds.txt`)
- `--refresh_time_min`: Refresh interval in minutes for checking stream status (default: 10)

**Controls:**
- Press `q` to exit the program

**Output:**
- Active stream status (connected/disconnected)
- Real-time FPS for each active stream
- Connection health metrics

### Video Recording

Record RTSP streams to MP4 files with optional time-based scheduling:

```bash
cd haigs_app
python record.py --feeds_file feeds.txt
```

**Features:**
- Automatic recording of all active RTSP streams
- Time-based scheduling (configure non-recording periods)
- MP4 output format with H.264 codec
- Separate files for each camera feed

### Hand Landmark Detection

Extract hand landmarks from video files:

```bash
cd haigs_app
python extract_hand_landmarks.py --input_video path/to/video.mp4 --output_csv hand_landmarks.csv
```

**Features:**
- Detects up to 2 hands per frame
- Exports 21 landmarks per hand (X, Y, Z coordinates)
- CSV output format for easy data analysis
- MediaPipe-based detection for high accuracy

**Real-time Multi-Stream Hand Tracking:**

```bash
cd video_streaming
python stream_test_with_hand.py
```

Displays a 2x2 grid of RTSP streams with real-time hand landmark overlay.

### Object Detection

#### Training a Model

Open and run the training notebook:

```bash
cd object_detection
jupyter notebook train.ipynb
```

#### Running Inference

Single image inference:

```bash
cd haigs_app
python infer.py --image path/to/image.jpg --model yolov8n.pt --conf 0.5
```

**For interactive inference and real-time tracking:**

```bash
cd object_detection
jupyter notebook obj_detect.ipynb  # For batch inference
jupyter notebook rt_ob_track.ipynb # For real-time tracking
```

### Chatbot

Launch the GPT-2 based chatbot:

```bash
cd chat_bot
jupyter notebook chatbot.ipynb
```

The chatbot uses pre-trained GPT-2 models from Hugging Face Transformers for natural language generation.

---

## Configuration

### RTSP Feed Configuration

Edit `haigs_app/feeds.txt` to add or modify camera feeds:

```
feed1:rtsp://username:password@192.168.1.127:554/live/ch1
feed2:rtsp://username:password@192.168.1.174:554/live/ch1
feed3:rtsp://username:password@192.168.1.123:554/live/ch1
```

**Format:**
```
stream_name:rtsp://username:password@ip_address:port/live/channel
```

### Model Configuration

Pre-trained models are located in their respective directories:

- **Hand Detection**: `haigs_app/trained_model.pt`
- **Object Detection**: `object_detection/yolov8*.pt`

To use a different model, specify the path when running inference scripts.

---

## Models

### Available Pre-trained Models

| Model | Size | Purpose | Location |
|-------|------|---------|----------|
| YOLOv8 Nano | 6.5 MB | Fast object detection | `object_detection/yolov8n.pt` |
| YOLOv8 Small | 22.6 MB | Balanced accuracy/speed | `object_detection/yolov8s.pt` |
| YOLOv5 Small-U | 18.6 MB | Ultralytics variant | `object_detection/yolov5su.pt` |
| YOLOv8 Nano Seg | 7 MB | Instance segmentation | `object_detection/yolov8n-seg.pt` |
| Hand Detection | - | Hand landmark detection | `haigs_app/trained_model.pt` |

### Dataset Information

The project includes factory-specific datasets for training:

- **Dataset V0**: Initial COCO-style annotated dataset
- **Semantic Dataset**: Semantic segmentation annotations
- **Machine Detection Dataset**: Factory machine classification
- **Augmented Dataset**: Data augmentation results in `aug_folder/`

Dataset metadata and class information are stored in `notes.json` files within each dataset directory.

---

## System Requirements

### Minimum Requirements
- **CPU**: Intel Core i5 or equivalent
- **RAM**: 8 GB
- **Storage**: 10 GB free space
- **OS**: Windows 10, Ubuntu 18.04+, macOS 10.14+

### Recommended Requirements
- **CPU**: Intel Core i7 or AMD Ryzen 7
- **RAM**: 16 GB or more
- **GPU**: NVIDIA GPU with 6GB+ VRAM (for real-time inference)
- **Storage**: 20 GB free space (SSD recommended)
- **Network**: Stable network connection for RTSP streaming

---

## Troubleshooting

### RTSP Connection Issues
- Verify camera IP addresses and credentials in `feeds.txt`
- Ensure cameras are powered on and connected to the network
- Check firewall settings to allow RTSP traffic (port 554)
- Confirm VLC is properly installed and accessible

### Model Inference Issues
- Ensure CUDA is installed for GPU acceleration
- Verify model files are not corrupted (check file sizes)
- Reduce batch size if encountering out-of-memory errors
- Update Ultralytics: `pip install --upgrade ultralytics`

### Hand Detection Issues
- Ensure adequate lighting in the video source
- Verify MediaPipe installation: `pip install --upgrade mediapipe`
- Check that input video is in a supported format (MP4, AVI, MOV)

---

## Performance Notes

- **Multi-stream Processing**: The system can handle 4-8 simultaneous RTSP streams on recommended hardware
- **Inference Speed**:
  - YOLOv8 Nano: ~100 FPS on GPU, ~20 FPS on CPU
  - YOLOv8 Small: ~60 FPS on GPU, ~10 FPS on CPU
  - Hand Detection: ~30 FPS on GPU, ~8 FPS on CPU
- **Recording**: No significant performance impact when recording up to 4 streams simultaneously

---

## Future Enhancements

- Integration of all modules into a unified dashboard
- REST API for remote access and control
- WebSocket support for real-time streaming
- Database integration for analytics and historical data
- Alert system for anomaly detection
- Mobile application for remote monitoring

---

## Contributing

Contributions are welcome! Please follow these guidelines:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## Acknowledgments

- **MediaPipe** by Google for hand landmark detection
- **Ultralytics** for YOLO implementations
- **Hugging Face** for Transformers library
- **VLC Media Player** for RTSP streaming capabilities

---

## Contact

For questions or support, please open an issue on the [GitHub repository](https://github.com/tarekbzahid/susu_summer24).

---

**Project Status**: Active Development (Summer 2024)

**Last Updated**: January 2026
