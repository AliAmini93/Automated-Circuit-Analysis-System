import logging

logger = logging.getLogger('logger_Info')
from paddleocr import PaddleOCR
from ultralytics import YOLO
from imutils import perspective
import numpy as np
from scipy import ndimage, stats

paddleOCR = PaddleOCR(use_angle_cls=True, lang="en", cls=True,
                      rec_model_dir='PaddleOCRModel/inference/en_PP-OCRv4_rec_IC_yolo8_cml_rotate',
                      det_model_dir='PaddleOCRModel/inference/en_PP-OCRv3_det_infer',
                      rec_char_dict_path='PaddleOCRModel/inference/en_dict.txt',
                      cls_model_dir='PaddleOCRModel/inference/ch_ppocr_mobile_v2.0_cls_infer',
                      use_gpu=False,
                      show_log=False)
model = YOLO('BoxDetectionModel/best.pt')


def rotate_90(image):
    angle = 0
    shape = image.shape
    if shape[0] > shape[1]:
        angle = 90
        rotated = ndimage.rotate(image, 90, reshape=True)
        return rotated, angle
    return image, angle


def ocr(img):
    texts = []
    angles = []

    results = model.predict(img, conf=0.5,
                            verbose=False)  # save=True, save_txt=True,conf=0.5,save_crop=True,max_det=1,show=True)
    boxes = results[0].boxes.xywh.cpu().numpy()

    for i, box in enumerate(boxes):

        x, y, w, h = int(box[0]), int(box[1]), int(box[2]), int(box[3])
        x = x - (w / 2)
        y = y - (h / 2)

        pts = np.asarray([(x, y + h), (x + w, y + h), (x + w, y), (x, y)])

        warped = perspective.four_point_transform(img, pts)
        warped, angle = rotate_90(warped)

        result = paddleOCR.ocr(np.array(warped), cls=True, det=False, rec=False)

        if result[0][0][0] == '180':
            angle += 180

            warped = ndimage.rotate(warped, 180, reshape=True)

        angles.append(angle)

        result = paddleOCR.ocr(np.array(warped), cls=False, det=False, rec=True)

        texts.append(result[0][0][0])
    if len(angles) == 0:
        angles.append(0)
    print('ALL TEXT: ', texts)
    logger.info('ALL TEXT: %s' % str(texts))
    return (texts, stats.mode(angles)[0])
