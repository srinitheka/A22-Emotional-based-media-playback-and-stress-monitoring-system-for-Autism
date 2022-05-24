import cv2
import tensorflow
from Models.model import FacialExpressionModel
import numpy as np
import time
import serial
from audioplayer import AudioPlayer

rgb = cv2.VideoCapture(0)
facec = cv2.CascadeClassifier('Models/haarcascade_frontalface_default.xml')
font = cv2.FONT_HERSHEY_SIMPLEX
found = set()



arduinoData = serial.Serial('COM5', 115200)
readdat=""

def getSeriAl():
    global DaTa_r
    global gsr_r
    global   stat
    if(arduinoData.in_waiting >0):
        line = arduinoData.readline()
        readdat=line.decode()
        
        #print(readdat)
        if(readdat == "Ready\r\n"):
            print("Device online")
            arduinoData.write('PyreC$'.encode())
        if(readdat == "GSR:\r\n"):
            line = arduinoData.readline()
            readdat=line.decode()
            gsr_r=readdat
            #print(readdat)
        
        print(readdat)
             

    else:
        readdat=""




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
    count_h=0
    count_s=0
    count_n=0
    while True:
        global gsr_r
        
        getSeriAl()
        print("gsr: ",gsr_r)
        faces, fr, gray_fr = __get_data__()
        for (x, y, w, h) in faces:
            time.sleep(0.2)
            fc = gray_fr[y:y+h, x:x+w]
            
            roi = cv2.resize(fc, (48, 48))
            pred = cnn.predict_emotion(roi[np.newaxis, :, :, np.newaxis])

            cv2.putText(fr, pred, (x, y), font, 1, (255, 255, 0), 2)
            cv2.rectangle(fr,(x,y),(x+w,y+h),(255,0,0),2)
            if(str(pred)=='Happy' ):
                count_h+=1
                count_s=0
                print("Happy ",count_h)
                if(count_h>=5 and (int(gsr_r)>0 and int(gsr_r) <80)):
                    arduinoData.write('Happy$'.encode())
                    AudioPlayer("rhy.mp3").play(block=True)
                    arduinoData.write('PyreC$'.encode())
                    count_h=0
                elif(count_h>5 and (int(gsr_r)==0 or int(gsr_r)> 80)):
                    count_h=0
                    arduinoData.write('PyreC$'.encode())
            elif(str(pred)=='Sad' ):
                count_s+=1
                count_h=0
                print("Sad ",count_s)
                if(count_s>=5 and int(gsr_r)>80):
                    arduinoData.write('Sad$'.encode())
                    AudioPlayer("rhythmic_clapping.wav").play(block=True)
                    arduinoData.write('PyreC$'.encode())
                    count_s=0
                elif(count_s>5):
                    count_s=0
                    arduinoData.write('PyreC$'.encode())
            else:
                count_n+=1
                count_s=0
                count_h=0
                if(count_n>=5):
                    count_n=0
                    arduinoData.write('PyreC$'.encode())
                

        if cv2.waitKey(1) == 27:
            break
        cv2.imshow('Emotion Based Teaching', fr)
    cv2.destroyAllWindows()

gsr_r=0
getSeriAl()
if __name__ == '__main__':
    model = FacialExpressionModel("Models/face_model.json", "Models/face_model.h5")
    start_app(model)
