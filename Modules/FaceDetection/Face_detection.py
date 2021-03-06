import cv2
import mediapipe as mp
import time
pTime = 0
cap = cv2.VideoCapture("face_detect.mp4")

mpFaceDetection = mp.solutions.face_detection
mpDraw = mp.solutions.drawing_utils
faceDetection = mpFaceDetection.FaceDetection()


while True:
    success, img = cap.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = faceDetection.process(imgRGB)
    if results.detections:
        for id, detection in enumerate(results.detections):
            print(id, detection)
            #mpDraw.draw_detection(img, detection)
            bboxC = detection.location_data.relative_bounding_box
            ih, iw, ic = img.shape
            bboxC = int(bboxC.xmin * iw), int(bboxC.ymin * ih), \
                    int(bboxC.width * iw),int(bboxC.height * ih)
            cv2.rectangle(img, bboxC, (255,0,255), 2)
            cv2.putText(img, f'{int(detection.score[0] * 100)}%', (bboxC[0], bboxC[1] - 20), cv2.FONT_HERSHEY_PLAIN, 3,
                        (0, 255, 0), 2)
    img = cv2.resize(img, (600, 400))

    cTime = time.time()
    fps = 1/(cTime - pTime)
    pTime = cTime
    cv2.putText(img,f'Fps: {int(fps)}',(20,70), cv2.FONT_HERSHEY_PLAIN, 3, (255,0,0),2)

    cv2.imshow("Image", img)
    cv2.waitKey(1)
