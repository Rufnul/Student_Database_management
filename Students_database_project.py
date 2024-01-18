# Import tkinter library
import tkinter as tk
from tkinter.ttk import Combobox
from tkinter import *
from tkinter.filedialog import askopenfilename, askdirectory
from PIL import Image, ImageTk, ImageDraw, ImageFont
import re
import random
import mysql.connector
import os
import io
import win32api
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import my_email

# initilize the window and title
root = tk.Tk()
root.geometry('500x600')
root.title('TKinter Hub(Students Management and Registration Hub)')

# create a border background colour
bg_color = '#273b7a'

login_student_icon = tk.PhotoImage(file='images/login_student_img.png')
login_admin_icon = tk.PhotoImage(file='images/admin_img.png')
add_student_icon = tk.PhotoImage(file='images/First_Img.png')
locked_icon = tk.PhotoImage(file='images/locked.png')
unlocked_icon = tk.PhotoImage(file='images/unlocked.png')
add_student_pic_icon = tk.PhotoImage(file='images/add_image.png')


def init_database():
    mydb = mysql.connector.connect(host="127.0.0.1", user="root", password="tiger", database="students_account")
    cursor = mydb.cursor()

    cursor.execute("SHOW TABLES LIKE 'data'")
    table_exists = cursor.fetchone()

    if table_exists:
        cursor.execute("SELECT * FROM data")
        print(cursor.fetchall())
    else:
        cursor.execute("""
        CREATE TABLE data(id_number VARCHAR(255), password VARCHAR(255), name VARCHAR(255), age VARCHAR(255),
                       gender VARCHAR(255), phone_number VARCHAR(255), student_class VARCHAR(255), email VARCHAR(255),
                       image LONGBLOB)""")
    
    mydb.commit()
    cursor.close()
    mydb.close()

def check_id_already_exist(id_number):
        
    mydb = mysql.connector.connect(host="127.0.0.1", user="root", password="tiger", database="students_account")
    cursor = mydb.cursor()

    sql = "SELECT * FROM data WHERE id_number = %s"
    cursor.execute(sql, (id_number,))
    
    response = cursor.fetchall()

    cursor.close()
    mydb.close()

    return response

def check_valid_password(id_number, password):
        
    mydb = mysql.connector.connect(host="127.0.0.1", user="root", password="tiger", database="students_account")
    cursor = mydb.cursor()

    sql = "SELECT id_number, password FROM data WHERE id_number = %s AND password = %s"
    cursor.execute(sql, (id_number, password))
    
    response = cursor.fetchall()

    cursor.close()
    mydb.close()

    return response

    id_exists = check_id_already_exist("")
    print("ID exists:", id_exists)


def add_data(id_number, password, name, age, gender, phone_number,
             student_class, email, pic_data):
    
    mydb = mysql.connector.connect(host="127.0.0.1", user="root", password="tiger", database="students_account")

    cursor = mydb.cursor()

    sql = """INSERT INTO data (id_number, password, name, age, gender, phone_number, student_class, email, image) 
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""
    val = (id_number, password, name, age, gender, phone_number, student_class, email, pic_data)
    
    cursor.execute(sql, val)

    mydb.commit()
    cursor.close()
    mydb.close()


def confirmation_box(message):

    answer = tk.BooleanVar()
    answer.set(False)

    def action(ans):
        answer.set(ans)
        confirmation_box_fm.destroy()

    confirmation_box_fm = tk.Frame(root, highlightbackground=bg_color, highlightthickness=3)
    message_lb= tk.Label(confirmation_box_fm, text=message, font=('Bold', 15))
    message_lb.pack(pady=20)
    cancel_btn =  tk.Button(confirmation_box_fm, text='Cancel', font=('Bold', 15), bd=0, bg=bg_color, fg='white',
                            command=lambda: action(False))
    cancel_btn.place(x=60, y=160)
    yes_btn =  tk.Button(confirmation_box_fm, text='Yes', font=('Bold', 15), bd=0, bg=bg_color, fg='white',
                            command=lambda: action(True))
    yes_btn.place(x=180, y=160, width=80)
    confirmation_box_fm.place(x=100, y=120, width=320, height=220)

    root.wait_window(confirmation_box_fm)
    return answer.get()

def message_box(message):
   
    message_box_fm = tk.Frame(root, highlightbackground=bg_color, highlightthickness=3)
    
    close_btn = tk.Button(message_box_fm, text='X', bd=0, font=('Bold', 13), fg=bg_color,
                          command= lambda: message_box_fm.destroy())
    close_btn.place(x=290, y=5)

    message_lb = tk.Label(message_box_fm, text=message, font=('Bold', 15))
    message_lb.pack(pady=50)

    message_box_fm.place(x=100, y=120, width=320, height=200)

def draw_student_card(student_pic_path, student_data):
    labels ="""
