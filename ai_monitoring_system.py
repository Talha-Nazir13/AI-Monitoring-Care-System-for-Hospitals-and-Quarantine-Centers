#!/usr/bin/env python
# coding: utf-8

# In[6]:


import cv2
import numpy as np
import math
import time
import json
import tkinter as tk
from tkinter import filedialog

# Global variables
video_path = ""
activity_data = {"activities": []}
output_box = None
count = 0
count1 = 0
slope = 0
slope1 = 100
minArea = 120 * 100
radianToDegree = 57.324
minimumLengthOfLine = 150.0
minAngle = 18
maxAngle = 72
cooldown_duration = 7  # seconds
list_falls = []
count_fall = 0
cooldown_start_time = 0
firstFrame = None

# Function definition for frame Conversion
def convertFrame(frame):
    r = 750.0 / frame.shape[1]
    dim = (750, int(frame.shape[0] * r))
    frame = cv2.resize(frame, dim, interpolation=cv2.INTER_AREA)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (31, 31), 0)

    return frame, gray

def select_video():
    global video_path
    video_path = filedialog.askopenfilename()

def run_detection():
    global video_path, activity_data, output_box
    cap = cv2.VideoCapture(video_path)
    count_fall = 0
    cooldown_start_time = 0
    firstFrame = None

    while True:
        ret, frame = cap.read()
        if frame is None:
            break
        frame, gray = convertFrame(frame)

        # Comparison Frame
        if firstFrame is None:
            time.sleep(1.0)
            _, frame = cap.read()
            frame, gray = convertFrame(frame)
            firstFrame = gray
            continue

        # Frame difference between current and comparison frame
        frameDelta = cv2.absdiff(firstFrame, gray)
        # Thresholding
        thresh1 = cv2.threshold(frameDelta, 20, 255, cv2.THRESH_BINARY)[1]
        # Dilation of Pixels
        thresh = cv2.dilate(thresh1, None, iterations=15)

        # Finding the Region of Interest with changes
        contours, _ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        for con in contours:
            if len(con) >= 5 and cv2.contourArea(con) > minArea:
                ellipse = cv2.fitEllipse(con)

                # Draw ellipse
                cv2.ellipse(frame, ellipse, (255, 255, 0), 5)

                # Co-ordinates of extreme points
                extTop = tuple(con[con[:, :, 1].argmin()][0])
                extBot = tuple(con[con[:, :, 1].argmax()][0])
                extLeft = tuple(con[con[:, :, 0].argmin()][0])
                extRight = tuple(con[con[:, :, 0].argmax()][0])

                line1 = math.sqrt((extTop[0] - extBot[0]) * (extTop[0] - extBot[0]) + (extTop[1] - extBot[1]) * (
                            extTop[1] - extBot[1]))
                midPoint = [extTop[0] - int((extTop[0] - extBot[0]) / 2),
                            extTop[1] - int((extTop[1] - extBot[1]) / 2)]
                if line1 > minimumLengthOfLine:
                    if (extTop[0] != extBot[0]):
                        slope = abs(extTop[1] - extBot[1]) / (extTop[0] - extBot[0])

                else:
                    if (extRight[0] != extLeft[0]):
                        slope = abs(extRight[1] - extLeft[1]) / (extRight[0] - extLeft[0])

                originalAngleP = np.arctan((slope1 - slope) / (1 + slope1 * slope))
                originalAngleH = np.arctan(slope)
                originalAngleH = originalAngleH * radianToDegree
                originalAngleP = originalAngleP * radianToDegree

                if (abs(originalAngleP) > minAngle and abs(originalAngleH) < maxAngle and abs(
                        originalAngleP) + abs(originalAngleH) > 89 and abs(
                        originalAngleP) + abs(originalAngleH) < 91):
                    current_time = time.time()
                    if current_time - cooldown_start_time > cooldown_duration:
                        count_fall += 1
                        output_box.insert(tk.END, "Fall detected\n")
                        activity_data["activities"].append({"time": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(current_time)),
                                                             "activity": "Fall"})
                        cooldown_start_time = current_time

        if len(contours) > 0:
            if cv2.contourArea(contours[0]) > 1000:
                current_time = time.time()
                if current_time - cooldown_start_time > cooldown_duration:
                    output_box.insert(tk.END, "Some activity detected\n")
                    activity_data["activities"].append({"time": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(current_time)),
                                                         "activity": "Some activity detected"})
                    cooldown_start_time = current_time

        cv2.imshow('Frame', frame)
        cv2.imshow('Thresh', thresh)
        output_box.update()  # Update output box
        k = cv2.waitKey(30) & 0xff
        if k == 27:
            break

    cap.release()
    cv2.waitKey(1)
    cv2.destroyAllWindows()

