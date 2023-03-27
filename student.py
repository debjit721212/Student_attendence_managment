from tkinter import*
from tkinter import ttk
from PIL import Image,ImageTk
from tkinter import messagebox
import mysql.connector 
import cv2

class Student:
    def __init__(self,root):
        self.root=root
        self.root.geometry("1530x790+0+0")
        self.root.title("Student")
        
        
        # ============== variables ======================
        self.var_dep=StringVar()
        self.var_course=StringVar()
        self.var_year=StringVar()
        self.var_semester=StringVar()
        self.var_std_id=StringVar()
        self.var_dev=StringVar()
        self.var_name=StringVar()
        self.var_roll=StringVar()
        self.var_gender=StringVar()
        self.var_dob=StringVar()
        self.var_email=StringVar()
        self.var_teacher=StringVar()
        self.var_phone=StringVar()
        self.var_address=StringVar()
        
        #### Adding title
        title_lev_= Label(self.root,text="Welcome to student info Page",font=('times new roman',45,'bold'),bg="lightblue",fg="white")
        title_lev_.place(x=0,y=0,width=1530,height=110)
        
        
        # Put background image
        img4 = Image.open(r'E:\student_management\photo\middle-school-building-20723831.jpg')
        img4 = img4.resize((1530,680),Image.ANTIALIAS)
        self.photoimg4=ImageTk.PhotoImage(img4)
        
        bg_img = Label(self.root,image=self.photoimg4)
        bg_img.place(x=0,y=110,width=1530,height=680)
        
        
        ########## Adding title into back ground images 
        title_lev= Label(bg_img,text="Student Information",font=('times new roman',35,'bold'),bg="gold",fg="red")
        title_lev.place(x=0,y=-1,width=1530,height=50)
        
        ### Creating main frame
        main_frame= Frame(bg_img,bd=3,bg="white")
        main_frame.place(x=20,y=60,width=1480,height=610)
        
        ## creating left frame
        left_frame=LabelFrame(main_frame,bd=2,bg='white',relief=RIDGE,text="Student Details",font=('times new roman',12,'bold'))
        left_frame.place(x=15,y=10,width=700,height=590)
        
        img_left = Image.open(r'E:\student_management\photo\middle-school-building-20723831.jpg')
        img_left = img_left.resize((700,130),Image.ANTIALIAS)
        self.photoimg_left=ImageTk.PhotoImage(img_left)
        
        left_lev = Label(left_frame,image=self.photoimg_left)
        left_lev.place(x=1,y=0,width=700,height=130)
        
        ## Current Course
        current_course_frame=LabelFrame(left_frame,bd=2,bg='white',relief=RIDGE,text="Current Course information",font=('times new roman',12,'bold'))
        current_course_frame.place(x=5,y=135,width=685,height=115)
        
        # Depertment label
        dep_lable= Label(current_course_frame,text="Department",font=('times new roman',13,'bold'),bg='white')
        dep_lable.grid(row=0,column=0,padx=10,sticky=W)
        # Pepartment combo box
        dep_combo= ttk.Combobox(current_course_frame,textvariable=self.var_dep,font=('times new roman',13,'bold'),width=17,state="readonly")
        dep_combo["values"]=("Select Deperment","Computer Science","ECE","IT","Civil","Mechanical","Data Science")
        dep_combo.current(0)
        dep_combo.grid(row=0,column=1,padx=2,pady=10,sticky=W)
        
        # Course label
        course_lable= Label(current_course_frame,text="Course",font=('times new roman',13,'bold'),bg='white')
        course_lable.grid(row=0,column=3,padx=10,sticky=W)
        # Pepartment combo box
        course_combo= ttk.Combobox(current_course_frame,textvariable=self.var_course,font=('times new roman',13,'bold'),width=17,state="readonly")
        course_combo["values"]=("Select Course","B.TECH","M.TECH","DEPLOMA")
        course_combo.current(0)
        course_combo.grid(row=0,column=4,padx=2,pady=10,sticky=W)
        
        # Year label
        year_lable= Label(current_course_frame,text="Year",font=('times new roman',13,'bold'),bg='white')
        year_lable.grid(row=1,column=0,padx=10,sticky=W)
        # Pepartment combo box
        year_combo= ttk.Combobox(current_course_frame,textvariable=self.var_year,font=('times new roman',13,'bold'),width=17,state="readonly")
        year_combo["values"]=("Select Year","2020-21","2021-22","2022-23","2023-24","2024-25")
        year_combo.current(0)
        year_combo.grid(row=1,column=1,padx=2,pady=10,sticky=W)
        
        # Semester label
        semester_lable= Label(current_course_frame,text="Semester",font=('times new roman',13,'bold'),bg='white')
        semester_lable.grid(row=1,column=3,padx=10,sticky=W)
        # Pepartment combo box
        semester_combo= ttk.Combobox(current_course_frame,textvariable=self.var_semester,font=('times new roman',13,'bold'),width=17,state="readonly")
        semester_combo["values"]=("Select Semester","Semester-1","Semester-2")
        semester_combo.current(0)
        semester_combo.grid(row=1,column=4,padx=2,pady=10,sticky=W)
        
        ## Student information
        class_student_frame=LabelFrame(left_frame,bd=2,bg='white',relief=RIDGE,text="Class Student information",font=('times new roman',12,'bold'))
        class_student_frame.place(x=5,y=250,width=685,height=315)
        
        # Student ID 
        student_id_lable= Label(class_student_frame,text="Student ID : ",font=('times new roman',13,'bold'),bg='white')
        student_id_lable.grid(row=0,column=0,padx=10,pady=5,sticky=W) 
        ###Student ID Entry
        student_id_entry= ttk.Entry(class_student_frame,textvariable=self.var_std_id,width=18,font=('times new roman',13,'bold'))
        student_id_entry.grid(row=0,column=1,padx=10,pady=5,sticky=W)
        
        # Student name
        student_name_lable= Label(class_student_frame,text="Student Name : ",font=('times new roman',13,'bold'),bg='white')
        student_name_lable.grid(row=0,column=2,padx=10,pady=5,sticky=W)
        ###Student name Entry
        student_name_entry= ttk.Entry(class_student_frame,textvariable=self.var_name,width=18,font=('times new roman',13,'bold'))
        student_name_entry.grid(row=0,column=3,padx=10,pady=5,sticky=W)
        
        ### Class Division
        class_division_lable= Label(class_student_frame,text="Class Division : ",font=('times new roman',13,'bold'),bg='white')
        class_division_lable.grid(row=2,column=0,padx=10,pady=5,sticky=W)
        ###Class division Combo
        class_division_combo= ttk.Combobox(class_student_frame,textvariable=self.var_dev,font=('times new roman',13,'bold'),width=16,state="readonly")
        class_division_combo["values"]=("A","B","C")
        class_division_combo.current(0)
        class_division_combo.grid(row=2,column=1,padx=10,pady=5,sticky=W)
        # class_division_entry= ttk.Entry(class_student_frame,textvariable=self.var_dev,width=18,font=('times new roman',13,'bold'))
        # class_division_entry.grid(row=2,column=1,padx=10,pady=5,sticky=W)
        
        ### Roll No
        roll_no_lable= Label(class_student_frame,text="Roll No : ",font=('times new roman',13,'bold'),bg='white')
        roll_no_lable.grid(row=2,column=2,padx=10,pady=5,sticky=W)
        ###Class division Entry
        roll_no_entry= ttk.Entry(class_student_frame,textvariable=self.var_roll,width=18,font=('times new roman',13,'bold'))
        roll_no_entry.grid(row=2,column=3,padx=10,pady=5,sticky=W)
        
        ### Gender
        Gender_lable= Label(class_student_frame,text="Gender : ",font=('times new roman',13,'bold'),bg='white')
        Gender_lable.grid(row=4,column=0,padx=10,pady=5,sticky=W)
        ###Gender Combo
        gender_combo= ttk.Combobox(class_student_frame,textvariable=self.var_gender,font=('times new roman',13,'bold'),width=16,state="readonly")
        gender_combo["values"]=("Select Gender","Male","Female","Transgender")
        gender_combo.current(0)
        gender_combo.grid(row=4,column=1,padx=10,pady=5,sticky=W)
        
        ### Date of Brith
        dob_lable= Label(class_student_frame,text="DOB : ",font=('times new roman',13,'bold'),bg='white')
        dob_lable.grid(row=4,column=2,padx=10,pady=5,sticky=W)
        ### Email ID Entry
        email_id_entry= ttk.Entry(class_student_frame,textvariable=self.var_dob,width=18,font=('times new roman',13,'bold'))
        email_id_entry.grid(row=4,column=3,padx=10,pady=5,sticky=W)
        
        ### Email ID
        email_id_lable= Label(class_student_frame,text="Email ID : ",font=('times new roman',13,'bold'),bg='white')
        email_id_lable.grid(row=6,column=0,padx=10,pady=5,sticky=W)
        ### Email ID Entry
        email_id_entry= ttk.Entry(class_student_frame,textvariable=self.var_email,width=18,font=('times new roman',13,'bold'))
        email_id_entry.grid(row=6,column=1,padx=10,pady=5,sticky=W)
        
        ### Phone number 
        phone_number_lable= Label(class_student_frame,text="Phone Number : ",font=('times new roman',13,'bold'),bg='white')
        phone_number_lable.grid(row=6,column=2,padx=10,pady=5,sticky=W)
        ### Phone number 
        phone_number_entry= ttk.Entry(class_student_frame,textvariable=self.var_phone,width=18,font=('times new roman',13,'bold'))
        phone_number_entry.grid(row=6,column=3,padx=10,pady=5,sticky=W)
        
        ### Class Teacher
        class_teacher_lable= Label(class_student_frame,text="Class Teacher : ",font=('times new roman',13,'bold'),bg='white')
        class_teacher_lable.grid(row=8,column=0,padx=10,pady=5,sticky=W)
        ### Class Teacher
        class_teacher_entry= ttk.Entry(class_student_frame,textvariable=self.var_teacher,width=18,font=('times new roman',13,'bold'))
        class_teacher_entry.grid(row=8,column=1,padx=10,pady=5,sticky=W)
        
        ### Address
        address_lable= Label(class_student_frame,text="Address : ",font=('times new roman',13,'bold'),bg='white')
        address_lable.grid(row=8,column=2,padx=10,pady=5,sticky=W)
        ### Address  Entry
        address_entry= ttk.Entry(class_student_frame,textvariable=self.var_address,width=18,font=('times new roman',13,'bold'))
        address_entry.grid(row=8,column=3,padx=10,pady=5,sticky=W)
        
        ## Radio Button
        self.var_redio1=StringVar()
        radiobutton1=ttk.Radiobutton(class_student_frame,variable=self.var_redio1,text="Take a photo sample",value="Yes",)
        radiobutton1.grid(row=10,column=0)
        
        radiobutton2=ttk.Radiobutton(class_student_frame,variable=self.var_redio1,text="No photo sample",value="No",)
        radiobutton2.grid(row=10,column=1)
        
        # bbuttons frame
        btn_frame=Frame(class_student_frame,bd=2,relief=RIDGE,bg="white")
        btn_frame.place(x=0,y=205,width=680,height=65)
        #SAve
        save_botton= Button(btn_frame,text="Save",command=self.add_data,width=15,bg='white',fg='Green',font=('times new roman',13,'bold'))
        save_botton.grid(row=0,column=0,padx=4,pady=4)
        
        # Update
        update_botton= Button(btn_frame,text="Update",command=self.update_data,width=15,bg='white',fg='Green',font=('times new roman',13,'bold'))
        update_botton.grid(row=0,column=1,padx=4,pady=4)
        
        #Reset
        reset_botton= Button(btn_frame,text="Reset",command=self.reset_data,width=15,bg='white',fg='Black',font=('times new roman',13,'bold'))
        reset_botton.grid(row=0,column=2,padx=4,pady=4)
        
        # Delete
        delete_botton= Button(btn_frame,text="Delete",command=self.delete_data,width=15,bg='white',fg='Red',font=('times new roman',13,'bold'))
        delete_botton.grid(row=0,column=3,padx=4,pady=4)
        
        btn_frame1 = Frame(class_student_frame,bd=2,relief=RIDGE,bg="white")
        btn_frame1.place(x=0,y=245,width=680,height=45)
        
        # take photo
        take_photo_botton= Button(btn_frame1,text="Take a photo",command=self.generate_dataset,width=32,bg='white',fg='Red',font=('times new roman',13,'bold'))
        take_photo_botton.grid(row=0,column=0,padx=4,pady=4)
        
        # Update photo
        update_photo_botton= Button(btn_frame1,text="Update a photo",width=32,bg='white',fg='Red',font=('times new roman',13,'bold'))
        update_photo_botton.grid(row=0,column=1,padx=4,pady=4)
        
        ## creating right frame
        right_frame=LabelFrame(main_frame,bd=2,bg='white',relief=RIDGE,text="Student Details",font=('times new roman',12,'bold'))
        right_frame.place(x=750,y=10,width=700,height=590)
        
        img_right = Image.open(r'E:\student_management\photo\middle-school-building-20723831.jpg')
        img_right = img_right.resize((700,130),Image.ANTIALIAS)
        self.photoimg_right=ImageTk.PhotoImage(img_right)
        
        right_lev = Label(right_frame,image=self.photoimg_right)
        right_lev.place(x=1,y=0,width=700,height=130)
        
        
        ## ======= search System ========
        
        search_student_frame=LabelFrame(right_frame,bd=2,bg='white',relief=RIDGE,text="Search Student",font=('times new roman',12,'bold'))
        search_student_frame.place(x=5,y=135,width=685,height=70)
        
        # Search Student
        search_student_lable= Label(search_student_frame,text="Search By : ",font=('times new roman',13,'bold'),bg='white',fg="green")
        search_student_lable.grid(row=0,column=0,padx=10,pady=5,sticky=W)
        # Combo box
        search_combo= ttk.Combobox(search_student_frame,font=('times new roman',13,'bold'),width=13,state="readonly")
        search_combo["values"]=("Select","Roll No","Student ID",)
        search_combo.current(0)
        search_combo.grid(row=0,column=1,padx=2,pady=10,sticky=W)
        # Entry 
        search_entry= ttk.Entry(search_student_frame,width=17,font=('times new roman',13,'bold'))
        search_entry.grid(row=0,column=2,padx=4,pady=4)
        
        ## Search Botton
        search_botton= Button(search_student_frame,text="Search",width=11,bg='white',fg='Red',font=('times new roman',13,'bold'))
        search_botton.grid(row=0,column=3,padx=4,pady=4)
        ## Show All  Botton
        showAll_botton= Button(search_student_frame,text="Show All",width=11,bg='white',fg='Red',font=('times new roman',13,'bold'))
        showAll_botton.grid(row=0,column=4,padx=4,pady=4)
        
        ### ========== Table frame ============
        student_table_frame=LabelFrame(right_frame,bd=2,bg='white',relief=RIDGE,)
        student_table_frame.place(x=5,y=209,width=685,height=340)
        
        #### Scroll ber
        scroll_x=ttk.Scrollbar(student_table_frame,orient=HORIZONTAL,)
        scroll_y=ttk.Scrollbar(student_table_frame,orient=VERTICAL,)
        
        self.student_table=ttk.Treeview(student_table_frame,columns=("Department","Course","Year","Semester","Stu_ID","Name","DOB","Div","Roll","Gender","Email","Phone","Teacher","Address","Photo"),xscrollcommand=scroll_x.set,yscrollcommand=scroll_y.set)
        scroll_x.pack(side=BOTTOM,fill=X)
        scroll_y.pack(side=RIGHT,fill=Y)
        scroll_x.config(command=self.student_table.xview)
        scroll_y.config(command=self.student_table.yview)
        
        # Showing heading 
        self.student_table.heading("Department",text="Department")
        self.student_table.heading("Course",text="Course")
        self.student_table.heading("Year",text="Year")
        self.student_table.heading("Semester",text="Semester")
        self.student_table.heading("Stu_ID",text="Student ID")
        self.student_table.heading("Name",text="Name")
        self.student_table.heading("DOB",text="DOB")
        self.student_table.heading("Div",text="Divison")
        self.student_table.heading("Roll",text="Roll")
        self.student_table.heading("Gender",text="Gender")
        self.student_table.heading("Email",text="Email")
        self.student_table.heading("Phone",text="Phone")
        self.student_table.heading("Teacher",text="Teacher")
        self.student_table.heading("Address",text="Address")
        self.student_table.heading("Photo",text="Photo Status")
        self.student_table["show"]="headings"
        
        self.student_table.column("Department",width=120)
        self.student_table.column("Course",width=120)
        self.student_table.column("Year",width=120)
        self.student_table.column("Semester",width=120)
        self.student_table.column("Stu_ID",width=100)
        self.student_table.column("Name",width=130)
        self.student_table.column("DOB",width=100)
        self.student_table.column("Div",width=100)
        self.student_table.column("Roll",width=120)
        self.student_table.column("Gender",width=100)
        self.student_table.column("Email",width=140)
        self.student_table.column("Phone",width=140)
        self.student_table.column("Teacher",width=140)
        self.student_table.column("Address",width=140)
        self.student_table.column("Photo",width=100)
        
        self.student_table.pack(fill=BOTH,expand=1)
        self.student_table.bind("<ButtonRelease>",self.get_cursor)
        self.fetch_data()
        
    # ============== Function Decration ===================
    def add_data(self):
        if self.var_dep.get()=="Select Department" or self.var_course.get()=="Select Course" or self.var_std_id.get()=="" or self.var_address.get()=="" or self.var_dev.get()=="" or self.var_dob.get()=="" or self.var_email.get()=="" or self.var_gender.get()=="Select Gender" or self.var_name.get()=="" or self.var_phone.get()=="":
            messagebox.showerror("Error","All Firlds are require",parent=self.root)
        else:
            try:
                conn=mysql.connector.connect(host="localhost",user="root",passwd="root",database="face_recognizer",auth_plugin = 'mysql_native_password')
                my_cursor=conn.cursor()
                my_cursor.execute("INSERT INTO students VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(
                                                                                                            self.var_dep.get(),
                                                                                                            self.var_course.get(),
                                                                                                            self.var_year.get(),
                                                                                                            self.var_semester.get(),
                                                                                                            self.var_std_id.get(),
                                                                                                            self.var_name.get(),
                                                                                                            self.var_dob.get(),
                                                                                                            self.var_dev.get(),
                                                                                                            self.var_roll.get(),
                                                                                                            self.var_gender.get(),
                                                                                                            self.var_email.get(),
                                                                                                            self.var_phone.get(),
                                                                                                            self.var_teacher.get(),
                                                                                                            self.var_address.get(),
                                                                                                            self.var_redio1.get()
                ))
                conn.commit()
                self.fetch_data()
                conn.close()
                messagebox.showinfo("Success","Student details has been added Successfully",parent=self.root)
            except Exception as es:
                messagebox.showerror("Error",f"Due to : {str(es)}",parent=self.root)
    
    # ================= Fetch data =====================
    def fetch_data(self):
        conn=mysql.connector.connect(host="localhost",user="root",passwd="root",database="face_recognizer",auth_plugin = 'mysql_native_password')
        my_cursue=conn.cursor()
        my_cursue.execute("SELECT * FROM students")
        data=my_cursue.fetchall()
        
        if len(data)!=0:
            self.student_table.delete(*self.student_table.get_children())
            for i in data:
                self.student_table.insert("",END,values=i)
            conn.commit()
        conn.close()
    
    # ============= get function ===============
    def get_cursor(self,event=""):
        cursor_focus=self.student_table.focus()
        content=self.student_table.item(cursor_focus)
        data=content["values"]
        
        self.var_dep.set(data[0]),
        self.var_course.set(data[1]),
        self.var_year.set(data[2]),
        self.var_semester.set(data[3]),
        self.var_std_id.set(data[4]),
        self.var_name.set(data[5]),
        self.var_dob.set(data[6]),
        self.var_dev.set(data[7]),
        self.var_roll.set(data[8]),
        self.var_gender.set(data[9]),
        self.var_email.set(data[10]),
        self.var_phone.set(data[11]),
        self.var_teacher.set(data[12]),
        self.var_address.set(data[13]),
        self.var_redio1.set(data[14])
        
    # update function
    def update_data(self):
        if self.var_dep.get()=="Select Department" or self.var_course.get()=="Select Course" or self.var_std_id.get()=="" or self.var_address.get()=="" or self.var_dev.get()=="" or self.var_dob.get()=="" or self.var_email.get()=="" or self.var_gender.get()=="Select Gender" or self.var_name.get()=="" or self.var_phone.get()=="":
            messagebox.showerror("Error","All Firlds are require",parent=self.root)
        else:
            try:
                Update=messagebox.askyesno("Update","Do you want to update student details",parent=self.root)
                if Update>0:
                    conn=mysql.connector.connect(host="localhost",user="root",passwd="root",database="face_recognizer",auth_plugin = 'mysql_native_password')
                    my_cursor=conn.cursor()
                    my_cursor.execute("update students set Department=%s,Course=%s,Stu_year=%s,Semester=%s,Student_name=%s,DOB=%s,Class_division=%s,Roll_no=%s,Gender=%s,Email_id=%s,phone_number=%s,Class_teacher=%s,Address=%s,Photo_sample=%s WHERE Student_ID=%s",(
                                                                                                                    self.var_dep.get(),
                                                                                                                    self.var_course.get(),
                                                                                                                    self.var_year.get(),
                                                                                                                    self.var_semester.get(),
                                                                                                                    self.var_name.get(),
                                                                                                                    self.var_dob.get(),
                                                                                                                    self.var_dev.get(),
                                                                                                                    self.var_roll.get(),
                                                                                                                    self.var_gender.get(),
                                                                                                                    self.var_email.get(),
                                                                                                                    self.var_phone.get(),
                                                                                                                    self.var_teacher.get(),
                                                                                                                    self.var_address.get(),
                                                                                                                    self.var_redio1.get(),
                                                                                                                    self.var_std_id.get()
                                                                                                                    ))
                else:
                    if not Update:
                        return
                messagebox.showinfo("Success","Student details update completed.",parent=self.root)
                conn.commit()
                self.fetch_data()
                conn.close()
            except Exception as es:
                messagebox.showerror("Error",f"Due To: {str(es)}",parent=self.root)   
                
                    
    ######   Delete Function
    
    def delete_data(self):
        if self.var_std_id.get()=="":
            messagebox.showerror("Error","Student id must be require ",parent=self.root)
        else:
            try:
                delete=messagebox.askyesno("Student delete Page","Do you want to detele student details",parent=self.root)
                if delete>0:
                    conn=mysql.connector.connect(host="localhost",user="root",passwd="root",database="face_recognizer",auth_plugin = 'mysql_native_password')
                    my_cursor=conn.cursor()
                    sql="DELETE FROM students WHERE Student_ID=%s"
                    val=(self.var_std_id.get(),)
                    my_cursor.execute(sql,val)
                else:
                    if not delete:
                        return
                messagebox.showinfo("Success","Student details deleted succussfully",parent=self.root)
                conn.commit()
                self.fetch_data()
                conn.close()
            except Exception as es:
                messagebox.showerror("Error",f"Due To : {str(es)}",parent=self.root)
                    
    ### Reset function 
    def reset_data(self):
        self.var_dep.set("Select Department")
        self.var_course.set("Select Course"),
        self.var_year.set("Select year"),
        self.var_semester.set("Select Semester"),
        self.var_std_id.set(""),
        self.var_name.set(""),
        self.var_dob.set(""),
        self.var_dev.set("A"),
        self.var_roll.set(""),
        self.var_gender.set("Select Gender"),
        self.var_email.set(""),
        self.var_phone.set(""),
        self.var_teacher.set(""),
        self.var_address.set(""),
        self.var_redio1.set("")
    ##=================generate dataset or take a photo sample
    def generate_dataset(self):
        if self.var_dep.get()=="Select Department" or self.var_course.get()=="Select Course" or self.var_std_id.get()=="" or self.var_address.get()=="" or self.var_dev.get()=="" or self.var_dob.get()=="" or self.var_email.get()=="" or self.var_gender.get()=="Select Gender" or self.var_name.get()=="" or self.var_phone.get()=="":
            messagebox.showerror("Error","All Firlds are require",parent=self.root)
        else:
            try:
                conn=mysql.connector.connect(host="localhost",user="root",passwd="root",database="face_recognizer",auth_plugin = 'mysql_native_password')
                my_cursor=conn.cursor()
                my_cursor.execute("SELECT * FROM students")
                my_result=my_cursor.fetchall()
                id=self.var_std_id.get()
                # for x in my_result:
                #     id+=1
                my_cursor.execute("update students set Department=%s,Course=%s,Stu_year=%s,Semester=%s,Student_name=%s,DOB=%s,Class_division=%s,Roll_no=%s,Gender=%s,Email_id=%s,phone_number=%s,Class_teacher=%s,Address=%s,Photo_sample=%s WHERE Student_ID=%s",(
                                                                                                                    self.var_dep.get(),
                                                                                                                    self.var_course.get(),
                                                                                                                    self.var_year.get(),
                                                                                                                    self.var_semester.get(),
                                                                                                                    self.var_name.get(),
                                                                                                                    self.var_dob.get(),
                                                                                                                    self.var_dev.get(),
                                                                                                                    self.var_roll.get(),
                                                                                                                    self.var_gender.get(),
                                                                                                                    self.var_email.get(),
                                                                                                                    self.var_phone.get(),
                                                                                                                    self.var_teacher.get(),
                                                                                                                    self.var_address.get(),
                                                                                                                    self.var_redio1.get(),
                                                                                                                    self.var_std_id.get()
                                                                                                                    ))
                conn.commit()
                self.fetch_data()
                self.reset_data()
                conn.close()
                # ==== Load predifiend data on face frontals from opencv
                face_classifier=cv2.CascadeClassifier(r'E:\student_management\student\Lib\site-packages\cv2\data\haarcascade_frontalface_default.xml')
                def face_cropped(img):
                    gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
                    faces=face_classifier.detectMultiScale(gray,1.3,5)
                    # Scalling factor = 1.3
                    # Munimum neibor = 5
                    for (x,y,w,h) in faces:
                        face_cropped=img[y:y+h,x:x+w]
                        return face_cropped
                cap=cv2.VideoCapture(0)
                img_id=0
                while True:
                    ret,frame=cap.read()
                    if face_cropped(frame) is not None:
                        img_id+=1
                        face=cv2.resize(face_cropped(frame),(450,450))
                        face=cv2.cvtColor(face,cv2.COLOR_BGR2GRAY)
                        file_name_path="student_image/user."+str(id)+"."+str(img_id)+".jpg"
                        cv2.imwrite(file_name_path,face)
                        cv2.putText(face,str(img_id),(50,50),cv2.FONT_HERSHEY_COMPLEX,2,(0,255,10),2)
                        cv2.imshow("croped face",face)
                    
                    if cv2.waitKey(1)==13 or int(img_id)==100:
                        break
                cap.release()
                cv2.destroyAllWindows()
                messagebox.showinfo("Result","Generating Dataset completed successfully")
            except Exception as es:
                messagebox.showerror("Error",f"Due to : {str(es)}",parent=self.root)    
            
                        
        
          
if __name__=="__main__":
    root=Tk()
    obj = Student(root)
    root.mainloop()
     