ID Number:
Name:
Gender:
Age:
Class:
Contact:
E-mail:
"""
    student_card = Image.open('images/student_card_frame.png')
    pic = Image.open(student_pic_path).resize((100, 100))
    student_card.paste(pic, (15,25))

    draw = ImageDraw.Draw(student_card)

    heading_font = ImageFont.truetype('bahnschrift', 18)
    label_font = ImageFont.truetype('arial', 15)
    data_font = ImageFont.truetype('bahnschrift', 13)

    draw.text(xy=(150,60), text='Student Card', fill=(0,0,0), font=heading_font)
    draw.multiline_text(xy=(15,120), text=labels, fill=(0,0,0), font=data_font, spacing=6)
    draw.multiline_text(xy=(95,120), text=student_data, fill=(0,0,0), font=data_font, spacing=10)

    return student_card

def student_card_page(student_card_obj):

    def save_student_card():
        path = askdirectory()

        if path:
            print(path)

            student_card_obj.save(f'{path}/student_card.png')

    def print_student_card():
        path = askdirectory()

        if path:
            print(path)

            student_card_obj.save(f'{path}/student_card.png')
            win32api.ShellExecute(0, 'print', f'{path}/student_card.png',None, '.', 0)

    def close_page():
        student_card_page_fm.destroy()
        root.update()
        student_login_page()


    student_card_img = ImageTk.PhotoImage(student_card_obj)

    student_card_page_fm = tk.Frame(root, highlightbackground=bg_color, highlightthickness=3)

    heading_lb = tk.Label(student_card_page_fm, text = 'Student Card',
                          bg = bg_color, fg='white', font=('Bold', 18))
    heading_lb.place(x=0, y=0, width=400)

    close_btn = tk.Button(student_card_page_fm, text='X',
                          bg=bg_color, fg='white', font=('Bold', 13), bd=0, command= close_page)
    close_btn.place(x=370, y=0)

    student_card_lb = tk.Label(student_card_page_fm, image = student_card_img)
    student_card_lb.place(x=50, y=50)

    student_card_lb.image = student_card_img

    save_student_card_btn = tk.Button(student_card_page_fm, text='Save Student Card',
                                      bg= bg_color, fg='white', font=('Bold', 15), bd=1, command= save_student_card)
    save_student_card_btn.place(x=80, y=375)

    print_student_card_btn = tk.Button(student_card_page_fm, text='🖨',
                                      bg= bg_color, fg='white', font=('Bold', 18), bd=1, command= print_student_card)
    print_student_card_btn.place(x=270, y=370)

    student_card_page_fm.place(x=50, y=30, width=400, height=450)

# create a function for welcome page
def welcome_page():

    def forward_to_student_login_page():
        welcome_page_fm.destroy()
        root.update()
        student_login_page()

    def forward_to_admin_login_page():
        welcome_page_fm.destroy()
        root.update()
        admin_login_page()

    def forward_to_add_account_page():
        welcome_page_fm.destroy()
        root.update()
        add_account_page()

    welcome_page_fm = tk.Frame(
        root, highlightbackground=bg_color, highlightthickness=3)

    # Creating a heading lable
    heading_lb = tk.Label(welcome_page_fm, text='Welcome To\nStudent Registration/\nManagement System', bg=bg_color, fg='white', font=('bold', 16))
    heading_lb.place(x=0, y=0, width=400)

    # Create button for login
    student_login_btn = tk.Button(welcome_page_fm, text='Login Student', bg=bg_color, fg='white', font=('Bold', 15), bd=0, command=forward_to_student_login_page)
    student_login_btn.place(x=120, y=125, width=200)

    student_login_img = tk.Button(welcome_page_fm, image=login_student_icon, bd=0, command=forward_to_student_login_page)
    student_login_img.place(x=60, y=100)

    # Creating admin login button
    login_admin_btn = tk.Button(welcome_page_fm, text='Login Admin', bg=bg_color, fg='white', font=('Bold', 15), bd=0, command=forward_to_admin_login_page)
    login_admin_btn.place(x=120, y=225, width=200)

    student_admin_img = tk.Button(welcome_page_fm, image=login_admin_icon, bd=0, command=forward_to_admin_login_page)
    student_admin_img.place(x=60, y=200)

    # creating the student adding button

    add_student_btn = tk.Button(
        welcome_page_fm, text='Create Account', bg=bg_color, fg='white', font=('Bold', 15), bd=0, command=forward_to_add_account_page)
    add_student_btn.place(x=120, y=325, width=200)

    add_student_img = tk.Button(welcome_page_fm, image=add_student_icon, bd=0, command=forward_to_add_account_page)
    add_student_img.place(x=60, y=300)

    # creating a frame
    welcome_page_fm.pack(pady=30)
    welcome_page_fm.pack_propagate(False)
    welcome_page_fm.configure(width=400, height=420)

def sendmail_to_student(email, message, subject):
    smtp_server = 'smtp.gmail.com'
    smtp_port= 587

    username = my_email.email_address
    password = my_email.password

    msg = MIMEMultipart()

    msg['Subject'] = subject
    msg['From'] = username
    msg['To'] = email

    msg.attach(MIMEText(_text= message, _subtype= 'html'))
    smtp_connection = smtplib.SMTP(host= smtp_server, port= smtp_port)
    smtp_connection.starttls()
    smtp_connection.login(user=username, password=password)

    smtp_connection.sendmail(from_addr=username, to_addrs=email,
                             msg=msg.as_string())
    print('Mail send Successfullt...')

def forget_password_page():

    def recover_password():

        if check_id_already_exist(id_number=student_id_ent.get()):
            print('correct ID')

            mydb = mysql.connector.connect(host="127.0.0.1", user="root",
                                           password="tiger", database="students_account")
            cursor = mydb.cursor()
            id_number = student_id_ent.get()

            sql = "SELECT password FROM data WHERE id_number = %s"
            cursor.execute(sql, (id_number,))
            recovered_password = cursor.fetchall()[0][0]
            student_email = student_id_ent.get()

            sql_mail= "SELECT email FROM data WHERE id_number = %s"
            cursor.execute(sql_mail, (student_email,))
            student_email = cursor.fetchall()[0][0]

            cursor.close()
            mydb.close()

            confirmation = confirmation_box(message= f"""We will send \nYour Forgotten Password