def save_report():
    global activity_data
    filename = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON Files", "*.json")])
    if filename:
        with open(filename, "w") as json_file:
            json.dump(activity_data, json_file)

def exit_application():
    root.destroy()

# Tkinter GUI
root = tk.Tk()
root.title("AI Care Monitoring System")
root.geometry("800x600")

# Button to select a video
select_button = tk.Button(root, text="Select Video", command=select_video)
select_button.pack()

# Button to run detection
run_button = tk.Button(root, text="Run Detection", command=run_detection)
run_button.pack()

# Output box to display detected activities
output_frame = tk.Frame(root)
output_frame.pack(pady=10)
output_label = tk.Label(output_frame, text="Detected Activities:")
output_label.pack()
output_box = tk.Text(output_frame, height=10, width=30)
output_box.pack()

# Button to save activity report
save_button = tk.Button(root, text="Save Report", command=save_report)
save_button.pack()

# Button to exit application
exit_button = tk.Button(root, text="Exit", command=exit_application)
exit_button.pack()

root.mainloop()


# In[3]:


import cv2
import numpy as np
import math
import time
import json
import tkinter as tk
from tkinter import filedialog

# Global variables
video_path = ""
activity_data = {"activities": []}
output_box = None
count = 0
count1 = 0
slope = 0
slope1 = 100
minArea = 120 * 100
radianToDegree = 57.324
minimumLengthOfLine = 150.0
minAngle = 18
maxAngle = 72
cooldown_duration = 7  # seconds
list_falls = []
count_fall = 0
cooldown_start_time = 0
firstFrame = None

# Function definition for frame Conversion
def convertFrame(frame):
    r = 750.0 / frame.shape[1]
    dim = (750, int(frame.shape[0] * r))
    frame = cv2.resize(frame, dim, interpolation=cv2.INTER_AREA)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (31, 31), 0)

    return frame, gray

def select_video():
    global video_path
    video_path = filedialog.askopenfilename()

def run_detection():
    global video_path, activity_data, output_box
    cap = cv2.VideoCapture(video_path)
    count_fall = 0
    cooldown_start_time = 0
    firstFrame = None

    while True:
        ret, frame = cap.read()
        if frame is None:
            break
        frame, gray = convertFrame(frame)

        # Comparison Frame
        if firstFrame is None:
            time.sleep(1.0)
            _, frame = cap.read()
            frame, gray = convertFrame(frame)
            firstFrame = gray
            continue

        # Frame difference between current and comparison frame
        frameDelta = cv2.absdiff(firstFrame, gray)
        # Thresholding
        thresh1 = cv2.threshold(frameDelta, 20, 255, cv2.THRESH_BINARY)[1]
        # Dilation of Pixels
        thresh = cv2.dilate(thresh1, None, iterations=15)

        # Finding the Region of Interest with changes
        contours, _ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        for con in contours:
            if len(con) >= 5 and cv2.contourArea(con) > minArea:
                ellipse = cv2.fitEllipse(con)

                # Draw ellipse
                cv2.ellipse(frame, ellipse, (255, 255, 0), 5)

                # Co-ordinates of extreme points
                extTop = tuple(con[con[:, :, 1].argmin()][0])
                extBot = tuple(con[con[:, :, 1].argmax()][0])
                extLeft = tuple(con[con[:, :, 0].argmin()][0])
                extRight = tuple(con[con[:, :, 0].argmax()][0])

                line1 = math.sqrt((extTop[0] - extBot[0]) * (extTop[0] - extBot[0]) + (extTop[1] - extBot[1]) * (
                            extTop[1] - extBot[1]))
                midPoint = [extTop[0] - int((extTop[0] - extBot[0]) / 2),
                            extTop[1] - int((extTop[1] - extBot[1]) / 2)]
                if line1 > minimumLengthOfLine:
                    if (extTop[0] != extBot[0]):
                        slope = abs(extTop[1] - extBot[1]) / (extTop[0] - extBot[0])

                else:
                    if (extRight[0] != extLeft[0]):
                        slope = abs(extRight[1] - extLeft[1]) / (extRight[0] - extLeft[0])

                originalAngleP = np.arctan((slope1 - slope) / (1 + slope1 * slope))
                originalAngleH = np.arctan(slope)
                originalAngleH = originalAngleH * radianToDegree
                originalAngleP = originalAngleP * radianToDegree

                if (abs(originalAngleP) > minAngle and abs(originalAngleH) < maxAngle and abs(
                        originalAngleP) + abs(originalAngleH) > 89 and abs(
                        originalAngleP) + abs(originalAngleH) < 91):
                    current_time = time.time()
                    if current_time - cooldown_start_time > cooldown_duration:
                        count_fall += 1
                        output_box.insert(tk.END, "Fall detected\n")
                        activity_data["activities"].append({"time": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(current_time)),
                                                             "activity": "Fall"})
                        cooldown_start_time = current_time

        if len(contours) > 0:
            if cv2.contourArea(contours[0]) > 1000:
                current_time = time.time()
                if current_time - cooldown_start_time > cooldown_duration:
                    output_box.insert(tk.END, "Some activity detected\n")
                    activity_data["activities"].append({"time": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(current_time)),
                                                         "activity": "Some activity detected"})
                    cooldown_start_time = current_time

        cv2.imshow('Frame', frame)
        cv2.imshow('Thresh', thresh)
        output_box.update()  # Update output box
        k = cv2.waitKey(30) & 0xff
        if k == 27:
            break

    cap.release()
    cv2.waitKey(1)
    cv2.destroyAllWindows()

