from tkinter import*
from tkinter import ttk
from PIL import Image,ImageTk
from tkinter import messagebox
from student import Student
from attendence import Attendence
from developer import Devoloper
from help_desk import Helpdesk
import cv2
import mysql.connector 
import numpy as np
import os
from time import strftime
from datetime import datetime

class Face_Recognition_System:
    def __init__(self,root):
        self.root=root
        self.root.geometry("1530x790+0+0")
        self.root.title("Face Recognition System")
        
        # # Put imagees into the webpage
        # img1 = Image.open(r'D:\wobot_ai\HardHat_Dataset\images\hard_hat_workers62.png')
        # img1 = img1.resize((1530,130),Image.ANTIALIAS)
        # self.photoimg1=ImageTk.PhotoImage(img1)
        
        # lab1 = Label(self.root,image=self.photoimg1)
        # lab1.place(x=0,y=0,width=1530,height=130)
        
        title_lev_= Label(self.root,text="IIT Kharagpur",font=('times new roman',45,'bold'),bg="blue",fg="white")
        title_lev_.place(x=0,y=0,width=1530,height=130)
        
        
        # img2
        # Put imagees into the webpage
        # img2 = Image.open(r'D:\wobot_ai\HardHat_Dataset\images\hard_hat_workers101.png')
        # img2 = img2.resize((500,130),Image.ANTIALIAS)
        # self.photoimg2=ImageTk.PhotoImage(img2)
        
        # lab2 = Label(self.root,image=self.photoimg2)
        # lab2.place(x=500,y=0,width=500,height=130)
        
        # # Put imagees into the webpage
        # img3 = Image.open(r'D:\wobot_ai\HardHat_Dataset\images\hard_hat_workers67.png')
        # img3 = img3.resize((530,130),Image.ANTIALIAS)
        # self.photoimg3=ImageTk.PhotoImage(img3)
        
        # lab3 = Label(self.root,image=self.photoimg3)
        # lab3.place(x=1000,y=0,width=530,height=130)
        
        # Put background image
        img4 = Image.open(r'E:\student_management\photo\vadim-sherbakov-d6ebY-faOO0-unsplash.jpg')
        img4 = img4.resize((1530,660),Image.ANTIALIAS)
        self.photoimg4=ImageTk.PhotoImage(img4)
        
        bg_img = Label(self.root,image=self.photoimg4)
        bg_img.place(x=0,y=130,width=1530,height=660)
        
        
        ########## Adding title into back ground images 
        title_lev= Label(bg_img,text="Auto Attendence System",font=('times new roman',35,'bold'),bg="gold",fg="red")
        title_lev.place(x=0,y=0,width=1530,height=45)
        
        
        #===== Adding Time ==========
        def time():
            string=strftime("%H:%M:%S")
            lbl.config(text=string)
            lbl.after(1000,time)
        lbl=Label(title_lev,font=('times new roman',15,'bold'),bg="gold",fg="Blue")
        lbl.place(x=55,y=0,width=110,height=50)
        time()
        ######### Student button 
        img5 = Image.open(r'E:\student_management\photo\omar-lopez-nomivMNW07o-unsplash.jpg')
        img5 = img5.resize((220,220),Image.ANTIALIAS)
        self.photoimg5=ImageTk.PhotoImage(img5)
        
        button1= Button(bg_img,image=self.photoimg5,command=self.student_derails ,cursor="hand2")
        button1.place(x=200,y=100,width=220,height=220)
        
        button1_1=Button(bg_img,text="Student Details",command=self.student_derails,font=('times new roman',15,'bold'),bg="Blue",fg="white")
        button1_1.place(x=200,y=300,width=220,height=40)
        
        ######### Face detector button 
        img6 = Image.open(r'E:\student_management\photo\man-face-recognition-concept-92721828.jpg')
        img6 = img6.resize((220,220),Image.ANTIALIAS)
        self.photoimg6=ImageTk.PhotoImage(img6)
        
        button2= Button(bg_img,image=self.photoimg6,cursor="hand2",command=self.face_recog)
        button2.place(x=500,y=100,width=220,height=220)
        
        button2_1=Button(bg_img,text="Face Detector",command=self.face_recog,font=('times new roman',15,'bold'),bg="Blue",fg="white")
        button2_1.place(x=500,y=300,width=220,height=40)
        
        ######### Attendence button 
        img7 = Image.open(r'E:\student_management\photo\pexels-pavel-danilyuk-8423046.jpg')
        img7 = img7.resize((220,220),Image.ANTIALIAS)
        self.photoimg7=ImageTk.PhotoImage(img7)
        
        button3= Button(bg_img,image=self.photoimg7,cursor="hand2",command=self.attence_derails)
        button3.place(x=800,y=100,width=220,height=220)
        
        button3_1=Button(bg_img,text="Attendence",command=self.attence_derails,font=('times new roman',15,'bold'),bg="Blue",fg="white")
        button3_1.place(x=800,y=300,width=220,height=40)
        
        ######### Help Desk button 
        img8 = Image.open(r'E:\student_management\photo\young-help-desk-operator-working-office-161497428.jpg')
        img8 = img8.resize((220,220),Image.ANTIALIAS)
        self.photoimg8=ImageTk.PhotoImage(img8)
        
        button4= Button(bg_img,image=self.photoimg8,cursor="hand2",command=self.helpDesk_derails)
        button4.place(x=1100,y=100,width=220,height=220)
        
        button4_1=Button(bg_img,text="Help Desk",command=self.helpDesk_derails,font=('times new roman',15,'bold'),bg="Blue",fg="white")
        button4_1.place(x=1100,y=300,width=220,height=40)
        
        ######### train face button 
        img9 = Image.open(r'E:\student_management\photo\1_lpv2o0GGqMO1zlGp_-q23Q.png')
        img9 = img9.resize((220,220),Image.ANTIALIAS)
        self.photoimg9=ImageTk.PhotoImage(img9)
        
        button5= Button(bg_img,image=self.photoimg9,command=self.train_classifire,cursor="hand2")
        button5.place(x=200,y=390,width=220,height=220)
        
        button5_1=Button(bg_img,text="Train Face",command=self.train_classifire,font=('times new roman',15,'bold'),bg="Blue",fg="white")
        button5_1.place(x=200,y=590,width=220,height=40)
        
        ######### Photos button 
        img10 = Image.open(r'D:\my photos\PicsArt_08-29-05.00.23.jpg')
        img10 = img10.resize((220,220),Image.ANTIALIAS)
        self.photoimg10=ImageTk.PhotoImage(img10)
        
        button6= Button(bg_img,image=self.photoimg10,cursor="hand2",command=self.open_img)
        button6.place(x=500,y=390,width=220,height=220)
        
        button6_1=Button(bg_img,text="Photos",command=self.open_img,font=('times new roman',15,'bold'),bg="Blue",fg="white")
        button6_1.place(x=500,y=590,width=220,height=40)
        
        ######### Developer button 
        img11 = Image.open(r'E:\student_management\photo\dev2.jpg')
        img11 = img11.resize((220,220),Image.ANTIALIAS)
        self.photoimg11=ImageTk.PhotoImage(img11)
        
        button7= Button(bg_img,image=self.photoimg11,cursor="hand2",command=self.developer_derails)
        button7.place(x=800,y=390,width=220,height=220)
        
        button7_1=Button(bg_img,text="Developer",command=self.developer_derails,font=('times new roman',15,'bold'),bg="Blue",fg="white")
        button7_1.place(x=800,y=590,width=220,height=40)
        
        ######### Exit button 
        img12 = Image.open(r'E:\student_management\photo\1200px-Glass_exit_sign.jpg')
        img12 = img12.resize((220,220),Image.ANTIALIAS)
        self.photoimg12=ImageTk.PhotoImage(img12)
        
        button8= Button(bg_img,image=self.photoimg12,cursor="hand2",command=self.ifExit)
        button8.place(x=1100,y=390,width=220,height=220)
        
        button8_1=Button(bg_img,command=self.ifExit,text="EXIT",font=('times new roman',15,'bold'),bg="Blue",fg="white")
        button8_1.place(x=1100,y=590,width=220,height=40)
        
        
        
    ##Photo tab
    def open_img(self):
        os.startfile("student_image")   
    
    def ifExit(self):
        self.ifExit=messagebox.askyesno("Face Recognization","Are you sure exit this page",parent=self.root)
        if self.ifExit>0:
            self.root.destroy()
        else:
            return
    # ============== Function Buttons ============================
    def student_derails(self):
        self.new_window=Toplevel(self.root)
        self.app=Student(self.new_window)
        
    def attence_derails(self):
        self.new_window=Toplevel(self.root)
        self.app=Attendence(self.new_window)
        
    def developer_derails(self):
        self.new_window=Toplevel(self.root)
        self.app=Devoloper(self.new_window)
        
    def helpDesk_derails(self):
        self.new_window=Toplevel(self.root)
        self.app=Helpdesk(self.new_window)
        
        
    ### Creating function for training 
    def train_classifire(self):
        data_dir=("student_image")
        path=[os.path.join(data_dir,file) for file in os.listdir(data_dir)]
        faces=[]
        ids=[]
        
        for image in path:
            img=Image.open(image).convert("L") # convert gray scale
            imageNp=np.array(img,"uint8")
            id_=int(os.path.split(image)[1].split(".")[1])
            
            faces.append(imageNp)
            ids.append(id_)
            cv2.imshow("Training",imageNp)
            cv2.waitKey(1)==13
        ids_=np.array(ids)
        # =================== tranin classifire
        clf=cv2.face.LBPHFaceRecognizer_create()
        clf.train(faces,ids_)
        clf.write("classifier.xml")
        cv2.destroyAllWindows()
        messagebox.showinfo("Results","Training dataset is completed")
        
    # =============== Attendance =======================
    def mark_attendance(self,i,r,n,d):
        with open("student.csv","r+",newline="\n") as f:
            myDatalist=f.readlines()
            name_list=[]
            for line in myDatalist:
                entry=line.split(",")
                name_list.append(entry[0])
            if (i not in name_list) and (r not in name_list) and (n not in name_list) and (d not in name_list):
                now=datetime.now()
                d1=now.strftime("%d/%m/%Y")
                dtString=now.strftime("%H:%M:%S")
                f.writelines(f"\n{i},{r},{n},{d},{dtString},{d1},present")
    
    
    ### Detect face function 
    def face_recog(self):
        def draw_boundray(img,classifier,ScaleFactor,minNeighbors,color,text,clf):
            gray_image=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
            features=classifier.detectMultiScale(gray_image,ScaleFactor,minNeighbors)
            coord=[]
            for (x,y,w,h) in features:
                cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),3)
                id,predict=clf.predict(gray_image[y:y+h,x:x+h])
                confidence=int((100*(1-predict/300)))
                
                
                conn=mysql.connector.connect(host="localhost",user="root",passwd="root",database="face_recognizer",auth_plugin = 'mysql_native_password')
                my_cursor=conn.cursor()
                
                my_cursor.execute("SELECT Student_name from students where Student_ID="+str(id))
                n=my_cursor.fetchone()
                n="+".join(n)
                
                my_cursor.execute("SELECT Roll_no from students where Student_ID ="+str(id))
                r=my_cursor.fetchone()
                r="+".join(r)
                
                my_cursor.execute("SELECT Department from students where Student_ID ="+str(id))
                d=my_cursor.fetchone()
                d="+".join(d)
                
                my_cursor.execute("SELECT Student_ID from students where Student_ID ="+str(id))
                i=my_cursor.fetchone()
                i="+".join(i)
                
                
                
                
                if confidence>77:
                    cv2.putText(img,f"Roll: {r}",(x,y-55),cv2.FONT_HERSHEY_COMPLEX,0.8,(255,255,255),2)
                    cv2.putText(img,f"Name: {n}",(x,y-40),cv2.FONT_HERSHEY_COMPLEX,0.8,(255,255,255),2)
                    cv2.putText(img,f"Student_ID: {i}",(x,y-25),cv2.FONT_HERSHEY_COMPLEX,0.8,(255,255,255),2)
                    cv2.putText(img,f"Department: {d}",(x,y-5),cv2.FONT_HERSHEY_COMPLEX,0.8,(255,255,255),2)
                    self.mark_attendance(i,r,n,d)
                else:
                    cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),3)
                    cv2.putText(img,"Unknown_face",(x,y-55),cv2.FONT_HERSHEY_COMPLEX,0.8,(0,0,255),2)
                coord=[x,y,w,h]
            return coord
        def recognize(img,clf,faceCascade):
            coord=draw_boundray(img,faceCascade,1.1,10,(255,255,255),"Face",clf)
            return img
        faceCascade=cv2.CascadeClassifier(r'E:\student_management\student\Lib\site-packages\cv2\data\haarcascade_frontalface_default.xml')
        clf=cv2.face.LBPHFaceRecognizer_create()
        clf.read("classifier.xml") 
        
        video_cap=cv2.VideoCapture(0)
        
        while True:
            ret,frame=video_cap.read()
            img=recognize(frame,clf,faceCascade)
            cv2.imshow("Welcome to face Recognization",img)
            if cv2.waitKey(1)==13:
                break
        video_cap.release()
        cv2.destroyAllWindows()   
                    
                    
        

if __name__=="__main__":
    root=Tk()
    obj = Face_Recognition_System(root)
    root.mainloop()
     