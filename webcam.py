""" for use with python 3.10 """
from pathlib import Path
from ultralytics import YOLO
import cv2
import cvzone
from math import ceil

project_dir = Path(__file__).resolve().parent

#camera object :
cap = cv2.VideoCapture(str(project_dir / "videos" / "potatos.mp4"))  # for videos
# cap = cv2.VideoCapture(0) #for webcam
#camera window size :
cap.set(3, 1280)
cap.set(4, 720)

#model :
openvino_model_dir = project_dir / "yolov8n_openvino_model"
pt_model_file = project_dir / "best.pt"
if not pt_model_file.exists():
    pt_model_file = project_dir / "last.pt"

if openvino_model_dir.exists():
    model_path = openvino_model_dir
elif pt_model_file.exists():
    model_path = pt_model_file
else:
    raise FileNotFoundError(
        "No model found. Expected either 'yolov8n_openvino_model/' (OpenVINO export) "
        "or 'best.pt'/'last.pt' in the project folder."
    )

model = YOLO(str(model_path))

#classes
classNames = model.names

while True:
    success, img= cap.read()
    if not success:
        break
    infer_kwargs = {"stream": True, "imgsz": 320}
    if model_path == openvino_model_dir:
        infer_kwargs["device"] = "intel:gpu"  # OpenVINO device
    results = model(img, **infer_kwargs)
    for r in results:
        boxes = r.boxes
        for box in boxes:
            #bounding box coordinates :
            x1, y1, x2, y2 = box.xyxy[0]
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
            # cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 255), 3)# alternative for cvzone.cornerRect
            w, h = x2 - x1, y2 - y1
            cvzone.cornerRect(img, (x1, y1, w, h) )
            #confidence :
            conf = ceil(box.conf[0]*100)/100
            #class name :
            cls = int(box.cls[0])
            cvzone.putTextRect(img, f'{classNames[cls]} {conf}', (max(0, x1), max(35, y1)), scale=0.9, thickness=2)


    cv2.imshow("Image", img)
    cv2.waitKey(1)