def save_report():
    global activity_data
    filename = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON Files", "*.json")])
    if filename:
        with open(filename, "w") as json_file:
            json.dump(activity_data, json_file)

def exit_application():
    root.destroy()

# Tkinter GUI
root = tk.Tk()
root.title("AI Care Monitoring System")
root.geometry("900x600")

# Button to select a video
select_button = tk.Button(root, text="Select Video", command=select_video)
select_button.pack()

# Button to run detection
run_button = tk.Button(root, text="Run Detection", command=run_detection)
run_button.pack()

# Output box to display detected activities
output_frame = tk.Frame(root)
output_frame.pack(pady=10)
output_label = tk.Label(output_frame, text="Detected Activities:")
output_label.pack()
output_box = tk.Text(output_frame, height=10, width=30)
output_box.pack()

# Button to save activity report
save_button = tk.Button(root, text="Save Report", command=save_report)
save_button.pack()

# Button to exit application
exit_button = tk.Button(root, text="Exit", command=exit_application)
exit_button.pack()

# Video display label
video_label = tk.Label(root)
video_label.pack(side="bottom")  # Placing video label at the bottom

root.mainloop()


# # Ready To Use

# In[3]:


import cv2
import numpy as np
import math
import time
import json
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk


# Global variables
video_path = ""
activity_data = {"activities": []}
output_box = None
count = 0
count1 = 0
slope = 0
slope1 = 100
minArea = 120 * 100
radianToDegree = 57.324
minimumLengthOfLine = 150.0
minAngle = 18
maxAngle = 72
cooldown_duration = 7  # seconds
list_falls = []
count_fall = 0
cooldown_start_time = 0
firstFrame = None

# Function definition for frame Conversion
def convertFrame(frame):
    r = 750.0 / frame.shape[1]
    dim = (750, int(frame.shape[0] * r))
    frame = cv2.resize(frame, dim, interpolation=cv2.INTER_AREA)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (31, 31), 0)

    return frame, gray

def select_video():
    global video_path
    video_path = filedialog.askopenfilename()

def run_detection():
    global video_path, activity_data, output_box
    cap = cv2.VideoCapture(video_path)
    count_fall = 0
    cooldown_start_time = 0
    firstFrame = None

    while True:
        ret, frame = cap.read()
        if frame is None:
            break
        frame, gray = convertFrame(frame)

        # Comparison Frame
        if firstFrame is None:
            time.sleep(1.0)
            _, frame = cap.read()
            frame, gray = convertFrame(frame)
            firstFrame = gray
            continue

        # Frame difference between current and comparison frame
        frameDelta = cv2.absdiff(firstFrame, gray)
        # Thresholding
        thresh1 = cv2.threshold(frameDelta, 20, 255, cv2.THRESH_BINARY)[1]
        # Dilation of Pixels
        thresh = cv2.dilate(thresh1, None, iterations=15)

        # Finding the Region of Interest with changes
        contours, _ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        for con in contours:
            if len(con) >= 5 and cv2.contourArea(con) > minArea:
                ellipse = cv2.fitEllipse(con)

                # Draw ellipse
                cv2.ellipse(frame, ellipse, (255, 255, 0), 5)

                # Co-ordinates of extreme points
                extTop = tuple(con[con[:, :, 1].argmin()][0])
                extBot = tuple(con[con[:, :, 1].argmax()][0])
                extLeft = tuple(con[con[:, :, 0].argmin()][0])
                extRight = tuple(con[con[:, :, 0].argmax()][0])

                line1 = math.sqrt((extTop[0] - extBot[0]) * (extTop[0] - extBot[0]) + (extTop[1] - extBot[1]) * (
                            extTop[1] - extBot[1]))
                midPoint = [extTop[0] - int((extTop[0] - extBot[0]) / 2),
                            extTop[1] - int((extTop[1] - extBot[1]) / 2)]
                if line1 > minimumLengthOfLine:
                    if (extTop[0] != extBot[0]):
                        slope = abs(extTop[1] - extBot[1]) / (extTop[0] - extBot[0])

                else:
                    if (extRight[0] != extLeft[0]):
                        slope = abs(extRight[1] - extLeft[1]) / (extRight[0] - extLeft[0])

                originalAngleP = np.arctan((slope1 - slope) / (1 + slope1 * slope))
                originalAngleH = np.arctan(slope)
                originalAngleH = originalAngleH * radianToDegree
                originalAngleP = originalAngleP * radianToDegree

                if (abs(originalAngleP) > minAngle and abs(originalAngleH) < maxAngle and abs(
                        originalAngleP) + abs(originalAngleH) > 89 and abs(
                        originalAngleP) + abs(originalAngleH) < 91):
                    current_time = time.time()
                    if current_time - cooldown_start_time > cooldown_duration:
                        count_fall += 1
                        output_box.insert(tk.END, "Fall detected\n")
                        activity_data["activities"].append({"time": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(current_time)),
                                                             "activity": "Fall"})
                        cooldown_start_time = current_time

        if len(contours) > 0:
            if cv2.contourArea(contours[0]) > 1000:
                current_time = time.time()
                if current_time - cooldown_start_time > cooldown_duration:
                    output_box.insert(tk.END, "Some activity detected\n")
                    activity_data["activities"].append({"time": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(current_time)),
                                                         "activity": "Some activity detected"})
                    cooldown_start_time = current_time

        # Convert the frame to a format compatible with Tkinter
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(frame_rgb)
        imgtk = ImageTk.PhotoImage(image=img)

        # Update the label with the new frame
        label.imgtk = imgtk
        label.configure(image=imgtk)

        # Display the frame in the GUI
        label.pack()

        output_box.update()  # Update output box
        k = cv2.waitKey(30) & 0xff
        if k == 27:
            break

    cap.release()
    cv2.waitKey(1)
    cv2.destroyAllWindows()

