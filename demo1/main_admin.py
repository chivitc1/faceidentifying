import time

import cv2
import tkinter
import PIL.Image, PIL.ImageTk

class App:
    def __init__(self, window, window_title, video_source=0):
        self.window = window
        self.window.title(window_title)
        self.video_source = video_source

        # Canvas control
        self.vid = MyVideoCapture(self.video_source)
        self.canvas = tkinter.Canvas(window, width=self.vid.width, height=self.vid.height)
        self.canvas.pack()

        # Textbox control
        self.lbl = tkinter.Label(window, text="Person Name").pack(padx=5, pady=20, side=tkinter.LEFT)

        self.personName = tkinter.StringVar()
        self.txtPersonName = tkinter.Entry(window, width=30, textvariable=self.personName).pack(padx=5, pady=20, side=tkinter.LEFT)

        # Button control
        self.btn_capture = tkinter.Button(window, text="Capture", width=50, command=self.capture).pack(padx=5, pady=20, side=tkinter.LEFT)

        self.delay = 15
        self.update()
        self.window.mainloop()

    def update(self):
        ret, frame = self.vid.get_frame()

        if ret:
            self.photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
            self.canvas.create_image(0,0, image=self.photo, anchor=tkinter.NW)
        self.window.after(self.delay, self.update)

    def capture(self):
        if not self.personName:
            return

        ret, frame = self.vid.get_frame()
        if ret:
            dir_name = "images/{}".format(self.personName.get())
            import os
            os.makedirs(dir_name, exist_ok=True)
            file_name = "{}/img_{}.jpg".format(dir_name, time.strftime("%Y%m%d_%H%M%S"))
            print(file_name)
            cv2.imwrite(file_name, cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))


class MyVideoCapture:
    def __init__(self, video_source=0):
        self.vid = cv2.VideoCapture(video_source)
        if not self.vid.isOpened():
            raise ValueError("Unable to open video source", video_source)

        self.width = self.vid.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT)

    def __del__(self):
        if self.vid.isOpened():
            self.vid.release()

    def get_frame(self):
        if self.vid.isOpened():
            ret, frame = self.vid.read()
            if ret:
                return ret, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            else:
                return ret, None


if __name__ == '__main__':
    App(tkinter.Tk(), "Video capture")
