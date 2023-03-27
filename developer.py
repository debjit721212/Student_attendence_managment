from tkinter import*
from tkinter import ttk
from PIL import Image,ImageTk
from tkinter import messagebox
import mysql.connector 
import cv2

class Devoloper:
    def __init__(self,root):
        self.root=root
        self.root.geometry("1530x790+0+0")
        self.root.title("Developer")
        
        title_lev_= Label(self.root,text="Welcome to Developer Page",font=('times new roman',45,'bold'),bg="skyblue",fg="white")
        title_lev_.place(x=0,y=0,width=1530,height=120)
        
        #####
        ### Creating main frame
        main_frame= Frame(self.root,bd=3,bg="white")
        main_frame.place(x=257,y=135,width=1000,height=600)
        
        # attendence_id
        text1_lable= Label(main_frame,text="Hello!",font=('times new roman',13,'bold'),bg='white')
        text1_lable.grid(row=0,column=0,padx=10,pady=7,sticky=W)
        
        text1_lable= Label(main_frame,text="Greetings of the day.",font=('times new roman',13,'bold'),bg='white')
        text1_lable.grid(row=1,column=0,padx=10,pady=7,sticky=W)
        
        text1_lable= Label(main_frame,text="I'm Debjit Adak.I'm a Data Scientist.",font=('times new roman',13,'bold'),bg='white')
        text1_lable.grid(row=2,column=0,padx=10,pady=7,sticky=W)
        
        text1_lable= Label(main_frame,text="My area of interest is Computer Vision and NLP.",font=('times new roman',13,'bold'),bg='white')
        text1_lable.grid(row=3,column=0,padx=10,pady=7,sticky=W)
        
        text1_lable= Label(main_frame,text="Anyone can reach out to me through email.",font=('times new roman',13,'bold'),bg='white')
        text1_lable.grid(row=4,column=0,padx=10,pady=7,sticky=W)
        
        text1_lable= Label(main_frame,text="My email id is debjit721212@gmail.com",font=('times new roman',13,'bold'),bg='white')
        text1_lable.grid(row=5,column=0,padx=10,pady=7,sticky=W)






if __name__=="__main__":
    root=Tk()
    obj = Devoloper(root)
    root.mainloop()