def save_report():
    global activity_data
    filename = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON Files", "*.json")])
    if filename:
        with open(filename, "w") as json_file:
            json.dump(activity_data, json_file)

def exit_application():
    root.destroy()

# Tkinter GUI
root = tk.Tk()
root.title("AI Care Monitoring System")
root.geometry("800x800")
# Heading
heading_label = tk.Label(root, text="AI Power Monitoring Care", font=("Arial", 30, "bold"))
heading_label.pack(pady=10)
# Button to select a video
select_button = tk.Button(root, text="Select Video", command=select_video)
select_button.pack()

# Button to run detection
run_button = tk.Button(root, text="Run Detection", command=run_detection)
run_button.pack()

# Output box to display detected activities
output_frame = tk.Frame(root)
output_frame.pack(pady=10)
output_label = tk.Label(output_frame, text="Detected Activities:")
output_label.pack()
output_box = tk.Text(output_frame, height=10, width=30)
output_box.pack()

# Button to save activity report
save_button = tk.Button(root, text="Save Report", command=save_report)
save_button.pack()

# Button to exit application
exit_button = tk.Button(root, text="Exit", command=exit_application)
exit_button.pack()

# Label to display video frames
label = tk.Label(root)
label.pack()

root.mainloop()


# In[ ]:





# In[ ]:





# In[5]:


import cv2
import numpy as np
import math
import time
import json
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

# Global variables
video_path = ""
activity_data = {"activities": []}
output_box = None
count = 0
count1 = 0
slope = 0
slope1 = 100
minArea = 120 * 100
radianToDegree = 57.324
minimumLengthOfLine = 150.0
minAngle = 18
maxAngle = 72
cooldown_duration = 7  # seconds
list_falls = []
count_fall = 0
cooldown_start_time = 0
firstFrame = None

# Function definition for frame Conversion
def convertFrame(frame):
    r = 750.0 / frame.shape[1]
    dim = (750, int(frame.shape[0] * r))
    frame = cv2.resize(frame, dim, interpolation=cv2.INTER_AREA)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (31, 31), 0)
    return frame, gray

def select_video():
    global video_path
    video_path = filedialog.askopenfilename()

