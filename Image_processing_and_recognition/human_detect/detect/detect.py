import cv2
import os
import time
import datetime
import numpy as np
from utils.logger import setup_logger

logger = setup_logger("OpenLock")

class FaceRecognition:
    def read_dic_face(self,file_list):
        dic_face = {}
        with open(file_list) as f:
            num_lines = 0
            for lines in f:
                num_lines += 1
                num_id = lines.split(" ", 1)[0]
                face_id = lines.split(" ", 1)[1]
                face_id = face_id.replace('\n', '')
                dic_face[int(num_id)] = face_id


        return dic_face


    def face_detect(self,recognizer,faceCascade,dic_face,cap):

        # 读取一帧图像
        img = cap

        # 转换为灰度
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # 进行人脸检测
        faces = faceCascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(50, 50),
                                                 flags=cv2.CASCADE_SCALE_IMAGE)

        # 遍历检测到的人脸
        for (x, y, w, h) in faces:

            # 进行人脸识别
            id_face, confidence = recognizer.predict(gray[y:y + h, x:x + w])


            # 检测可信度，这里是通过计算距离来计算可信度，confidence越小说明越近似
            if (confidence < 60):
                str_face = dic_face[id_face]
                str_confidence = "  %.2f" % confidence
                color = (0, 255, 0)
                flag = True
                logger.info(f"人脸检测结果： {str_face} , {confidence:.4f},{flag}")
                return {"x": x,"y": y,"w": w,"h": h,"flag": flag,"color": color,"str_confidence": str_confidence,"str_face": str_face}



            else:
                str_face = "unknown"
                color = (0, 0, 255)
                flag = False
                str_confidence = "  %.2f" % confidence
                logger.info(f"人脸检测结果： {str_face} , {confidence:.4f},{flag}")
                return {"x": x,"y": y,"w": w,"h": h,"flag": flag,"color": color,"str_confidence": str_confidence,"str_face": str_face}