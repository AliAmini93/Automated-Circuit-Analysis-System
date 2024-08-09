import logging

logger = logging.getLogger('logger_Info')
logger_Debug = logging.getLogger('logger_Debug')
from ultralytics import YOLO

model = YOLO('ocrDetection/best.pt')


def ocr_detection(path):
    results = model.predict(path, conf=0.5, save_crop=True)

    dic = results[0].names
    try:
        logo = dic[results[0].boxes.cls.cpu().data.numpy()[0]]
    except Exception as e:
        logger_Debug.exception(e)
        logo = None
    print('Result of logo detection: %s' % logo)
    return logo
# path='IC-Images/hynix/748.jpg'
# print(ocr_detection(path))