def run_detection():
    global video_path, activity_data, output_box, cooldown_start_time, firstFrame

    cap = cv2.VideoCapture(video_path)
    count_fall = 0
    cooldown_start_time = 0
    firstFrame = None

    while True:
        ret, frame = cap.read()
        if frame is None:
            break
        frame, gray = convertFrame(frame)

        # Comparison Frame
        if firstFrame is None:
            time.sleep(1.0)
            _, frame = cap.read()
            frame, gray = convertFrame(frame)
            firstFrame = gray
            continue

        # Frame difference between current and comparison frame
        frameDelta = cv2.absdiff(firstFrame, gray)
        # Thresholding
        thresh1 = cv2.threshold(frameDelta, 20, 255, cv2.THRESH_BINARY)[1]
        # Dilation of Pixels
        thresh = cv2.dilate(thresh1, None, iterations=15)

        # Finding the Region of Interest with changes
        contours, _ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        for con in contours:
            if len(con) >= 5 and cv2.contourArea(con) > minArea:
                ellipse = cv2.fitEllipse(con)

                # Draw ellipse
                cv2.ellipse(frame, ellipse, (255, 255, 0), 5)

                # Co-ordinates of extreme points
                extTop = tuple(con[con[:, :, 1].argmin()][0])
                extBot = tuple(con[con[:, :, 1].argmax()][0])
                extLeft = tuple(con[con[:, :, 0].argmin()][0])
                extRight = tuple(con[con[:, :, 0].argmax()][0])

                line1 = math.sqrt((extTop[0] - extBot[0]) * (extTop[0] - extBot[0]) + (extTop[1] - extBot[1]) * (
                            extTop[1] - extBot[1]))
                midPoint = [extTop[0] - int((extTop[0] - extBot[0]) / 2),
                            extTop[1] - int((extTop[1] - extBot[1]) / 2)]
                if line1 > minimumLengthOfLine:
                    if (extTop[0] != extBot[0]):
                        slope = abs(extTop[1] - extBot[1]) / (extTop[0] - extBot[0])

                else:
                    if (extRight[0] != extLeft[0]):
                        slope = abs(extRight[1] - extLeft[1]) / (extRight[0] - extLeft[0])

                originalAngleP = np.arctan((slope1 - slope) / (1 + slope1 * slope))
                originalAngleH = np.arctan(slope)
                originalAngleH = originalAngleH * radianToDegree
                originalAngleP = originalAngleP * radianToDegree

                if (abs(originalAngleP) > minAngle and abs(originalAngleH) < maxAngle and abs(
                        originalAngleP) + abs(originalAngleH) > 89 and abs(
                        originalAngleP) + abs(originalAngleH) < 91):
                    current_time = time.time()
                    if current_time - cooldown_start_time > cooldown_duration:
                        count_fall += 1
                        output_msg = f"Fall detected - {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(current_time))}\n"
                        output_box.insert(tk.END, output_msg)
                        activity_data["activities"].append({"time": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(current_time)),
                                                             "activity": "Fall"})
                        cooldown_start_time = current_time

        if len(contours) > 0:
            if cv2.contourArea(contours[0]) > 1000:
                current_time = time.time()
                if current_time - cooldown_start_time > cooldown_duration:
                    output_msg = f"Some activity detected - {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(current_time))}\n"
                    output_box.insert(tk.END, output_msg)
                    activity_data["activities"].append({"time": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(current_time)),
                                                         "activity": "Some activity detected"})
                    cooldown_start_time = current_time

        # Convert the frame to a format compatible with Tkinter
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(frame_rgb)
        imgtk = ImageTk.PhotoImage(image=img)

        # Update the label with the new frame
        label.imgtk = imgtk
        label.configure(image=imgtk)

        # Display the frame in the GUI
        label.pack()

        output_box.update()  # Update output box
        k = cv2.waitKey(30) & 0xff
        if k == 27:
            break

    cap.release()
    cv2.waitKey(1)
    cv2.destroyAllWindows()

def save_report():
    global activity_data
    filename = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON Files", "*.json")])
    if filename:
        with open(filename, "w") as json_file:
            json.dump(activity_data, json_file)

def exit_application():
    root.destroy()

# Tkinter GUI
root = tk.Tk()
root.title("AI Care Monitoring System")
root.geometry("800x800")
# Load background image
# Adding background image
bg_image = tk.PhotoImage(file="ss1.png")
bg_label = tk.Label(root, image=bg_image)
bg_label.place(relwidth=1, relheight=1)
# Heading
heading_label = tk.Label(root, text="AI Power Monitoring Care", font=("Arial", 30, "bold"))
heading_label.pack(pady=10)
# Button to select a video
select_button = tk.Button(root, text="Select Video", command=select_video)
select_button.pack()

# Button to run detection
run_button = tk.Button(root, text="Run Detection", command=run_detection)
run_button.pack()

# Output box to display detected activities
output_frame = tk.Frame(root)
output_frame.pack(pady=10)
output_label = tk.Label(output_frame, text="Detected Activities:")
output_label.pack()
output_box = tk.Text(output_frame, height=10, width=30)
output_box.pack()

# Button to save activity report
save_button = tk.Button(root, text="Save Report", command=save_report)
save_button.pack()

# Button to exit application
exit_button = tk.Button(root, text="Exit", command=exit_application)
exit_button.pack()

# Label to display video frames
label = tk.Label(root)
label.pack()

root.mainloop()


# In[1]:





# In[ ]:





# In[ ]:





# In[3]:


import cv2
import numpy as np
import math
import time
import json
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk

