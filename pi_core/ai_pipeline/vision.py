import cv2
import logging

try:
    from ultralytics import YOLO
    HAS_YOLO = True
except ImportError:
    HAS_YOLO = False

class VisionPipeline:
    def __init__(self, config: dict):
        self.model_path = config.get("model_path", "yolov8n.pt")
        self.confidence_threshold = config.get("confidence_threshold", 0.5)
        self.model = None
        
        if HAS_YOLO:
            try:
                self.model = YOLO(self.model_path)
                logging.info(f"YOLO model loaded: {self.model_path}")
            except Exception as e:
                logging.error(f"Failed to load YOLO model: {e}")

    def process_frame(self, frame):
        if frame is None:
            return None, []
            
        detections = []
        out_frame = frame.copy()
        
        if self.model:
            results = self.model(frame, verbose=False)
            for r in results:
                boxes = r.boxes
                for box in boxes:
                    conf = float(box.conf[0])
                    if conf >= self.confidence_threshold:
                        cls_id = int(box.cls[0])
                        class_name = self.model.names[cls_id]
                        
                        # Bounding box
                        x1, y1, x2, y2 = map(int, box.xyxy[0])
                        detections.append({
                            "class": class_name,
                            "confidence": conf,
                            "bbox": (x1, y1, x2, y2)
                        })
                        
                        # Draw on frame
                        cv2.rectangle(out_frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                        cv2.putText(out_frame, f"{class_name} {conf:.2f}", (x1, y1 - 10),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                                    
        return out_frame, detections