Via your Email Address
                                            {student_email}                                            
Do you want to Continue?...""")
            
            if confirmation:
                msg= f"""<h1>Your Forgotten Password is: </h1>
                <h2>{recovered_password}</h2>
                <p>Once remember your password, After delete this message</p>"""
                sendmail_to_student(email=student_email, message=msg, subject= 'Password Recovered')

        else:
            print('Incorrect ID')
            message_box(message='! Invalid ID number')

    forget_password_page_fm = tk.Frame(root, highlightbackground=bg_color, highlightthickness=3)
    heading_lb = tk.Label(forget_password_page_fm, text='Forgetting Password',
                          font=('Bold', 15),bg=bg_color, fg='white')
    heading_lb.place(x=0, y=0, width=350)

    close_btn = tk.Button(forget_password_page_fm, text='X',
                          font=('Bold', 13), bg=bg_color, fg='white',
                          bd=0, command=lambda: forget_password_page_fm.destroy())
    close_btn.place(x=320, y=0)

    student_id_lb = tk.Label(forget_password_page_fm, text='Enter Student ID Number.',
                             font=('Bold', 13))
    student_id_lb.place(x=90, y=40)
    
    student_id_ent = tk.Entry(forget_password_page_fm, font=('Bold', 15),
                              justify=tk.CENTER)
    student_id_ent.place(x=70, y=70, width=180)

    info_lb = tk.Label(forget_password_page_fm, text="""Via Your Email Address
