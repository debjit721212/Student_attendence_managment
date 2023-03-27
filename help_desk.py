from tkinter import*
from tkinter import ttk
from PIL import Image,ImageTk
from tkinter import messagebox

class Helpdesk:
    def __init__(self,root):
        self.root=root
        self.root.geometry("1530x790+0+0")
        self.root.title("Help Desk")
        
        title_lev_= Label(self.root,text="Welcome to Help Desk",font=('times new roman',45,'bold'),bg="skyblue",fg="white")
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
        
        text1_lable= Label(main_frame,text="If any issue is here, feel free to reach out us.",font=('times new roman',13,'bold'),bg='white')
        text1_lable.grid(row=2,column=0,padx=10,pady=7,sticky=W)
        
        text1_lable= Label(main_frame,text="Our official email is humba721212@gmail.com",font=('times new roman',13,'bold'),bg='white')
        text1_lable.grid(row=3,column=0,padx=10,pady=7,sticky=W)
        
        text1_lable= Label(main_frame,text="Our help line number is +91XXXXXXXXXX for India.For US XXXXXXXXXX",font=('times new roman',13,'bold'),bg='white')
        text1_lable.grid(row=4,column=0,padx=10,pady=7,sticky=W)
        
        text1_lable= Label(main_frame,text="Our service is 24X7",font=('times new roman',13,'bold'),bg='white')
        text1_lable.grid(row=5,column=0,padx=10,pady=7,sticky=W)






if __name__=="__main__":
    root=Tk()
    obj = Helpdesk(root)
    root.mainloop()