# Global variables
video_path = ""
activity_data = {"activities": []}
output_box = None
count = 0
count1 = 0
slope = 0
slope1 = 100
minArea = 120 * 100
radianToDegree = 57.324
minimumLengthOfLine = 150.0
minAngle = 18
maxAngle = 72
cooldown_duration = 7  # seconds
list_falls = []
count_fall = 0
cooldown_start_time = 0
firstFrame = None

# Function definition for frame Conversion
def convertFrame(frame):
    r = 750.0 / frame.shape[1]
    dim = (750, int(frame.shape[0] * r))
    frame = cv2.resize(frame, dim, interpolation=cv2.INTER_AREA)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (31, 31), 0)
    return frame, gray

def login():
    global root, username_entry, password_entry, login_window

    def check_credentials():
        username = username_entry.get()
        password = password_entry.get()
        if username == "aicare" and password == "123":
            login_window.destroy()
            open_main_window()
        else:
            messagebox.showerror("Error", "Invalid username or password")

    login_window = tk.Toplevel(root)
    login_window.title("Login")
    login_window.geometry("300x150")

    username_label = tk.Label(login_window, text="Username:")
    username_label.pack()
    username_entry = tk.Entry(login_window)
    username_entry.pack()

    password_label = tk.Label(login_window, text="Password:")
    password_label.pack()
    password_entry = tk.Entry(login_window, show="*")
    password_entry.pack()

    login_button = tk.Button(login_window, text="Login", command=check_credentials)
    login_button.pack()

def open_main_window():
    global root
    root = tk.Tk()
    root.title("AI Care Monitoring System")
    root.geometry("800x800")

    # Load background image
    # Adding background image
    bg_image = tk.PhotoImage(file="ss1.png")
    bg_label = tk.Label(root, image=bg_image)
    bg_label.place(relwidth=1, relheight=1)

    # Heading
    heading_label = tk.Label(root, text="AI Power Monitoring Care", font=("Arial", 30, "bold"))
    heading_label.pack(pady=10)

    # Button to select a video
    select_button = tk.Button(root, text="Select Video", command=select_video)
    select_button.pack()

    # Button to run detection
    run_button = tk.Button(root, text="Run Detection", command=run_detection)
    run_button.pack()

    # Output box to display detected activities
    output_frame = tk.Frame(root)
    output_frame.pack(pady=10)
    output_label = tk.Label(output_frame, text="Detected Activities:")
    output_label.pack()
    output_box = tk.Text(output_frame, height=10, width=30)
    output_box.pack()

    # Button to save activity report
    save_button = tk.Button(root, text="Save Report", command=save_report)
    save_button.pack()

    # Button to exit application
    exit_button = tk.Button(root, text="Exit", command=exit_application)
    exit_button.pack()

    # Label to display video frames
    label = tk.Label(root)
    label.pack()

    root.mainloop()

def select_video():
    global video_path
    video_path = filedialog.askopenfilename()

