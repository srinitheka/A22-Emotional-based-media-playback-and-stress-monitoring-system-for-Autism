import cv2
from model import FacialExpressionModel
import numpy as np
import time
from audioplayer import AudioPlayer
rgb = cv2.VideoCapture(0)
facec = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
font = cv2.FONT_HERSHEY_SIMPLEX
found = set()
def __get_data__():
    """
    __get_data__: Gets data from the VideoCapture object and classifies them
    to a face or no face. 
    
    returns: tuple (faces in image, frame read, grayscale frame)
    """
    _, fr = rgb.read()
    fr=cv2.flip(fr,1)
    gray = cv2.cvtColor(fr, cv2.COLOR_BGR2GRAY)
    faces = facec.detectMultiScale(gray, 1.3, 5)
    
    return faces, fr, gray

def start_app(cnn):
    skip_frame = 10
    data = []
    flag = False
    ix = 0
    count_h=0
    count_s=0
    while True:
        ix += 1
        
        faces, fr, gray_fr = __get_data__()
        for (x, y, w, h) in faces:
            fc = gray_fr[y:y+h, x:x+w]
            
            roi = cv2.resize(fc, (48, 48))
            pred = cnn.predict_emotion(roi[np.newaxis, :, :, np.newaxis])

            cv2.putText(fr, pred, (x, y), font, 1, (255, 255, 0), 2)
            cv2.rectangle(fr,(x,y),(x+w,y+h),(255,0,0),2)
            if(str(pred)=='Happy'):
                count_h+=1
                count_s=0
                print("Happy ",count_h)
                if(count_h>=5):
                    AudioPlayer("rhy.mp3").play(block=True)
            if(str(pred)=='Sad'):
                count_s+=1
                count_h=0
                print("Sad ",count_s)
                if(count_s>=5):
                    AudioPlayer("rhythmic_clapping.wav").play(block=True)
            else:
                count=0
                

        if cv2.waitKey(1) == 27:
            break
        cv2.imshow('Filter', fr)
    cv2.destroyAllWindows()


if __name__ == '__main__':
    model = FacialExpressionModel("face_model.json", "face_model.h5")
    start_app(model)
