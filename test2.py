import numpy as np, cv2, dlib, os, pickle
from tkinter import *
from tkinter import ttk

window = Tk()
window.geometry("800x600")
window.option_add("*font", "import 17")
window.config(bg="#ffffff")
Label(bg="#ffffff").grid(row=0, column=0)
Label(bg="#ffffff").grid(row=0, column=0)
Label(window, text='สาขา  ', bg="#ffffff").grid(row=1, column=1)
txt = ttk.Combobox(values=['CS', 'PH'], width=20)
txt.current()
txt.grid(row=1, column=2)
Label(bg="#ffffff").grid(row=2)

Label(window, text='รุ่น   ', bg="#ffffff").grid(row=3, column=1)
txt1 = ttk.Combobox(window, values=list(range(2560, 2571)), width=20)
txt1.current()
txt1.grid(row=3, column=2)
Label(bg="#ffffff").grid(row=4)

def submit():
   name_file = (txt.get())
   sub_file = (txt1.get())
   hon = "branch "
   path = './' + hon + name_file + '/' + sub_file + '/'
   detector = dlib.get_frontal_face_detector()
   sp = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')
   model = dlib.face_recognition_model_v1('dlib_face_recognition_resnet_model_v1.dat')
   print('file name : ' + name_file + '_' + sub_file + '.pk  loading...สักครู่ ')
   FACE_DESC = []
   FACE_NAME = []
   for fn in os.listdir(path):
       if fn.endswith('.jpg'):
            img = cv2.imread(path + fn)[:, :, ::-1]
            img1 = cv2.imread(path + fn)
            dets = detector(img, 1)
            for k, d in enumerate(dets):
                 shape = sp (img, d)
                 face_desc = model.compute_face_descriptor(img, shape, 1)
                 FACE_DESC.append(face_desc)
                 print('loading...', fn)
                 FACE_NAME.append(fn[:fn.index('_')])
                 r = 'ดำเนิดงานเสร็จสิ้น'
                 txt2.configure(text=r)
                 cv2.imshow('loading', img1)
                 cv2.waitKey(1)
                 pickle.dump((FACE_DESC, FACE_NAME), open('datasets\\' + name_file + '_' + sub_file + '.pk', 'wb'))



submit = Button(window, text='submit', command=submit)
submit.grid(row=5, column=3)
Label(window,).grid(row=6)

txt2 = Label(window, text="", bg="#ffffff", fg="blue")
txt2.grid(row=10, column=2)

window.mainloop()
