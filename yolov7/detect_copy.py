import argparse
import time
from pathlib import Path

import cv2
import torch
import torch.backends.cudnn as cudnn
from numpy import random

from models.experimental import attempt_load
from utils.datasets import LoadStreams, LoadImages
from utils.general import check_img_size, check_requirements, check_imshow, non_max_suppression, apply_classifier, \
    scale_coords, xyxy2xywh, strip_optimizer, set_logging, increment_path
from utils.plots import plot_one_box
from utils.torch_utils import select_device, load_classifier, time_synchronized, TracedModel

def detect_custom(source, weights='yolov7.pt', view_img=False, save_txt=False, save_img=False, img_size=640,
                  conf_thres=0.25, iou_thres=0.45, device='', classes=None, agnostic_nms=False, augment=False,
                  update=False, project='runs/detect', name='exp', exist_ok=False, no_trace=False):
    # The rest of your code remains the same, but without the argparse part.

    # Initialize
    set_logging()
    device = select_device(device)
    half = device.type != 'cpu'  # half precision only supported on CUDA

    # Load model
    model = attempt_load(weights, map_location=device)  # load FP32 model
    stride = int(model.stride.max())  # model stride
    img_size = check_img_size(img_size, s=stride)  # check img_size

    if no_trace:
        model = TracedModel(model, device, img_size)

    if half:
        model.half()  # to FP16

    # ... (the rest of your code)
    dataset=LoadImages(source, img_size=img_size,stride=stride)

    names = model.module.names if hasattr(model, 'module') else model.names
    colors = [[random.randint(0, 255) for _ in range(3)] for _ in names]
    # Run inference
    if device.type != 'cpu':
        model(torch.zeros(1, 3, img_size, img_size).to(device).type_as(next(model.parameters())))  # run once
    old_img_w = old_img_h = img_size
    old_img_b = 1

    t0 = time.time()
    for path, img, im0s, vid_cap in dataset:
        img = torch.from_numpy(img).to(device)
        img = img.half() if half else img.float()  # uint8 to fp16/32
        img /= 255.0  # 0 - 255 to 0.0 - 1.0
        if img.ndimension() == 3:
            img = img.unsqueeze(0)

    with torch.no_grad():   # Calculating gradients would cause a GPU memory leak
        pred = model(img, augment=augment)[0]

    pred = non_max_suppression(pred, conf_thres, iou_thres, classes=classes, agnostic=agnostic_nms) 
    for i, det in enumerate(pred):  # detections per image
        p, s, im0, frame = path, '', im0s, getattr(dataset, 'frame', 0)      
        # The rest of your code remains the same
    p = Path(p)  # to Path
    gn = torch.tensor(im0.shape)[[1, 0, 1, 0]]  # normalization gain whwh
    if len(det):
        # Rescale boxes from img_size to im0 size
        det[:, :4] = scale_coords(img.shape[2:], det[:, :4], im0.shape).round()

        # Print results
        for c in det[:, -1].unique():
            n = (det[:, -1] == c).sum()  # detections per class
            s += f"{n} {names[int(c)]}{'s' * (n > 1)}, "  # add to string
            if names[int(c)]=='bottle':
                if n>=1:
                    return n
        return 0

detect_custom(source='inference/images', weights='yolov7.pt', view_img=True, save_txt=True, save_img=True,
              img_size=640, conf_thres=0.25, iou_thres=0.45, device='', classes=None, agnostic_nms=False,
              augment=False, update=False, project='runs/detect', name='exp', exist_ok=False, no_trace=False)
