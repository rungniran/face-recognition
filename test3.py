import cv2, numpy as np, dlib, pickle
import datetime
import os
import csv
from tkinter import *
from tkinter import ttk





#_______________________________________________________________________________________________________________________
window = Tk()
window.title("ตรวจสอบใบหน้า")
window.geometry('890x500')
window.option_add("*Font", "import 17")
window.configure(bg="#ffffff")
Label(bg="#ffffff", text="ตรวจจับใบหน้า").grid(row=0)
Label(bg="#ffffff").grid(row=1)
Label(bg="#ffffff").grid(row=2)


Label(window, text="วิชา  ", width=20, bg="#ffffff").grid(row=3, column=1)
txt = Entry(window, width=21)
txt.grid(row=3, column=2)
Label(bg="#ffffff").grid(row=4)


Label(window, text="สาขา  ",  width=20, bg="#ffffff").grid(row=5, column=1)
txt1 = ttk.Combobox(window, values=['CS', 'PH'], width=20)
txt1.grid(row=5, column=2)
Label(bg="#ffffff").grid(row=6)


Label(window, text="รุ่นที่  ", width=20, bg="#ffffff").grid(row=7, column=1)
txt2 = ttk.Combobox(window, values=list(range(2560, 2571)), width=20,)
txt2.current()
txt2.grid(row=7, column=2)
Label(bg="#ffffff").grid(row=8)


#_______________________________________________________________________________________________________________________
def submit():
    sub_j = (txt.get())
    name_branch = (txt1.get())
    class_ = (txt2.get())
    webcap = cv2.VideoCapture(0)
    time = datetime.datetime.now()
    datasets = 'database\\' + sub_j + " " + time.strftime("%d-%m-%Y")
    path = os.path.join(datasets)
    if not os.path.isdir(path):
         os.mkdir(path)
         face_detector = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
         detector = dlib.get_frontal_face_detector()
         sp = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')
         model = dlib.face_recognition_model_v1('dlib_face_recognition_resnet_model_v1.dat')
         FACE_DESC, FACE_NAME = pickle.load(open('datasets\\'+name_branch + '_' + class_+'.pk', 'rb'))
         while (True):
              _, frame = webcap.read()
              time1 = datetime.datetime.now()
              cv2.line(frame, (0, 20), (650, 20), (255, 128, 0), 50)
              cv2.putText(frame, ('subject : ') + sub_j + time1.strftime(" (%d/%m/%Y)"), (7, 30), cv2.FONT_HERSHEY_COMPLEX, 0.6, (255, 255, 255), 1)
              gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
              faces = face_detector.detectMultiScale(gray, 1.3, 5)
              for(x, y, w, h) in faces:
                   img = frame[y-10:y+h+10, x-10:x+w+10][:, :, ::-1]
                   dets = detector(img, 1)
                   for k, d in enumerate(dets):
                        shape = sp(img, d)
                        face_desc0 = model.compute_face_descriptor(img, shape, 1)
                        d = []
                        for face_desc in FACE_DESC:
                             d.append(np.linalg.norm(np.array(face_desc) - np.array(face_desc0)))
                             idx = np.argmin(d)
                             if d[idx] < 0.5:
                                  name = FACE_NAME[idx]
                                  times = datetime.datetime.now()
                                  print(name)
                                  cv2.putText(frame, name[10:30], (x, y-10), cv2.FONT_HERSHEY_COMPLEX, 0.6, (255, 128, 0), 1)
                                  cv2.rectangle(frame, (x, y), (x + w, y + h), (200, 128, 0), 2)
                                  cv2.imwrite('%s/%s.jpg' % (path, name[10:30]), frame)
                                  with open('database\\' + sub_j + " " + time.strftime("%d-%m-%Y") + '\\' + time.strftime("%d-%m-%Y") + '.csv', 'a', newline="") as file:
                                       writer = csv.writer(file)
                                       writer.writerow([name[0:9], name[10:30] + "  เข้าเวลา  " + times.strftime("%H") + "น."])
              cv2.imshow(sub_j + ' ' + name_branch + ' ' + class_, frame)
              cv2.waitKey(1)


#_______________________________________________________________________________________________________________________
Label(text="ปล. (ข้อมูลต้องเป็นนภาษาอักกฤษ)", fg="blue", bg="#ffffff").grid(row=9, column=2)
button = Button(window, text="OK", bg="#0080ff", fg="#ffffff", width=8, command=submit)
button.grid(row=9, column=3)

window.mainloop()