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