import os
import sys
import math
import time
import cv2
import torch
import numpy as np
import torch.backends.cudnn as cudnn
from pathlib import Path
 
YOLOV7_DIR = Path(__file__).resolve().parent / "object_detector"
sys.path.append(str(YOLOV7_DIR))
 
from models.experimental import attempt_load
from utils.datasets import letterbox
from utils.general import non_max_suppression, scale_coords, xyxy2xywh
from utils.plots import plot_one_box
from utils.torch_utils import time_synchronized  

 
 
class objectDetector:
    def __init__(self, device: str = None, weights: str = None, img_size: int = 640):
        self.device = torch.device(device if device else ("cuda" if torch.cuda.is_available() else "cpu"))
        self.img_size = img_size
        weights_path = weights or (Path(__file__).resolve().parent / "weights" / "bestfire.pt")

        print(f"[INFO] Loading fire-smoke model from {weights_path} on {self.device}...")
        self.model = attempt_load(str(weights_path), map_location=self.device).to(self.device)

        if self.device.type == "cuda":
            self.model.half()
            self.model.float()
            dummy = torch.zeros(1, 3, self.img_size, self.img_size, device=self.device, dtype=torch.half)
            with torch.inference_mode():
                _ = self.model(dummy)
            del dummy
            torch.cuda.empty_cache()
            print("[INFO] Fire-Smoke Model warmed up on GPU")
        else:
            self.model.float()

        self.model.eval()
        self.names = self.model.module.names if hasattr(self.model, "module") else self.model.names
        self.loaded = True
        print(f"[INFO] Model loaded with classes: {self.names}")

    def preprocess(self, img):
        img = letterbox(img, new_shape=(self.img_size, self.img_size), stride=32, auto=True)[0]
        img = img[:, :, ::-1].transpose(2, 0, 1)
        img = np.ascontiguousarray(img)
        im = torch.from_numpy(img).to(self.device)
        im = im.float() / 255.0
        if im.ndimension() == 3:
            im = im.unsqueeze(0)
        if self.device.type == "cuda":
            pass
        return im

    def predict_tensor(self, tensor, conf_thres=0.25, iou_thres=0.45):
        with torch.no_grad():
            pred = self.model(tensor)[0]
        return non_max_suppression(pred, conf_thres=conf_thres, iou_thres=iou_thres)

    def predict_image(self, img_path, show=True):
        frame = cv2.imread(img_path)
        im = self.preprocess(frame)
        dets = self.predict(im)

        for det in dets:
            if len(det):
                det[:, :4] = scale_coords(im.shape[2:], det[:, :4], frame.shape).round()
                for *xyxy, conf, cls_id in det:
                    label = f"{self.names[int(cls_id)]} {float(conf):.2f}"
                    plot_one_box(xyxy, frame, label=label, color=(0, 255, 0), line_thickness=2)

        if show:
            cv2.imshow("Image Detection", frame)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
        return dets

    def predict_video(self, video_path, output_path=None, show=True, conf_thres=0.25, iou_thres=0.45):
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            raise RuntimeError(f"[ERROR] Cannot open video: {video_path}")

        if output_path:
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            fps = int(cap.get(cv2.CAP_PROP_FPS))
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
        else:
            out = None

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            im = self.preprocess(frame)
            dets = self.predict(im, conf_thres, iou_thres)

            for det in dets:
                if len(det):
                    det[:, :4] = scale_coords(im.shape[2:], det[:, :4], frame.shape).round()
                    for *xyxy, conf, cls_id in det:
                        label = f"{self.names[int(cls_id)]} {float(conf):.2f}"
                        plot_one_box(xyxy, frame, label=label, color=(0, 255, 0), line_thickness=2)

            if show:
                cv2.imshow("Video Detection", frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

            if out:
                out.write(frame)

        cap.release()
        if out:
            out.release()
        cv2.destroyAllWindows()
        print(f"[INFO] Video processing complete. Saved at {output_path if output_path else '[no save]'}")