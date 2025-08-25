import cv2
import numpy as np
import os
import time


def print_image_information(image):
    
    if image is None:
        print("Error: Image is None. Make sure 'lena.png' is in this folder.")
        return

    shape = image.shape
    if len(shape) == 2:  # grayscale fallback
        height, width = shape
        channels = 1
    else:
        height, width, channels = shape

    print(f"Height: {height}")
    print(f"Width: {width}")
    print(f"Channels: {channels}")
    print(f"Size: {image.size}")     # total number of elements
    print(f"Data Type: {image.dtype}")


def get_camera_info(cam_index=0, warmup_frames=5, fps_sample_frames=60):
    
    
    cap = cv2.VideoCapture(cam_index, cv2.CAP_DSHOW)

    if not cap.isOpened():
        raise RuntimeError("Could not open camera. Is it connected or used by another app?")

    
    for _ in range(warmup_frames):
        cap.read()

    
    width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    fps = cap.get(cv2.CAP_PROP_FPS)


    ret, frame = cap.read()
    if ret and (width <= 0 or height <= 0):
        h, w = frame.shape[:2]
        width, height = float(w), float(h)

    
    if not fps or fps < 1:
        frames = 0
        start = time.time()
        while frames < fps_sample_frames:
            ok, _ = cap.read()
            if not ok:
                break
            frames += 1
        elapsed = time.time() - start
        if elapsed > 0:
            fps = frames / elapsed
        else:
            fps = 0.0

    cap.release()
    return float(fps), float(height), float(width)

def save_camera_info_txt(out_path="solutions/camera_outputs.txt"):
    
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    try:
        fps, height, width = get_camera_info()
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(f"fps: {fps:.2f}\n")
            f.write(f"height: {height:.0f}\n")
            f.write(f"width: {width:.0f}\n")
        print(f"Camera information saved to {out_path}")
    except Exception as e:
        # Still create a file indicating the error (so you can commit something)
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(f"Error accessing camera: {e}\n")
        print(f"Camera access failed, wrote error to {out_path}")


if __name__ == "__main__":
   
    img_path = "lena-1.png"
    img = cv2.imread(img_path)
    print_image_information(img)  # <-- Take a screenshot of this console output (Step IV)

    
    save_camera_info_txt("solutions/camera_outputs.txt")
