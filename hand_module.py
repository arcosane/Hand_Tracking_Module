import cv2 as cv
import mediapipe as mp 
import time


class HandDetector():
    def __init__(self ,mode = False , maxHands = 2 ,modelComplexity=1,  detectionCon = 0.5 , trackCon = 0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.modelComplex = modelComplexity
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode,self.maxHands,self.modelComplex, self.detectionCon, self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils
        
    def findHands(self, img , draw = True):
        imgRGB = cv.cvtColor(img , cv.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)

        if self.results.multi_hand_landmarks:
            for handLnd in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLnd, self.mpHands.HAND_CONNECTIONS)
        return img
    
    def findPosition(self, img, handNo=0, draw=True):
        
        lmList = []
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]
            for id , lm in enumerate(myHand.landmark):
                h, w, c = img.shape
                cx , cy = int(lm.x*w) , int(lm.y*h)
                lmList.append([id,cx,cy])
                if draw:
                    cv.circle(img , (cx,cy), 10 , (255,255,0), cv.FILLED)        
        return lmList           
           
           
def main():
    cap = cv.VideoCapture(0)
    pTime = 0
    cTime = 0
    
    detector = HandDetector()
    
    while True:
        success, img = cap.read()
        img = detector.findHands(img)  
        lmList = detector.findPosition(img)
        
        
        
        cTime = time.time()
        fps = 1/(cTime - pTime)
        pTime = cTime
        cv.putText(img, str(int(fps)), (10,70), cv.FONT_HERSHEY_SIMPLEX, 3, (0,255,0), 2)
        cv.imshow("image",img)
        cv.waitKey(1)
    
if __name__ == "__main__":
    main()