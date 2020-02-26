from tkinter import *
from tkinter import ttk
import tkinter.messagebox
import cv2
import os

#_______________________________________________________________________________________________________________________
window = Tk()
window.title("บันทึกใบหน้า")
window.geometry('890x500')
window.option_add("*Font", "import 17")
window.configure(bg='#ffffff')
Label(text="บันทึกใบหน้า", bg='#ffffff').grid(row=0)
Label(bg='#ffffff').grid(row=1)
Label(bg='#ffffff').grid(row=2)


Label(window, text="สาขา  ", width=20, bg='#ffffff').grid(row=3, column=1)
txt = ttk.Combobox(window,  values=['CS', 'PH'], width=20)
txt.current()
txt.grid(row=3, column=2)
Label(bg='#ffffff').grid(row=4)


Label(window, text="รุ่นที่  ", width=20, bg='#ffffff').grid(row=5, column=1)
txt1 = ttk.Combobox(window, values=list(range(2560, 2571)), width=20)
txt1.current()
txt1.grid(row=5, column=2)
Label(bg='#ffffff').grid(row=6)


Label(text="ชื่อ  ", width=20, bg='#ffffff').grid(row=7, column=1)
txt2 = Entry(window, width=21, bg='#ffffff')
txt2.grid(row=7, column=2)
Label(bg='#ffffff').grid(row=8)


Label(window, text="รหัสนักศึกษา  ", width=20, bg='#ffffff').grid(row=9, column=1)
txt3 = Entry(window, width=21, bg='#ffffff')
txt3.grid(row=9, column=2)
Label(bg='#ffffff').grid(row=10)
def resets():
    txt.set("")
    txt1.set("")
    txt2.delete(0, 'end')
    txt3.delete(0, 'end')


#_______________________________________________________________________________________________________________________
def submit():
    webcam = cv2.VideoCapture(0)
    count = 1
    branch = (txt.get())
    class_ = (txt1.get())
    name = (txt2.get())
    id = (txt3.get())
    tkinter.messagebox.askokcancel('ตรวจสอบข้อมูล', name + " " + branch + "  รหัสนักศึกษา  " + id)
    path = os.path.join('branch ' + branch, class_, name)
    if not os.path.isdir(path):
          os.mkdir(path)
          (width, height) = (530, 500)
          haar_file = 'haarcascade_frontalface_default.xml'
          face_cascade = cv2.CascadeClassifier(haar_file)
          while count < 31:
                red, im = webcam.read()
                gray = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)
                faces = face_cascade.detectMultiScale(gray, 1.3, 4)
                cv2.putText(im, name, (8, 35), cv2.FONT_HERSHEY_COMPLEX, 0.9, (0, 0, 0), 1)
                for (x, y, w, h) in faces:
                    cv2.rectangle(im, (x, y), (x+w, y+h), (255, 0, 0), 2)
                    face = gray[y-150:y+h+150, x-100:x+w+100][:, :, ::-1]
                    face_resize = cv2.resize(face, (width, height))
                    cv2.imwrite('%s/%s %s %s %s_%s.jpg.jpg' % (path, id, name, branch, class_, count), face_resize)
                    count += 1
                    res = "ทำการบันทึกข้อมุลเสร็จสิ้น"
                    message.configure(text=res)
                    txt.set("")
                    txt1.set("")
                    txt2.delete(0, 'end')
                    txt3.delete(0, 'end')
                cv2.imshow(name + ' ' + branch + ' ' + class_, im)
                cv2.waitKey(30)


#_______________________________________________________________________________________________________________________
Label(text="ปล. (ข้อมูลต้องเป็นนภาษาอักกฤษ)", fg="blue", bg="#ffffff").grid(row=10, column=2)
submit = Button(window, text="OK", bg="blue", fg="#ffffff", width=8, command=submit)
submit.grid(row=11, column=4)

reset = Button(window, text="Reset", bg="#ffffff", width=8, command=resets)
reset.grid(row=11, column=5)

message = Label(window, text="", fg="green", bg="#ffffff")
message.grid(row=12, column=2)

window.mainloop()

