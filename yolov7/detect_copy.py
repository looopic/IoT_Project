from pathlib import Path

import torch
import torch.backends.cudnn as cudnn


from models.experimental import attempt_load
from utils.datasets import LoadStreams, LoadImages
from utils.general import check_img_size, set_logging,  non_max_suppression,scale_coords
from utils.torch_utils import select_device,  TracedModel


def detect_objects(source, weights, img_size=640, conf_thres=0.25, iou_thres=0.45, device='', classes=None, agnostic_nms=False, augment=False, no_trace=False):

    source = Path(source)

    set_logging()
    device = select_device(device)
    half = device.type != 'cpu'

    model = attempt_load(weights, map_location=device)
    stride = int(model.stride.max())
    img_size = check_img_size(img_size, s=stride)

    if no_trace:
        model = TracedModel(model, device, img_size)

    if half:
        model.half()


    if source.isnumeric() or source.endswith('.txt') or source.lower().startswith(
            ('rtsp://', 'rtmp://', 'http://', 'https://')):
        cudnn.benchmark = True
        dataset = LoadStreams(source, img_size=img_size, stride=stride)
    else:
        dataset = LoadImages(source, img_size=img_size, stride=stride)

    names = model.module.names if hasattr(model, 'module') else model.names

    if device.type != 'cpu':
        model(torch.zeros(1, 3, img_size, img_size).to(device).type_as(next(model.parameters())))

    old_img_w = old_img_h = img_size
    old_img_b = 1

    for path, img, im0s, vid_cap in dataset:
        img = torch.from_numpy(img).to(device)
        img = img.half() if half else img.float()
        img /= 255.0

        if img.ndimension() == 3:
            img = img.unsqueeze(0)

        if device.type != 'cpu' and (old_img_b != img.shape[0] or old_img_h != img.shape[2] or old_img_w != img.shape[3]):
            old_img_b = img.shape[0]
            old_img_h = img.shape[2]
            old_img_w = img.shape[3]
            for i in range(3):
                model(img, augment=augment)[0]

        with torch.no_grad():
            pred = model(img, augment=augment)[0]

        pred = non_max_suppression(pred, conf_thres, iou_thres, classes=classes, agnostic=agnostic_nms)

        for i, det in enumerate(pred):
            if source.isnumeric():
                p, s, im0, frame = path[i], '%g: ' % i, im0s[i].copy(), dataset.count
            else:
                p, s, im0, frame = path, '', im0s, getattr(dataset, 'frame', 0)

            p = Path(p)

            if len(det):
                det[:, :4] = scale_coords(img.shape[2:], det[:, :4], im0.shape).round()

                for c in det[:, -1].unique():
                    n = (det[:, -1] == c).sum()
                    s += f"{n} {names[int(c)]}{'s' * (n > 1)}, "
                    if(names[int(c)]=='bottle'):
                            return n

        return 0