def run_detection():
    global video_path, activity_data, output_box, cooldown_start_time, firstFrame

    cap = cv2.VideoCapture(video_path)
    count_fall = 0
    cooldown_start_time = 0
    firstFrame = None

    while True:
        ret, frame = cap.read()
        if frame is None:
            break
        frame, gray = convertFrame(frame)

        # Comparison Frame
        if firstFrame is None:
            time.sleep(1.0)
            _, frame = cap.read()
            frame, gray = convertFrame(frame)
            firstFrame = gray
            continue

        # Frame difference between current and comparison frame
        frameDelta = cv2.absdiff(firstFrame, gray)
        # Thresholding
        thresh1 = cv2.threshold(frameDelta, 20, 255, cv2.THRESH_BINARY)[1]
        # Dilation of Pixels
        thresh = cv2.dilate(thresh1, None, iterations=15)

        # Finding the Region of Interest with changes
        contours, _ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        for con in contours:
            if len(con) >= 5 and cv2.contourArea(con) > minArea:
                ellipse = cv2.fitEllipse(con)

                # Draw ellipse
                cv2.ellipse(frame, ellipse, (255, 255, 0), 5)

                # Co-ordinates of extreme points
                extTop = tuple(con[con[:, :, 1].argmin()][0])
                extBot = tuple(con[con[:, :, 1].argmax()][0])
                extLeft = tuple(con[con[:, :, 0].argmin()][0])
                extRight = tuple(con[con[:, :, 0].argmax()][0])

                line1 = math.sqrt((extTop[0] - extBot[0]) * (extTop[0] - extBot[0]) + (extTop[1] - extBot[1]) * (
                            extTop[1] - extBot[1]))
                midPoint = [extTop[0] - int((extTop[0] - extBot[0]) / 2),
                            extTop[1] - int((extTop[1] - extBot[1]) / 2)]
                if line1 > minimumLengthOfLine:
                    if (extTop[0] != extBot[0]):
                        slope = abs(extTop[1] - extBot[1]) / (extTop[0] - extBot[0])

                else:
                    if (extRight[0] != extLeft[0]):
                        slope = abs(extRight[1] - extLeft[1]) / (extRight[0] - extLeft[0])

                originalAngleP = np.arctan((slope1 - slope) / (1 + slope1 * slope))
                originalAngleH = np.arctan(slope)
                originalAngleH = originalAngleH * radianToDegree
                originalAngleP = originalAngleP * radianToDegree

                if (abs(originalAngleP) > minAngle and abs(originalAngleH) < maxAngle and abs(
                        originalAngleP) + abs(originalAngleH) > 89 and abs(
                        originalAngleP) + abs(originalAngleH) < 91):
                    current_time = time.time()
                    if current_time - cooldown_start_time > cooldown_duration:
                        count_fall += 1
                        output_msg = f"Fall detected - {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(current_time))}\n"
                        output_box.insert(tk.END, output_msg)
                        activity_data["activities"].append({"time": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(current_time)),
                                                             "activity": "Fall"})
                        cooldown_start_time = current_time

        if len(contours) > 0:
            if cv2.contourArea(contours[0]) > 1000:
                current_time = time.time()
                if current_time - cooldown_start_time > cooldown_duration:
                    output_msg = f"Some activity detected - {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(current_time))}\n"
                    output_box.insert(tk.END, output_msg)
                    activity_data["activities"].append({"time": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(current_time)),
                                                         "activity": "Some activity detected"})
                    cooldown_start_time = current_time

        # Convert the frame to a format compatible with Tkinter
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(frame_rgb)
        imgtk = ImageTk.PhotoImage(image=img)

        # Update the label with the new frame
        label.imgtk = imgtk
        label.configure(image=imgtk)

        # Display the frame in the GUI
        label.pack()

        output_box.update()  # Update output box
        k = cv2.waitKey(30) & 0xff
        if k == 27:
            break

    cap.release()
    cv2.waitKey(1)
    cv2.destroyAllWindows()

def save_report():
    global activity_data
    filename = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON Files", "*.json")])
    if filename:
        with open(filename, "w") as json_file:
            json.dump(activity_data, json_file)

def exit_application():
    root.destroy()

# Main code
login()


# In[2]:


import cv2
import numpy as np
import math
import time
import json
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk

# Global variables
video_path = ""
activity_data = {"activities": []}
output_box = None
count = 0
count1 = 0
slope = 0
slope1 = 100
minArea = 120 * 100
radianToDegree = 57.324
minimumLengthOfLine = 150.0
minAngle = 18
maxAngle = 72
cooldown_duration = 7  # seconds
list_falls = []
count_fall = 0
cooldown_start_time = 0
firstFrame = None

# Function definition for frame Conversion
def convertFrame(frame):
    r = 750.0 / frame.shape[1]
    dim = (750, int(frame.shape[0] * r))
    frame = cv2.resize(frame, dim, interpolation=cv2.INTER_AREA)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (31, 31), 0)
    return frame, gray

def login():
    global root, username_entry, password_entry, login_window

    def check_credentials():
        username = username_entry.get()
        password = password_entry.get()
        if username == "aicare" and password == "123":
            login_window.destroy()
            open_main_window()
        else:
            messagebox.showerror("Error", "Invalid username or password")

    login_window = tk.Toplevel()
    login_window.title("Login")
    login_window.geometry("300x150")

    username_label = tk.Label(login_window, text="Username:")
    username_label.pack()
    username_entry = tk.Entry(login_window)
    username_entry.pack()

    password_label = tk.Label(login_window, text="Password:")
    password_label.pack()
    password_entry = tk.Entry(login_window, show="*")
    password_entry.pack()

    login_button = tk.Button(login_window, text="Login", command=check_credentials)
    login_button.pack()

def open_main_window():
    global root
    root = tk.Tk()
    root.title("AI Care Monitoring System")
    root.geometry("800x800")

    # Load background image
    bg_image = tk.PhotoImage(file="ss1.png")
    bg_label = tk.Label(root, image=bg_image)
    bg_label.place(relwidth=1, relheight=1)

    # Heading
    heading_label = tk.Label(root, text="AI Power Monitoring Care", font=("Arial", 30, "bold"))
    heading_label.pack(pady=10)

    # Button to select a video
    select_button = tk.Button(root, text="Select Video", command=select_video)
    select_button.pack()

    # Button to run detection
    run_button = tk.Button(root, text="Run Detection", command=run_detection)
    run_button.pack()

    # Output box to display detected activities
    output_frame = tk.Frame(root)
    output_frame.pack(pady=10)
    output_label = tk.Label(output_frame, text="Detected Activities:")
    output_label.pack()
    output_box = tk.Text(output_frame, height=10, width=30)
    output_box.pack()

    # Button to save activity report
    save_button = tk.Button(root, text="Save Report", command=save_report)
    save_button.pack()

    # Button to exit application
    exit_button = tk.Button(root, text="Exit", command=exit_application)
    exit_button.pack()

    # Label to display video frames
    label = tk.Label(root)
    label.pack()

    root.mainloop()

