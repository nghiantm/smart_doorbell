import cv2
from simple_facerec import SimpleFacerec
import logging
import os
from resize import resize_and_compress_image
import requests
from datetime import datetime, timezone

class Doorbell:
    def __init__(self):
        # init face recogniion class and load in face images
        self.imageDirectory = "doorbell/images"
        self.tempImageDirectory = "doorbell/temp_images"
        self.sfr = SimpleFacerec()
        self.sfr.load_encoding_images(self.imageDirectory)

        ''' CHANGE RECORDING SOURCE ACCORDING TO YOUR DEVICE '''
        self.cap = cv2.VideoCapture(1)
        # init variables for cap.read() function
        self.ret = False # status for indicating success of read() function
        self.frame = None

        # init variables for detect_known_faces() function
        self.faceLocations = [] # coordinates for face in frame
        self.faceNames = []

        # init variables for detected persons
        self.detectedFaces = {} # add to when detect, clear when make API request
        self.init_detected_faces()

    def init_detected_faces(self):
        if os.path.isdir(self.imageDirectory):
            # list all image files
            fileList = os.listdir(self.imageDirectory)

            for fileName in fileList:
                nameWithoutExtension, _ = os.path.splitext(fileName)

                # add each file name as a key and a default value of FALSE to detectedFaces
                self.detectedFaces[nameWithoutExtension] = {
                    "status": False,
                    "timestamp": None
                }
                self.detectedFaces["status"] = False
        else:
            logging.error("Invalid image directory")

    def read_frame(self):
        self.ret, self.frame = self.cap.read()

    def send_detected_persons(self, directoryPath):
        # Check if the directory exists
        if not os.path.isdir(directoryPath):
            logging.error("Invalid temp_image directory")
            return
        
        # Get a list of all files in the directory
        fileList = os.listdir(directoryPath)

        # Filter the list to include only image files (you may want to expand this check)
        imageFiles = [file for file in fileList if file.endswith(('.jpg', '.jpeg'))]

        if not imageFiles:
            logging.warning(f"No images found in '{directoryPath}'.")
            return
        
        for imageFile in imageFiles:
            # Construct the full path to the image file
            imagePath = os.path.join(directoryPath, imageFile)

            # Process the image 
            base64Image = resize_and_compress_image(imagePath, 1920, 1080, 40)

            nameWithoutExtension, _ = os.path.splitext(imageFile)

            # Get the current date and time
            current_datetime = datetime.now(timezone.utc)  # Use utcnow() for UTC time or datetime.now() for local time

            # Format the datetime object as ISO 8601 string
            iso8601_string = current_datetime.isoformat(timespec="seconds")

            try:
                r = requests.post(
                        'http://localhost:5214/detection', 
                        json={
                            "name": nameWithoutExtension,
                            "date": iso8601_string,
                            "address": "3835 Lancaster",
                            "image": base64Image
                        }
                    )
                
                if r.status_code in [200, 201]:
                    logging.info("POSTED")
                    os.remove(imagePath)
                else:
                    logging.warning("Failed POST request")
                    logging.warning(r.text)
            except: 
                logging.error("Wrong backend address, check port number")

        self.init_detected_faces()

    def process_detected_frames(self, face_loc, name):
        y1, x2, y2, x1 = face_loc[0], face_loc[1], face_loc[2], face_loc[3]

        cv2.putText(self.frame, name,(x1, y1 - 10), cv2.FONT_HERSHEY_DUPLEX, 2, (0, 0, 200), 2)
        cv2.rectangle(self.frame, (x1, y1), (x2, y2), (0, 0, 200), 4)

        if self.detectedFaces[name]["status"] == 0:
            logging.info(f"Detected {name}")
            cv2.imwrite(f'doorbell/temp_images/{name}.jpg', self.frame)
            self.detectedFaces[name]["status"] = True
            self.detectedFaces["status"] = True

    def process_frames_continously(self):
        while True:
            self.read_frame()
            
            # detect faces
            self.faceLocations, self.faceNames = self.sfr.detect_known_faces(self.frame)

            if not self.faceNames:
                if self.detectedFaces["status"] == True:
                    self.send_detected_persons(self.tempImageDirectory)
            else:
                for face_loc, name in zip(self.faceLocations, self.faceNames):
                    if name != "Unknown":
                        self.process_detected_frames(face_loc, name)

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