We will send to you
Your forget password.""", justify=tk.LEFT)
    info_lb.place(x=75, y=110)

    next_btn = tk.Button(forget_password_page_fm,
                         text='Next', font=('Bold', 13), bg= bg_color,
                         fg='white', command= recover_password)
    
    next_btn.place(x=130, y=200, width=80)

    forget_password_page_fm.place(x=75, y=120, width=350, height=250)


    def fetch_student_data(query):
        mydb = mysql.connector.connect(host="127.0.0.1", user="root",
                                   password="tiger", database="students_account")
        cursor = mydb.cursor()

        cursor.execute(query)

        response = cursor.fetchall()
        mydb.close()

        return response

    def student_dashboard(id_number):

        query = "SELECT * FROM data WHERE id_number = %s"
        get_student_details = fetch_student_data(query, (id_number,))

        for student_data in get_student_details:
            print(student_data)


    def switch(indicator, page):
        home_btn_indicator.config(bg='#c3c3c3')
        student_card_btn_indicator.config(bg='#c3c3c3')
        security_btn_indicator.config(bg='#c3c3c3')
        edit_data_btn_indicator.config(bg='#c3c3c3')
        delete_account_indicator.config(bg='#c3c3c3')
        
        indicator.config(bg=bg_color)

        for child in pages_fm.winfo_children():
            child.destroy()
            root.update()
        
        page()

    dashboard_fm = tk.Frame(root, highlightbackground=bg_color,
                            highlightthickness=3)

    options_fm = tk.Frame(dashboard_fm, highlightbackground=bg_color,
                         highlightthickness=2, bg='#c3c3c3')
    
    home_btn = tk.Button(options_fm, text='Home', font=('Bold', 15),
                         fg=bg_color, bg='#c3c3c3', bd=0,
                         command=lambda: switch(indicator= home_btn_indicator,
                                                page= home_page))
    home_btn.place(x=10, y=50)

    home_btn_indicator = tk.Label(options_fm, bg='#c3c3c3')
    home_btn_indicator.place(x=5, y=48, width=3, height=40)

    student_card_btn = tk.Button(options_fm, text='Student\nCard', font=('Bold', 15),
                         fg=bg_color, bg='#c3c3c3', bd=0, justify=tk.LEFT,
                         command=lambda: switch(indicator= student_card_btn_indicator,
                                                page= dashboard_student_card_page))
    student_card_btn.place(x=10, y=100)

    student_card_btn_indicator = tk.Label(options_fm, bg='#c3c3c3')
    student_card_btn_indicator.place(x=5, y=108, width=3, height=40)

    security_btn = tk.Button(options_fm, text='Security', font=('Bold', 15),
                         fg=bg_color, bg='#c3c3c3', bd=0,
                         command=lambda:switch(indicator=security_btn_indicator,
                                               page= security_page))
    security_btn.place(x=10, y=170)

    security_btn_indicator = tk.Label(options_fm, bg='#c3c3c3')
    security_btn_indicator.place(x=5, y=170, width=3, height=40)

    edit_data_btn = tk.Button(options_fm, text='Edit Data', font=('Bold', 15),
                         fg=bg_color, bg='#c3c3c3', bd=0,
                         command=lambda: switch(indicator= edit_data_btn_indicator,
                                                page=edit_data_page))
    edit_data_btn.place(x=10, y=220)

    edit_data_btn_indicator = tk.Label(options_fm, bg='#c3c3c3')
    edit_data_btn_indicator.place(x=5, y=220, width=3, height=40)

    delete_account_btn = tk.Button(options_fm, text='Delete\nAccount', font=('Bold', 15),
                         fg=bg_color, bg='#c3c3c3', bd=0, justify=tk.LEFT,
                         command=lambda: switch(indicator= delete_account_indicator,
                                                page=delete_account_page))
    delete_account_btn.place(x=10, y=270)

    delete_account_indicator = tk.Label(options_fm, bg='#c3c3c3')
    delete_account_indicator.place(x=5, y=280, width=3, height=40)

    logout_btn = tk.Button(options_fm, text='Logout', font=('Bold', 15),
                         fg=bg_color, bg='#c3c3c3', bd=0, justify=tk.LEFT)
    logout_btn.place(x=10, y=340)

    options_fm.place(x=0, y=0, width = 120, height = 575)

    def home_page():
        home_page_fm = tk.Frame(pages_fm)
        home_page_lb = tk.Label(home_page_fm, text='Home Page',
                                font=('Bold', 15))
        home_page_lb.place(x=100, y=200)
        home_page_fm.pack(fill=tk.BOTH, expand= True)

    def dashboard_student_card_page():
        student_card_page_fm = tk.Frame(pages_fm)
        student_card_page_lb = tk.Label(student_card_page_fm, text='Student Card Page',
                                font=('Bold', 15))
        student_card_page_lb.place(x=100, y=200)
        student_card_page_fm.pack(fill=tk.BOTH, expand= True)

    def security_page():
        security_page_fm = tk.Frame(pages_fm)
        security_page_lb = tk.Label(security_page_fm, text='Security Page',
                                font=('Bold', 15))
        security_page_lb.place(x=100, y=200)
        security_page_fm.pack(fill=tk.BOTH, expand= True)

    def edit_data_page():
        edit_data_page_fm = tk.Frame(pages_fm)
        edit_data_page_lb = tk.Label(edit_data_page_fm, text='Edit Page',
                                font=('Bold', 15))
        edit_data_page_lb.place(x=100, y=200)
        edit_data_page_fm.pack(fill=tk.BOTH, expand= True)

    def delete_account_page():
        delete_account_page_fm = tk.Frame(pages_fm)
        delete_account_page_lb = tk.Label(delete_account_page_fm, text='Delete Account Page',
                                font=('Bold', 15))
        delete_account_page_lb.place(x=100, y=200)
        delete_account_page_fm.pack(fill=tk.BOTH, expand= True)

    pages_fm = tk.Frame(dashboard_fm)
    pages_fm.place(x=122, y=5, width=350, height=550)
    home_page()

    dashboard_fm.pack(pady=5)
    dashboard_fm.pack_propagate(False)
    dashboard_fm.configure(width=480, height=580)

#Student login Page
def student_login_page():

    def show_hide_password():

        if password_ent['show'] == '*':
            
            password_ent.config(show='')
            show_hide_btn.config(image=unlocked_icon)

        else:   
            password_ent.config(show='*')
            show_hide_btn.config(image=locked_icon)

    def forward_to_welcome_page():
        student_login_page_fm.destroy()
        root.update()
        welcome_page()

    def forward_to_forget_password_page():
        forget_password_page()

    def remove_highlight_warning(entry):
        
        if entry['highlightbackground']!= 'gray':
            if entry.get() !='':
                entry.config(highlightcolor=bg_color, highlightbackground='gray')

    def login_account():
        id_number = id_number_ent.get()
        verify_id_number = check_id_already_exist(id_number=id_number)

        if verify_id_number:
            print('ID is correct')

            password = password_ent.get()
            verify_password = check_valid_password(id_number=id_number, password=password)

            if verify_password:
                student_login_page_fm.destroy()
                student_dashboard(student_id=id_number)
                root.update()
            else:
                print('! Please check Password')
                password_ent.config(highlightcolor='red', highlightbackground='red')
                message_box(message='! Incorrect Password')
        else:
            print('! Oops ID is Incorrect')
            id_number_ent.config(highlightcolor='red', highlightbackground='red')
            message_box(message='! Please Enter Valid Student ID')


    # Student Login Page
    student_login_page_fm = tk.Frame(root, highlightbackground=bg_color, highlightthickness=3)

    heading_lb = tk.Label(student_login_page_fm, text='Student Login Page', bg=bg_color, fg='white', font=('Bold', 18))
    heading_lb.place(x=0, y=0, width=400)

    back_btn = tk.Button(student_login_page_fm, text='⇦', font=('bold', 20),fg=bg_color, bd=0, command=forward_to_welcome_page)
    back_btn.place(x=5, y=40)

    stud_icon_lb = tk.Label(student_login_page_fm, image=login_student_icon)
    stud_icon_lb.place(x=150, y=40)

    id_number_lb = tk.Label(student_login_page_fm, text='Enter Student ID Number', font=('Bold', 15), fg=bg_color)
    id_number_lb.place(x=80, y=140)

    id_number_ent = tk.Entry(student_login_page_fm, font=('Bold', 15), justify=tk.CENTER, highlightcolor=bg_color, highlightbackground='gray', highlightthickness=2)
    id_number_ent.place(x=80, y=190)
    id_number_ent.bind('<KeyRelease>', lambda e: remove_highlight_warning(entry=id_number_ent))

    password_lb = tk.Label(student_login_page_fm, text='Enter Student Password', font=('Bold', 15), fg=bg_color)
    password_lb.place(x=80, y=240)

    password_ent = tk.Entry(student_login_page_fm, font=('Bold', 15), justify=tk.CENTER, highlightcolor=bg_color, highlightbackground='gray', highlightthickness=2, show='*')
    password_ent.place(x=80, y=290)
    password_ent.bind('<KeyRelease>', lambda e: remove_highlight_warning(entry=password_ent))

    show_hide_btn = tk.Button(student_login_page_fm, image=locked_icon, bd=0, command=show_hide_password)
    show_hide_btn.place(x=310, y=280)

    login_btn = tk.Button(student_login_page_fm, text = 'Login', font = ('Bold', 15), bg=bg_color, fg='white', command = login_account)
    login_btn.place (x=95, y=340, width=200, height=40) 

    forget_password_btn = tk.Button(student_login_page_fm, text='⚠\nForget Password', fg=bg_color, bd=0, command= forward_to_forget_password_page)
    forget_password_btn.place(x=150, y=390)

    student_login_page_fm.pack(pady=30)
    student_login_page_fm.pack_propagate(False)
    student_login_page_fm.configure(width=400, height=480)

def admin_login_page():

    def show_hide_password():
        if password_ent['show'] == '*':
            password_ent.config(show='')
            show_hide_btn.config(image=unlocked_icon)

        else:
            password_ent.config(show='*')
            show_hide_btn.config(image=locked_icon)

    def forward_to_welcome_page():
        admin_login_page_fm.destroy()
        root.update()
        welcome_page()

    admin_login_page_fm = tk.Frame(root, highlightbackground=bg_color, highlightthickness=3)

    heading_lb= tk.Label(admin_login_page_fm, text='Admin Login Page', font=('Bold',18), bg=bg_color, fg='white')
    heading_lb.place(x=0, y=0, width=400)

    back_btn = tk.Button(admin_login_page_fm, text='⇦', font=('bold', 20),fg=bg_color, bd=0, command=forward_to_welcome_page)
    back_btn.place(x=5, y=40)

    admin_icon_lb = tk.Label(admin_login_page_fm, image=login_admin_icon)
    admin_icon_lb.place(x=150, y=40)

    username_lb = tk.Label(admin_login_page_fm, text='Enter Admin User Name', font=('Bold',15), fg=bg_color)
    username_lb.place(x=80, y=140)

    username_ent = tk.Entry(admin_login_page_fm, font=('Bold', 15), justify=tk.CENTER, highlightcolor=bg_color, highlightbackground='gray', highlightthickness=2)
    username_ent.place(x=80, y=190)

    password_lb = tk.Label(admin_login_page_fm, text='Enter Admin Password', font=('Bold', 15), fg=bg_color)
    password_lb.place(x=80, y=240)

    password_ent = tk.Entry(admin_login_page_fm, font=('Bold', 15), justify=tk.CENTER, highlightcolor=bg_color, highlightbackground='gray', highlightthickness=2, show='*')
    password_ent.place(x=80, y=290)

    show_hide_btn = tk.Button(admin_login_page_fm, image=locked_icon, bd=0, command=show_hide_password)
    show_hide_btn.place(x=310, y=280)

    login_btn = tk.Button(admin_login_page_fm, text = 'Login', font = ('Bold', 15),bg=bg_color, fg='white')
    login_btn.place(x=95, y=340, width=200, height=40) 

    forget_password_btn = tk.Button(admin_login_page_fm, text='Forget Password', fg=bg_color, bd=0)
    forget_password_btn.place(x=150, y=390)

    admin_login_page_fm.pack(pady=30)
    admin_login_page_fm.pack_propagate(False)
    admin_login_page_fm.configure(width=400, height= 480)


student_gender = tk.StringVar()
class_list = ['5th', '6th', '7th', '8th', '9th', '10th', '11th', '12th']

def add_account_page():

    pic_path = tk.StringVar()
    pic_path.set('')

    def open_pic():
        path = askopenfilename()

        if path:
            img = ImageTk.PhotoImage(Image.open(path).resize((100, 100)))
            pic_path.set(path)

            add_pic_btn.config(image=img)
            add_pic_btn.image = img
            

    def forward_to_welcome_page():

        ans= confirmation_box(message='Do you want to leave\nRegistration Foam?')
        
        if ans:
            add_account_page_fm.destroy()
            root.update()
            welcome_page()
        
    def remove_highlight_warning(entry):
        if entry['highlightbackground']!= 'gray':
            if entry.get() !='':
                entry.config(highlightcolor=bg_color, highlightbackground='gray')
    
    def check_invalid_email(email):
        pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        match = re.match(pattern, email)
        return bool(match)
    
    def generate_id_number():
        generated_id = ''

        for r in range(6):
            generated_id += str(random.randint(0, 9))

        if not check_id_already_exist(id_number=generated_id):

            student_id.config(state=tk.NORMAL)
            student_id.delete(0, tk.END)
            student_id.insert(tk.END, generated_id)
            student_id.config(state='readonly')

        else:
            generate_id_number()

    def check_input_validation():
        
        if student_name_ent.get() == '':
            student_name_ent.config(highlightcolor='red', highlightbackground='red')
            student_name_ent.focus()
            message_box(message='Student Name Required')
        
        elif student_age_ent.get() == '':
            student_age_ent.config(highlightcolor='red', highlightbackground='red')
            student_age_ent.focus()
            message_box(message='Student Age Required')

        elif student_contact_ent.get() =='':
            student_contact_ent.config(highlightcolor='red', highlightbackground='red')
            student_contact_ent.focus()
            message_box(message='Student Contact Num Required')
        
        elif select_class_btn.get() =='':
            select_class_btn.focus()
            message_box(message='Select Student class is Required')

        elif student_email_ent.get() == '':
            student_email_ent.config(highlightcolor='red', highlightbackground='red')
            student_email_ent.focus()
            message_box(message='Student E-Mail Required')

        elif not check_invalid_email(email=student_email_ent.get().lower()):
            student_email_ent.config(highlightcolor='red', highlightbackground='red')
            student_email_ent.focus()
            message_box(message='Please Enter a Valid\nE-mail Address')

        elif account_password_ent.get() == '':
            account_password_ent.config(highlightcolor='red', highlightbackground='red')
            account_password_ent.focus()
            message_box(message='Must Create a Password')

        else:
            pic_data = b''
           
            if pic_path.get():

                resize_pic = Image.open(pic_path.get()).resize((100, 100))
                resize_pic.save('temp_pic.png')

                read_data = open('temp_pic.png', 'rb')
                pic_data = read_data.read()
                read_data.close()

            else:
                read_data = open('images/add_image.png', 'rb')
                pic_data = read_data.read()
                read_data.close()
                pic_path.set('images/add_image.png')


            add_data(
                id_number=student_id.get(),
                password=account_password_ent.get(), 
                name=student_name_ent.get(),
                age=student_age_ent.get(),
                gender=student_gender.get(),
                phone_number=student_contact_ent.get(),
                student_class=select_class_btn.get(),
                email=student_email_ent.get(),
                pic_data=pic_data)

            

            data=f"""
{student_id.get()}
{student_name_ent.get()}
{student_gender.get()}
{student_age_ent.get()}
{select_class_btn.get()}
{student_contact_ent.get()}
{student_email_ent.get()}
"""

            get_student_card = draw_student_card(student_pic_path=pic_path.get(), student_data=data)
            student_card_page(student_card_obj=get_student_card)

            add_account_page_fm.destroy()
            root.update()

            message_box('Account Created Successfully...')


    add_account_page_fm = tk.Frame(root, highlightbackground=bg_color, highlightthickness=3)

    add_pic_section_fm = tk.Frame(add_account_page_fm, highlightbackground=bg_color, highlightthickness=2)

    add_pic_btn = tk.Button(add_pic_section_fm, image=add_student_pic_icon, bd=0, command=open_pic)
    add_pic_btn.pack()

    add_pic_section_fm.place(x=5, y=5, width=105, height=105)

    student_name_lb = tk.Label(add_account_page_fm, text='Enter Student Full Name: ', font=('Bold', 12))
    student_name_lb.place(x=5, y=130)

    student_name_ent = tk.Entry(add_account_page_fm, font=('Bold', 15), highlightcolor=bg_color, highlightbackground='gray',
                                highlightthickness=2)
    student_name_ent.place(x=5, y=160, width=180)
    student_name_ent.bind('<KeyRelease>', lambda e: remove_highlight_warning(entry=student_name_ent))

    student_gender_lb = tk.Label(add_account_page_fm,text='Select Gender', font=('Bold', 12))
    student_gender_lb.place(x=5, y=210)

    male_gender_btn = tk.Radiobutton(add_account_page_fm, text='Male', font=('Bold', 12), variable=student_gender, value='male')
    male_gender_btn.place(x=5, y=235)

    female_gender_btn = tk.Radiobutton(add_account_page_fm, text='female', font=('Bold', 12), variable=student_gender, value='female')
    female_gender_btn.place(x=75, y=235)

    student_gender.set('male')

    student_age_lb = tk.Label(add_account_page_fm, text='Enter Student Age', font=('Bold', 12))
    student_age_lb.place(x=5, y=275)

    student_age_ent = tk.Entry(add_account_page_fm, font=('Bold', 15), highlightcolor=bg_color, highlightbackground='gray',
                                highlightthickness=2)
    student_age_ent.place(x=5, y=305, width=180)
    student_age_ent.bind('<KeyRelease>', lambda e: remove_highlight_warning(entry=student_age_ent))

    student_contact_lb = tk.Label(add_account_page_fm, text='Enter Contact', font=('Bold', 12))
    student_contact_lb.place(x=5, y=360)

    student_contact_ent = tk.Entry(add_account_page_fm, font=('Bold', 15), highlightcolor=bg_color, highlightbackground='gray',
                                highlightthickness=2)
    student_contact_ent.place(x=5, y=390, width=180)
    student_contact_ent.bind('<KeyRelease>', lambda e: remove_highlight_warning(entry=student_contact_ent))

    student_class_lb = tk.Label(add_account_page_fm, text='Enter Class', font=('Bold', 12))
    student_class_lb.place(x=5, y=445)

    select_class_btn = Combobox(add_account_page_fm, font=('Bold', 15), state='readonly', values= class_list)
    select_class_btn.place(x=5, y=475, width= 180, height=30)
    

    student_id_lb = tk.Label(add_account_page_fm, text = 'Student ID Number: ', font=('Bold', 12))
    student_id_lb.place(x=240, y=35)

    student_id = tk.Entry(add_account_page_fm, font=('Bold', 18), bd=0)
    student_id.place(x=380, y=35, width=80)

    
    student_id.config(state='readonly')

    generate_id_number()

    id_info_lb = tk.Label(add_account_page_fm, text="""Automatically Generated ID Number
