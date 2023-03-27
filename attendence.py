from tkinter import*
from tkinter import ttk
from PIL import Image,ImageTk
from tkinter import messagebox
import mysql.connector 
import cv2
import os
import csv
from tkinter import filedialog
mydata=[]

class Attendence:
    def __init__(self,root):
        self.root=root
        self.root.geometry("1530x790+0+0")
        self.root.title("Attendence")
        
        # ============== variables ======================
        self.var_attendence_id=StringVar()
        self.var_roll=StringVar()
        self.var_name=StringVar()
        self.var_dep=StringVar()
        self.var_time=StringVar()
        self.var_date=StringVar()
        self.var_attendence_status=StringVar()
        
        
        title_lev_= Label(self.root,text="Attendence Details",font=('times new roman',45,'bold'),bg="skyblue",fg="white")
        title_lev_.place(x=0,y=0,width=1530,height=135)
        
        ### Creating main frame
        main_frame= Frame(self.root,bd=3,bg="white")
        main_frame.place(x=60,y=140,width=1400,height=600)
        
        ## creating left frame
        left_frame=LabelFrame(main_frame,bd=2,bg='white',relief=RIDGE,text="Student Attendence Details",font=('times new roman',12,'bold'))
        left_frame.place(x=20,y=10,width=650,height=580)
        
        img_left = Image.open(r'E:\student_management\photo\leon-wu-LLfRMRT-9AY-unsplash.jpg')
        img_left = img_left.resize((700,190),Image.ANTIALIAS)
        self.photoimg_left=ImageTk.PhotoImage(img_left)
        
        left_lev = Label(left_frame,image=self.photoimg_left)
        left_lev.place(x=1,y=0,width=700,height=190)
        
        # left inside frame
        left_indiseframe=Frame(left_frame,bd=2,relief=RIDGE,bg="white")
        left_indiseframe.place(x=5,y=200,width=635,height=307)
        
        ## leble and entry
        # attendence_id
        attendence_id_lable= Label(left_indiseframe,text="Attendence ID : ",font=('times new roman',13,'bold'),bg='white')
        attendence_id_lable.grid(row=5,column=0,padx=10,pady=7,sticky=W) 
        ###Student ID Entry
        attendence_id_entry= ttk.Entry(left_indiseframe,textvariable=self.var_attendence_id,width=15,font=('times new roman',13,'bold'))
        attendence_id_entry.grid(row=5,column=1,padx=10,pady=7,sticky=W)
        
        
        # Student Roll
        student_roll_lable= Label(left_indiseframe,text="Student Roll : ",font=('times new roman',13,'bold'),bg='white')
        student_roll_lable.grid(row=5,column=2,padx=10,pady=7,sticky=W)
        ###Student roll Entry
        student_roll_entry= ttk.Entry(left_indiseframe,textvariable=self.var_roll,width=15,font=('times new roman',13,'bold'))
        student_roll_entry.grid(row=5,column=3,padx=10,pady=7,sticky=W)
        
        # Student name
        student_name_lable= Label(left_indiseframe,text="Student Name : ",font=('times new roman',13,'bold'),bg='white')
        student_name_lable.grid(row=10,column=0,padx=10,pady=7,sticky=W)
        ###Student name Entry
        student_name_entry= ttk.Entry(left_indiseframe,textvariable=self.var_name,width=15,font=('times new roman',13,'bold'))
        student_name_entry.grid(row=10,column=1,padx=10,pady=7,sticky=W)
        
        # Depertment label
        dep_lable= Label(left_indiseframe,text="Department :",font=('times new roman',13,'bold'),bg='white')
        dep_lable.grid(row=10,column=2,padx=7,sticky=W)
        # Pepartment combo box
        dep_combo= ttk.Combobox(left_indiseframe,textvariable=self.var_dep,font=('times new roman',13,'bold'),width=15,state="readonly")
        dep_combo["values"]=("Select Department","Computer Science","ECE","IT","Civil","Mechanical","Data Science")
        dep_combo.current(0)
        dep_combo.grid(row=10,column=3,padx=2,pady=7,sticky=W)
        
        # time
        attendence_time_lable= Label(left_indiseframe,text="Time : ",font=('times new roman',13,'bold'),bg='white')
        attendence_time_lable.grid(row=15,column=0,padx=10,pady=7,sticky=W)
        ###Student name Entry
        attendence_time_entry= ttk.Entry(left_indiseframe,textvariable=self.var_time,width=15,font=('times new roman',13,'bold'))
        attendence_time_entry.grid(row=15,column=1,padx=10,pady=7,sticky=W)
        
        # Date
        attendence_date_lable= Label(left_indiseframe,text="Date : ",font=('times new roman',13,'bold'),bg='white')
        attendence_date_lable.grid(row=15,column=2,padx=10,pady=7,sticky=W)
        ###Student name Entry
        attendence_date_entry= ttk.Entry(left_indiseframe,textvariable=self.var_date,width=15,font=('times new roman',13,'bold'))
        attendence_date_entry.grid(row=15,column=3,padx=10,pady=7,sticky=W)
        
        # Attendence label
        attendence_lable= Label(left_indiseframe,text="Attendence Status :",font=('times new roman',13,'bold'),bg='white')
        attendence_lable.grid(row=45,column=1,padx=7,sticky=W)
        # Pepartment combo box
        attendence_combo= ttk.Combobox(left_indiseframe,textvariable=self.var_attendence_status,font=('times new roman',13,'bold'),width=14,state="readonly")
        attendence_combo["values"]=("Status","Present","Absent")
        attendence_combo.current(0)
        attendence_combo.grid(row=45,column=2,padx=5,pady=7)
        
        
        # bbuttons frame
        btn_frame=Frame(left_indiseframe,bd=2,relief=RIDGE,bg="white")
        btn_frame.place(x=0,y=200,width=632,height=80)
        #SAve
        save_botton= Button(btn_frame,text="Import CSV",command=self.importCSV,width=30,bg='white',fg='Green',font=('times new roman',13,'bold'))
        save_botton.grid(row=0,column=0,padx=4,pady=4)
        
        # Update
        update_botton= Button(btn_frame,text="Export CSV",command=self.exportCSV,width=29,bg='white',fg='Green',font=('times new roman',13,'bold'))
        update_botton.grid(row=0,column=3,padx=4,pady=4)
        
        #Reset
        reset_botton= Button(btn_frame,text="Update",width=30,bg='white',fg='Black',font=('times new roman',13,'bold'))
        reset_botton.grid(row=2,column=0,padx=4,pady=4)
        
        # Delete
        delete_botton= Button(btn_frame,text="Reset",command=self.reset_data,width=29,bg='white',fg='Black',font=('times new roman',13,'bold'))
        delete_botton.grid(row=2,column=3,padx=4,pady=4)
        
        # btn_frame1 = Frame(left_indiseframe,bd=2,relief=RIDGE,bg="white")
        # btn_frame1.place(x=0,y=245,width=680,height=45)
        
        
        ## creating right frame
        right_frame=LabelFrame(main_frame,bd=2,bg='white',relief=RIDGE,text="Student Details",font=('times new roman',12,'bold'))
        right_frame.place(x=720,y=10,width=650,height=580)
        
        
        btn_frame=Frame(right_frame,bd=2,relief=RIDGE,bg="white")
        btn_frame.place(x=5,y=5,width=630,height=505)
        
        ### Scroll ber 
        scroll_x=ttk.Scrollbar(btn_frame,orient=HORIZONTAL,)
        scroll_y=ttk.Scrollbar(btn_frame,orient=VERTICAL,)
        self.attendence_report_table=ttk.Treeview(btn_frame,columns=("Attendence_ID","Roll_no","Name","Department","Time","Date","Attendence_status"),xscrollcommand=scroll_x.set,yscrollcommand=scroll_y.set)
        scroll_x.pack(side=BOTTOM,fill=X)
        scroll_y.pack(side=RIGHT,fill=Y)
        scroll_x.config(command=self.attendence_report_table.xview)
        scroll_y.config(command=self.attendence_report_table.yview)
        
        
        # Showing heading 
        self.attendence_report_table.heading("Attendence_ID",text="Attendence ID")
        self.attendence_report_table.heading("Roll_no",text="Roll No")
        self.attendence_report_table.heading("Name",text="Name")
        self.attendence_report_table.heading("Department",text="Department")
        self.attendence_report_table.heading("Time",text="Time")
        self.attendence_report_table.heading("Date",text="Date")
        self.attendence_report_table.heading("Attendence_status",text="Attendence Status")
        self.attendence_report_table["show"]="headings"
        
        self.attendence_report_table.column("Attendence_ID",width=120)
        self.attendence_report_table.column("Roll_no",width=120)
        self.attendence_report_table.column("Name",width=120)
        self.attendence_report_table.column("Department",width=120)
        self.attendence_report_table.column("Time",width=120)
        self.attendence_report_table.column("Date",width=120)
        self.attendence_report_table.column("Attendence_status",width=120)
        
        self.attendence_report_table.pack(fill=BOTH,expand=1)
        self.attendence_report_table.bind("<ButtonRelease>",self.get_cursor)
        
    def fetchData(self,rows):
        self.attendence_report_table.delete(*self.attendence_report_table.get_children())
        for i in rows:
            self.attendence_report_table.insert("",END,values=i)
    ## ImportCSV function
    def importCSV(self):
        global mydata
        mydata.clear()
        fln=filedialog.askopenfilename(initialdir=os.getcwdb(),title="Open CSV",filetypes=(("CSV File","*.csv"),("All File","*.*")),parent=self.root)
        with open(fln) as myfile:
            csvread=csv.reader(myfile,delimiter=",")
            for i in csvread:
                mydata.append(i)
            self.fetchData(mydata)
    
    ## Export CSV function 
    def exportCSV(self):
        try:
            if len(mydata)<1:
                messagebox.showerror("No Data","No Data found to export",parent=self.root)
                return False
            fln=filedialog.asksaveasfilename(initialdir=os.getcwdb(),title="Open CSV",filetypes=(("CSV File","*.csv"),("All File","*.*")),parent=self.root)
            with open(fln,mode="w",newline="") as myfile:
                export_write=csv.writer(myfile,delimiter=",")
                for i in mydata:
                    export_write.writerow(i)
                messagebox.showinfo("Data Export","Your data exported to"+os.path.basename(fln)+"Successfully")
        except Exception as es:
                messagebox.showerror("Error",f"Due to : {str(es)}",parent=self.root)
                
    #### Get cursor
    def get_cursor(self,event=""):
        cursor_focus=self.attendence_report_table.focus()
        content=self.attendence_report_table.item(cursor_focus)
        data=content["values"]
        
        self.var_attendence_id.set(data[0]),
        self.var_roll.set(data[1]),
        self.var_name.set(data[2]),
        self.var_dep.set(data[3]),
        self.var_time.set(data[4]),
        self.var_date.set(data[5]),
        self.var_attendence_status.set(data[6])
        
    # ======== reset button
    def reset_data(self):
        self.var_attendence_id.set("")
        self.var_roll.set(""),
        self.var_name.set(""),
        self.var_dep.set("Select Department"),
        self.var_time.set(""),
        self.var_date.set(""),
        self.var_attendence_status.set("Status")
            



if __name__=="__main__":
    root=Tk()
    obj = Attendence(root)
    root.mainloop()