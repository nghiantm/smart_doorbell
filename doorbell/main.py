import cv2
from simple_facerec import SimpleFacerec
import logging
import os

class Doorbell():
    def __init__(self):
        # init face recogniion class and load in face images
        self.imageDirectory = "images/"
        self.sfr = SimpleFacerec()
        self.sfr.load_encoding_images(self.imageDirectory)

        ''' CHANGE RECORDING SOURCE ACCORDING TO YOUR DEVICE '''
        self.cap = cv2.VideoCapture(0)
        # init variables for cap.read() function
        self.ret = False # status for indicating success of read() function
        self.frame = None

        # init variables for detect_known_faces() function
        self.faceLocations = [] # coordinates for face in frame
        self.faceNames = []

        # init variables for detected persons
        self.detectedFaces = {} # add to when detect, clear when make API request
        self._init_detected_faces()

    def _init_detected_faces(self):
        if os.path.isdir(self.imageDirectory):
            # list all image files
            fileList = os.listdir(self.imageDirectory)

            for fileName in fileList:
                nameWithoutExtension, _ = os.path.splitext(fileName)

                # add each file name as a key and a default value of FALSE to detectedFaces
                self.detectedFaces[nameWithoutExtension] = {
                    "status": 0,
                    "coordinate": [0, 0, 0, 0]
                }

            print(self.detectedFaces)
        else:
            logging.error("Invalid image directory")

    def read_frame(self):
        self.ret, self.frame = self.cap.read()

    def process_frames_continously(self):
        while True:
            self.read_frame()
            
            # detect faces
            self.faceLocations, self.faceNames = self.sfr.detect_known_faces(self.frame)

            if not self.faceNames:
                # no faces detected
                # TODO: MAKE API REQUEST
                pass
            else:
                for face_loc, name in zip(self.faceLocations, self.faceNames):
                    if name != "Unknown":
                        y1, x2, y2, x1 = face_loc[0], face_loc[1], face_loc[2], face_loc[3]

                        if self.detectedFaces[name]["status"] == 0:
                            logging.info(f"Detected {name}")
                            cv2.imwrite('file.jpg', self.frame)
                            self.detectedFaces[name]["status"] = 1
                            self.detectedFaces[name]["coordinate"] = [y1, x2, y2, x1]

                        cv2.putText(self.frame, name,(x1, y1 - 10), cv2.FONT_HERSHEY_DUPLEX, 2, (0, 0, 200), 2)
                        cv2.rectangle(self.frame, (x1, y1), (x2, y2), (0, 0, 200), 4)

                        '''
                        if self.detectedFaces[name]["status"] == 0:
                            logging.info(f"Detected {name}")
                            cv2.imwrite('file.jpg', self.frame)
                            self.detectedFaces[name] = True
                        '''

            cv2.imshow("Frame", self.frame)
            key = cv2.waitKey(1)

    def run(self):
        try: 
            self.process_frames_continously()
        except KeyboardInterrupt:
            # quit when Ctrl + C is pressed
            logging.info('EXITING')
            print(self.detectedFaces)
            self.cap.release()
            cv2.destroyAllWindows()
        

if __name__ == "__main__":
    logging.basicConfig()
    logging.getLogger().setLevel(logging.INFO)
    doorbell = Doorbell()
    doorbell.run()
        