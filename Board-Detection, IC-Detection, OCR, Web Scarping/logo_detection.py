import logging

logger = logging.getLogger('logger_Info')
logger_Debug = logging.getLogger('logger_Debug')
from ultralytics import YOLO
import cv2

model = YOLO('logoDetectionModel/best.pt')


def logo_detection(img):
    results = model.predict(img, conf=0.5, max_det=1,
                            verbose=False)  # save=True, save_txt=True,conf=0.5,save_crop=True,max_det=1,show=True)
    dic = results[0].names
    try:
        box = results[0].boxes.xywh.cpu().data.numpy()[0]
        x, y, w, h = box[0], box[1], box[2], box[3]
        x = x - (w / 2)
        y = y - (h / 2)
        cv2.rectangle(img, (int(x), int(y)), (int(x + w), int(y + h)), (0, 0, 0), -1)

        logo = dic[results[0].boxes.cls.cpu().data.numpy()[0]]
        logo = logo.split('.')[0]
    except Exception as e:
        logger_Debug.exception(str(e))
        logo = None
    print('Result of logo detection: %s' % logo)
    logger.info('Result of logo detection: %s' % logo)
    logger_Debug.info('Result of logo detection: %s' % logo)
    return logo
# img=cv2.imread('two_side_1.png')
# logo_detection(img)