! Remember Using This ID Number 
Student will Login Account""", justify=tk.LEFT)
    id_info_lb.place(x=240, y=65)

    student_email_lb = tk.Label(add_account_page_fm, text='Enter Email', font=('Bold', 12))
    student_email_lb.place(x=240, y=130)

    student_email_ent = tk.Entry(add_account_page_fm, font=('Bold', 15), highlightcolor=bg_color, highlightbackground='gray',
                                highlightthickness=2)
    student_email_ent.place(x=240, y=160, width=180)
    student_email_ent.bind('<KeyRelease>', lambda e: remove_highlight_warning(entry=student_email_ent))

    email_info_lb = tk.Label(add_account_page_fm, text="""Via Email Address Student
can Recover Account
! In Case Forgetting Password & also
Student will get Future Notifications""", justify=tk.LEFT)
    email_info_lb.place(x=240, y=200)

    account_password_lb = tk.Label(add_account_page_fm, text='Create Account Password', font=('Bold', 12))
    account_password_lb.place(x=240, y=275)

    account_password_ent = tk.Entry(add_account_page_fm, font=('Bold', 15), highlightcolor=bg_color, highlightbackground='gray',
                                highlightthickness=2)
    account_password_ent.place(x=240, y=307, width=180)
    account_password_ent.bind('<KeyRelease>', lambda e: remove_highlight_warning(entry=account_password_ent))

    account_password_info_lb = tk.Label(add_account_page_fm, text= """Via Student Create Password
and Provided Student ID Number
Student can Login Account""", justify=tk.LEFT)
    account_password_info_lb.place(x=240, y=345)

    home_btn= tk.Button(add_account_page_fm, text='HOME', font=('Bold', 15), bg='red', fg='white', bd=0, command=forward_to_welcome_page)
    home_btn.place(x=240, y=420)

    submit_btn= tk.Button(add_account_page_fm, text='SUBMIT', font=('Bold', 15), bg=bg_color, fg='white', bd=0, command = check_input_validation)
    submit_btn.place(x=330, y=420)

    add_account_page_fm.pack(pady=5)
    add_account_page_fm.pack_propagate(False)
    add_account_page_fm.configure(width=480, height= 580)

#add_account_page()
#init_database()
#student_dashboard()
student_login_page()
root.mainloop()