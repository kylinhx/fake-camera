import cv2
import os
import random
import pyvirtualcam

class FakeCamera:
    def __init__(self, video_file, root_path):
        
        self.number = len(video_file)
        self.root = root_path

        self.video_file = video_file

        self.video = cv2.VideoCapture(self.root + self.video_file[random.randint(0, self.number - 1)])

    def read(self):
        ret, frame = self.video.read()
        if ret:
            return ret, frame
        else:
            # is video is done, select a new video file randomly
            self.video = cv2.VideoCapture(self.root + self.video_file[random.randint(0, self.number - 1)])
            # is video is done, restart the video
            self.video.set(cv2.CAP_PROP_POS_FRAMES, 0)
            
            return self.video.read()

    def release(self):
        self.video.release()


# main funciton
def play_fake_camera():
    video_file = os.listdir('./video/')  # video path
    root_path = './video/'
    fake_camera = FakeCamera(video_file, root_path)

    # create virtual camera
    with pyvirtualcam.Camera(width=1280, height=576, fps=24) as cam:
        while True:
            ret, frame = fake_camera.read()
            if not ret:
                break
            
            # turn frame to BGR
            img = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            
            # send frame to virtual camera
            cam.send(img)

            # Show frame（Choose）
            # cv2.imshow('Fake Camera', frame)

            # Check keyboard imput, if 'q' is pressed, break
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

            # camera wait for next frame
            cam.sleep_until_next_frame()

    fake_camera.release()
    cv2.destroyAllWindows()

# run the code
play_fake_camera()
