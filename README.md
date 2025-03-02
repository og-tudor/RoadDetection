# Pothole Detection System

## How to Run the Model

- **Run on an Image:**

  ```bash
  python detect.py --weights runs/train/exp2/weights/best.pt --img 416 --conf 0.25 --source path/to/your/image.jpg --max-det 20
- **Run on a Video:**

  ```bash
  python detect.py --weights runs/train/exp2/weights/best.pt --img 416 --conf 0.25 --source path/to/your/video.mp4 --max-det 20
- **Run on Webcam:**

  ```bash
  python detect.py --weights runs/train/exp2/weights/best.pt --img 416 --conf 0.25 --source 0 --max-det 20
 