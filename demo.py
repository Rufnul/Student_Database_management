import tkinter as tk

# initialize the window and title
root = tk.Tk()
root.geometry('500x600')
root.title('TKinter Hub (Students Management and Registration Hub)')

bg_color = '#273b7a'

# Note: Ensure the image paths are correct and the image files exist
login_student_icon = tk.PhotoImage(file='images/login_student_img.png')
login_admin_icon = tk.PhotoImage(file='images/admin_img.png')
add_student_icon = tk.PhotoImage(file='images/First_Img.png')
locked_icon = tk.PhotoImage(file='images/locked.png')
unlocked_icon = tk.PhotoImage(file='images/unlocked.png')

def welcome_page():
    def forward_to_student_login_page():
        welcome_page_fm.destroy()
        root.update()
        student_login_page()

    def forward_to_admin_login_page():
        welcome_page_fm.destroy()
        root.update()
        admin_login_page()

    welcome_page_fm = tk.Frame(root, highlightbackground=bg_color, highlightthickness=3)

    heading_lb = tk.Label(welcome_page_fm, text='Welcome To\nStudent Registration/\nManagement System', bg=bg_color, fg='white', font=('bold', 16))
    heading_lb.place(x=0, y=0, width=400)

    student_login_btn = tk.Button(welcome_page_fm, text='Login Student', bg=bg_color, fg='white', font=('Bold', 15), bd=0, command=forward_to_student_login_page)
    student_login_btn.place(x=120, y=125, width=200)

    student_login_img = tk.Label(welcome_page_fm, image=login_student_icon)
    student_login_img.place(x=60, y=100)

    login_admin_btn = tk.Button(welcome_page_fm, text='Login Admin', bg=bg_color, fg='white', font=('Bold', 15), bd=0, command=forward_to_admin_login_page)
    login_admin_btn.place(x=120, y=225, width=200)

    student_admin_img = tk.Label(welcome_page_fm, image=login_admin_icon)
    student_admin_img.place(x=60, y=200)

    add_student_btn = tk.Button(welcome_page_fm, text='Create Account', bg=bg_color, fg='white', font=('Bold', 15), bd=0)
    add_student_btn.place(x=120, y=325, width=200)

    add_student_img = tk.Label(welcome_page_fm, image=add_student_icon)
    add_student_img.place(x=60, y=300)

    welcome_page_fm.pack(pady=30)
    welcome_page_fm.pack_propagate(False)
    welcome_page_fm.configure(width=400, height=420)

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

    password_lb = tk.Label(student_login_page_fm, text='Enter Student Password', font=('Bold', 15), fg=bg_color)
    password_lb.place(x=80, y=240)

    password_ent = tk.Entry(student_login_page_fm, font=('Bold', 15), justify=tk.CENTER, highlightcolor=bg_color, highlightbackground='gray', highlightthickness=2, show='*')
    password_ent.place(x=80, y=290)

    show_hide_btn = tk.Button(student_login_page_fm, image=locked_icon, bd=0, command=show_hide_password)
    show_hide_btn.place(x=310, y=280)

    login_btn = tk.Button(student_login_page_fm, text = 'Login', font = ('Bold', 15), bg=bg_color, fg='white')
    login_btn.place (x=95, y=340, width=200, height=40) 

    forget_password_btn = tk.Button(student_login_page_fm, text='Forget Password', fg=bg_color, bd=0)
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


    admin_login_page_fm.pack(pady=30)
    admin_login_page_fm.pack_propagate(False)
    admin_login_page_fm.configure(width=400, height= 430)

welcome_page()
root.mainloop()