def select_video():
    global video_path
    video_path = filedialog.askopenfilename()

def run_detection():
    global video_path, activity_data, output_box, cooldown_start_time, firstFrame

    cap = cv2.VideoCapture(video_path)
    count_fall = 0
    cooldown_start_time = 0
    firstFrame = None

    while True:
        ret, frame = cap.read()
        if frame is None:
            break
        frame, gray = convertFrame(frame)

        # Comparison Frame
        if firstFrame is None:
            time.sleep(1.0)
            _, frame = cap.read()
            frame, gray = convertFrame(frame)
            firstFrame = gray
            continue

        # Frame difference between current and comparison frame
        frameDelta = cv2.absdiff(firstFrame, gray)
        # Thresholding
        thresh1 = cv2.threshold(frameDelta, 20, 255, cv2.THRESH_BINARY)[1]
        # Dilation of Pixels
        thresh = cv2.dilate(thresh1, None, iterations=15)

        # Finding the Region of Interest with changes
        contours, _ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        for con in contours:
            if len(con) >= 5 and cv2.contourArea(con) > minArea:
                ellipse = cv2.fitEllipse(con)

                # Draw ellipse
                cv2.ellipse(frame, ellipse, (255, 255, 0), 5)

                # Co-ordinates of extreme points
                extTop = tuple(con[con[:, :, 1].argmin()][0])
                extBot = tuple(con[con[:, :, 1].argmax()][0])
                extLeft = tuple(con[con[:, :, 0].argmin()][0])
                extRight = tuple(con[con[:, :, 0].argmax()][0])

                line1 = math.sqrt((extTop[0] - extBot[0]) * (extTop[0] - extBot[0]) + (extTop[1] - extBot[1]) * (
                            extTop[1] - extBot[1]))
                midPoint = [extTop[0] - int((extTop[0] - extBot[0]) / 2),
                            extTop[1] - int((extTop[1] - extBot[1]) / 2)]
                if line1 > minimumLengthOfLine:
                    if (extTop[0] != extBot[0]):
                        slope = abs(extTop[1] - extBot[1]) / (extTop[0] - extBot[0])

                else:
                    if (extRight[0] != extLeft[0]):
                        slope = abs(extRight[1] - extLeft[1]) / (extRight[0] - extLeft[0])

                originalAngleP = np.arctan((slope1 - slope) / (1 + slope1 * slope))
                originalAngleH = np.arctan(slope)
                originalAngleH = originalAngleH * radianToDegree
                originalAngleP = originalAngleP * radianToDegree

                if (abs(originalAngleP) > minAngle and abs(originalAngleH) < maxAngle and abs(
                        originalAngleP) + abs(originalAngleH) > 89 and abs(
                        originalAngleP) + abs(originalAngleH) < 91):
                    current_time = time.time()
                    if current_time - cooldown_start_time > cooldown_duration:
                        count_fall += 1
                        output_msg = f"Fall detected - {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(current_time))}\n"
                        output_box.insert(tk.END, output_msg)
                        activity_data["activities"].append({"time": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(current_time)),
                                                             "activity": "Fall"})
                        cooldown_start_time = current_time

        if len(contours) > 0:
            if cv2.contourArea(contours[0]) > 1000:
                current_time = time.time()
                if current_time - cooldown_start_time > cooldown_duration:
                    output_msg = f"Some activity detected - {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(current_time))}\n"
                    output_box.insert(tk.END, output_msg)
                    activity_data["activities"].append({"time": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(current_time)),
                                                         "activity": "Some activity detected"})
                    cooldown_start_time = current_time

        # Convert the frame to a format compatible with Tkinter
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(frame_rgb)
        imgtk = ImageTk.PhotoImage(image=img)

        # Update the label with the new frame
        label.imgtk = imgtk
        label.configure(image=imgtk)

        # Display the frame in the GUI
        label.pack()

        output_box.update()  # Update output box
        k = cv2.waitKey(30) & 0xff
        if k == 27:
            break

    cap.release()
    cv2.waitKey(1)
    cv2.destroyAllWindows()

def save_report():
    global activity_data
    filename = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON Files", "*.json")])
    if filename:
        with open(filename, "w") as json_file:
            json.dump(activity_data, json_file)

def exit_application():
    root.destroy()

# Main code
login()


# In[ ]:




