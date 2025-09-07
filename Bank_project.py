from tkinter import Tk,Label,Frame,Entry,Button,messagebox
from tkinter.ttk import Combobox
from Captcha_test import generate_captcha
from PIL import Image,ImageTk
import time,random
from table_creation import generate
from email_test import send_openacn_ack,send_otp,send_otp_for_pass
import sqlite3
import re

generate()

def show_dt():
    dt=time.strftime("%A %d-%b-%Y %r")
    dt_lbl.configure(text=dt)
    dt_lbl.after(1000,show_dt) #ms (2sec)

list_imgs=['Images/logo1.jpg','Images/logo2.png','Images/logo3.jpg','Images/logo4.jpg']
def image_animation(): 
    index=random.randint(0,3)
    img=Image.open(list_imgs[index]).resize((180,92))
    imgtk=ImageTk.PhotoImage(img,master=root)
    logo_lbl=Label(root,image=imgtk)
    logo_lbl.place(relx=0,rely=0)
    logo_lbl.image=imgtk
    logo_lbl.after(500,image_animation)

root=Tk()
root.state('zoomed')
root.configure(bg="pink")

tittle_lab=Label(root,text="Banking Automation",fg="black",bg='pink',font=('Century',40,'bold','underline'))
tittle_lab.pack()

dt_lbl=Label(root,font=('Algerian',15),bg='pink',fg='black')
dt_lbl.pack()
show_dt()

img=Image.open("Images/logo.jpg").resize((180,92))
imgtk=ImageTk.PhotoImage(img,master=root)

logo_lb2=Label(root,image=imgtk)
logo_lb2.place(relx=1.0,rely=0.0,anchor='ne')

image_animation()

footer_lbl=Label(root,font=('Calibri',20,'bold'),bg='pink',text="Developed BY:\nHemant @ 8299733436")
footer_lbl.pack(side='bottom')

code_captcha=generate_captcha()

def main_screen():
    def refresh_captcha():
        global code_captcha
        code_captcha=new_captcha=generate_captcha()
        captcha_value_lbl.configure(text=code_captcha)
 

    frm=Frame(root,highlightbackground='brown',highlightthickness=2)
    frm.configure(bg='powder blue')
    frm.place(relx=0,rely=.12,relwidth=1,relheight=.8)


    def forgot():
        frm.destroy()
        fp_screen()
    
    def login():
        utype=acntype_cb.get()
        uacn=acnno_e.get()
        upass=pass_e.get()

        ucaptcha=captcha_e.get()
        global code_captcha
        code_captcha= code_captcha.replace(' ','')

        if utype=="Admin":
            if uacn=='0' and upass=='admin':
                if code_captcha==ucaptcha:
                    frm.destroy()
                    admin_screen()
                else:
                    messagebox.showerror("Login","Invalid Captcha")  
            else:
                messagebox.showerror("Login","You are not Admin!")    
        else:
            
            if code_captcha==ucaptcha:

                conobj=sqlite3.connect(database='bank.sqlite')
                curobj=conobj.cursor()
                query='select * from accounts where acn_acno=? and acn_pass=?'
                curobj.execute(query,(uacn,upass))
                row=curobj.fetchone()
                if row==None:
                    messagebox.showerror("Login",'Invalid ACN/PASS')
                else:
                    frm.destroy()
                    user_screen(row[0],row[1])
            else:
                messagebox.showerror("Login","Invalid Captcha")        
                
    acntype_lbl=Label(frm,text='ACN Type👤',font=('Calibri',20,'bold'),bg='powder blue')
    acntype_lbl.place(relx=.3,rely=.1)

    acntype_cb=Combobox(frm,values=['User','Admin'],font=('Calibri',20,'bold'))
    acntype_cb.current(0)
    acntype_cb.place(relx=.4,rely=.1)

    acnno_lbl=Label(frm,text='AC NO.🔑',font=('Calibri',20,'bold'),bg='powder blue')
    acnno_lbl.place(relx=.3,rely=.2)

    acnno_e=Entry(frm,font=('Calibri',20,'bold'),bd=5)
    acnno_e.place(relx=.40,rely=.2)
    acnno_e.focus()

    pass_lbl=Label(frm,text='Password🔒',font=('Calibri',20,'bold'),bg='powder blue')
    pass_lbl.place(relx=.3,rely=.3)

    pass_e=Entry(frm,font=('Calibri',20,'bold'),bd=5,show='*')
    pass_e.place(relx=.40,rely=.3)

    captcha_lbl=Label(frm,text='captcha',font=('Calibri',20,'bold'),bg='powder blue')
    captcha_lbl.place(relx=.3,rely=.4)

    captcha_value_lbl=Label(frm,text=code_captcha,fg='green',font=('Calibri',20,'bold'))
    captcha_value_lbl.place(relx=.40,rely=.4)

    refresh_btn=Button(frm,text="🔄",command=refresh_captcha)
    refresh_btn.place(relx=.5,rely=.4,width=40,height=40)

    captcha_e=Entry(frm,font=('Calibri',20,'bold'),bd=5)
    captcha_e.place(relx=.40,rely=.5)

    submit_btn=Button(frm,text="Login",width=15,bd=5,font=('Arial',20,),command=login)
    submit_btn.place(relx=.41,rely=.6)

    fp_btn=Button(frm,text="Forgot Passward",command=forgot,bd=5,font=('Arial',20,))
    fp_btn.place(relx=.42,rely=.75)

def fp_screen():
    frm=Frame(root,highlightbackground='brown',highlightthickness=2)
    frm.configure(bg='grey')
    frm.place(relx=0,rely=.12,relwidth=1,relheight=.8) 

    def back():
        frm.destroy()
        main_screen()

    def fb_pass():
        uemail=email_e.get()
        uacn=acnno_e.get()

        conobj=sqlite3.connect(database='bank.sqlite')
        curobj=conobj.cursor()
        query='select * from accounts where acn_acno=?'
        curobj.execute(query,(uacn,))
        torow=curobj.fetchone()
        if torow==None:
             messagebox.showinfo("Forgot Password","To ACN does not exist")
        else:
            if uemail==torow[3]:
                otp=random.randint(1000,9999)
                send_otp_for_pass(uemail,otp)
                messagebox.showinfo("Forgot Password","OTP send to registerd email,kindlty verify")

                def verify_otp():
                        uotp=int(otp_e.get())
                        if otp==uotp:
                            conobj=sqlite3.connect(database='bank.sqlite')
                            curobj=conobj.cursor()

                            query='select acn_pass from accounts where acn_acno=?'
                            curobj.execute(query,(uacn,))
                            
                            messagebox.showinfo('Forgot Password',f"Your Password is {curobj.fetchone()[0]}")
                            conobj.close()
                            frm.destroy()
                            main_screen()
                        else:
                            messagebox.showerror("Forgot Password","Invalid OTP")

                otp_e=Entry(frm,font=('Calibri',20,'bold'),bd=5)
                otp_e.place(relx=.4,rely=.7)
                otp_e.focus()
            

                verify_btn=Button(frm,text="Verify",width=10,fg='black',bd=5,font=('Arial',15),command=verify_otp)
                verify_btn.place(relx=.8,rely=.8)
             

            else:
                messagebox.showinfo("Forgot Password","Email is not matched")
                

    back_btn=Button(frm,text=" 🔙 ",bg='white',bd=5,font=('Arial',20,'bold'),command=back)
    back_btn.place(relx=0,rely=0)

    acnno_lbl=Label(frm,text='AC NO.🔑',font=('Calibri',20,'bold'),bg='powder blue')
    acnno_lbl.place(relx=.3,rely=.2)

    acnno_e=Entry(frm,font=('Calibri',20,'bold'),bd=5)
    acnno_e.place(relx=.40,rely=.2)
    acnno_e.focus()

    email_lbl=Label(frm,text='Email📧',font=('Calibri',20,'bold'),bg='powder blue')
    email_lbl.place(relx=.3,rely=.3)

    email_e=Entry(frm,font=('Calibri',20,'bold'),bd=5)
    email_e.place(relx=.40,rely=.3)

    sub_btn=Button(frm,text="Submit",bd=5,font=('Arial',20,'bold'),command=fb_pass)
    sub_btn.place(relx=.45,rely=.4)

def admin_screen():
    frm=Frame(root,highlightbackground='brown',highlightthickness=2)
    frm.configure(bg="#00ffbf")
    frm.place(relx=0,rely=.12,relwidth=1,relheight=.8) 

    def logout():
        frm.destroy()
        main_screen()

    logout_btn=Button(frm,text="Logout",bg='white',bd=5,font=('Arial',20,'bold'),command=logout)
    logout_btn.place(relx=.9,rely=0)


    def open():
        ifrm=Frame(frm,highlightbackground='black',highlightthickness=2)
        ifrm.configure(bg="white")
        ifrm.place(relx=.2,rely=.2,relwidth=.7,relheight=.6) 

        t_lbl=Label(ifrm,text='This is open account screen',font=('Calibri',20,'bold'),bg='white',fg='purple')
        t_lbl.pack()

        def openac():
            uname=name_e.get()
            uemail=email_e.get()
            umob=mob_e.get()
            uadhar=adhar_e.get()
            uadr=adr_e.get()
            udob=dob_e.get()
            upass=generate_captcha()
            upass=upass.replace(' ','')
            ubal=0
            uopendate=time.strftime("%A %d-%b-%Y")

            # Empty Validation
            if len(uname)==0 or len(uemail)==0 or len(umob)==0 or len(uadhar)==0 or len(uadr)==0 or len(udob)==0:
                messagebox.showerror("Open Account","All Fields are Mandatory")
                return
            
            #email validation
            match=re.fullmatch(r"[a-zA-Z0-9_.]+@[a-zA-Z0-9]+\.[a-zA-Z]+",uemail)
            if match==None:
                 messagebox.showerror("Open Account","Kindly check email")
                 return
            
            #mobile no validation
            match=re.fullmatch("[6-9][0-9]{9}",umob)
            if match==None:
                 messagebox.showerror("Open Account","Kindly check mobile No.")
                 return
            
            #adhar no validation
            match=re.fullmatch("[0-9]{12}",uadhar)
            if match==None:
                 messagebox.showerror("Open Account","Kindly check adhar no.")
                 return
            
            conobj=sqlite3.connect(database='bank.sqlite')
            curobj=conobj.cursor()
            query='insert into accounts values(null,?,?,?,?,?,?,?,?,?)'
            curobj.execute(query,(uname,upass,uemail,umob,uadhar,uadr,udob,ubal,uopendate))
            conobj.commit()
            conobj.close()

            conobj=sqlite3.connect(database='bank.sqlite')
            curobj=conobj.cursor()
            curobj.execute("select max(acn_acno) from accounts")
            uacn=curobj.fetchone()[0]
            conobj.close()

            send_openacn_ack(uemail,uname,uacn,upass)
            messagebox.showinfo("Account","Account Opened and details send to email")
            frm.destroy()
            admin_screen()

        name_lbl=Label(ifrm,text='Name',font=('Calibri',20,'bold'),bg='white')
        name_lbl.place(relx=.05,rely=.15)

        name_e=Entry(ifrm,font=('Calibri',20,'bold'),bd=5)
        name_e.place(relx=.15,rely=.15)
        name_e.focus()  

        email_lbl=Label(ifrm,text='Email',font=('Calibri',20,'bold'),bg='white')
        email_lbl.place(relx=.05,rely=.4)

        email_e=Entry(ifrm,font=('Calibri',20,'bold'),bd=5)
        email_e.place(relx=.15,rely=.4)

        mob_lbl=Label(ifrm,text='Mob',font=('Calibri',20,'bold'),bg='white')
        mob_lbl.place(relx=.05,rely=.65)

        mob_e=Entry(ifrm,font=('Calibri',20,'bold'),bd=5)
        mob_e.place(relx=.15,rely=.65)

        adhar_lbl=Label(ifrm,text='Adhar',font=('Calibri',20,'bold'),bg='white')
        adhar_lbl.place(relx=.5,rely=.15)

        adhar_e=Entry(ifrm,font=('Calibri',20,'bold'),bd=5)
        adhar_e.place(relx=.6,rely=.15)

        adr_lbl=Label(ifrm,text='Adress',font=('Calibri',20,'bold'),bg='white')
        adr_lbl.place(relx=.5,rely=.4)

        adr_e=Entry(ifrm,font=('Calibri',20,'bold'),bd=5)
        adr_e.place(relx=.6,rely=.4)
        
        dob_lbl=Label(ifrm,text='DOB',font=('Calibri',20,'bold'),bg='white')
        dob_lbl.place(relx=.5,rely=.65)

        dob_e=Entry(ifrm,font=('Calibri',20,'bold'),bd=5)
        dob_e.place(relx=.6,rely=.65)

        open_btn=Button(ifrm,text="Open ACN",fg="#f200ff",bd=5,font=('Arial',20,),command=openac)
        open_btn.place(relx=.8,rely=.8)

    def close():
        ifrm=Frame(frm,highlightbackground='black',highlightthickness=2)
        ifrm.configure(bg="white")
        ifrm.place(relx=.2,rely=.2,relwidth=.7,relheight=.6) 

        t_lbl=Label(ifrm,text='This is close account screen',font=('Calibri',20,'bold'),bg='white',fg='purple')
        t_lbl.pack()

        def send_close_otp():
            uacn=acnno_e.get()

            conobj=sqlite3.connect(database='bank.sqlite')
            curobj=conobj.cursor()
            query='select * from accounts where acn_acno=?'
            curobj.execute(query,(uacn,))
            torow=curobj.fetchone()
            if torow==None:
             messagebox.showinfo("Close Account","To ACN does not exist")
            else:
                otp=random.randint(1000,9999)
                send_otp_for_pass(torow[3],otp)
                messagebox.showinfo("Close Account","OTP send to registerd email,kindlty verify")

                def verify_otp():
                        uotp=int(otp_e.get())
                        if otp==uotp:
                            conobj=sqlite3.connect(database='bank.sqlite')
                            curobj=conobj.cursor()

                            query='delete from accounts where acn_acno=?'
                            curobj.execute(query,(uacn,))
                            
                            messagebox.showinfo('Close Account',"Account closed")
                            conobj.commit()
                            conobj.close()
                            frm.destroy()
                            admin_screen()
                        else:
                            messagebox.showerror("Close Account","Invalid OTP")

                otp_e=Entry(frm,font=('Calibri',20,'bold'),bd=5)
                otp_e.place(relx=.5,rely=.6)
                otp_e.focus()
            

                verify_btn=Button(frm,text="Verify",width=10,fg='black',bd=5,font=('Arial',15),command=verify_otp)
                verify_btn.place(relx=.8,rely=.7)
             

        acnno_lbl=Label(ifrm,text='AC NO.🔑',font=('Calibri',20,'bold'),bg='powder blue')
        acnno_lbl.place(relx=.3,rely=.2)

        acnno_e=Entry(ifrm,font=('Calibri',20,'bold'),bd=5)
        acnno_e.place(relx=.45,rely=.2)
        acnno_e.focus()

        otp_btn=Button(ifrm,text="Send OTP",fg="#ff1900",bd=5,font=('Arial',20,),command=send_close_otp)
        otp_btn.place(relx=.5,rely=.4)

    def view():
        ifrm=Frame(frm,highlightbackground='black',highlightthickness=2)
        ifrm.configure(bg="white")
        ifrm.place(relx=.2,rely=.2,relwidth=.7,relheight=.6) 

        t_lbl=Label(ifrm,text='This is view account screen',font=('Calibri',20,'bold'),bg='white',fg='purple')
        t_lbl.pack()

        from tktable import Table

        table_headers=("ACNO.","NAME","Email","MOB","OPEN DATE","BALANCE")
        mytable = Table(ifrm, table_headers,headings_bold=True)
        mytable.place(relx=.1,rely=.1,relheight=.4,relwidth=.8)

        conobj=sqlite3.connect(database='bank.sqlite')
        curobj=conobj.cursor()
        query='select acn_acno,acn_name,acn_email,acn_mob,acn_opendate,acn_bal from accounts'
        curobj.execute(query)
        for tup in curobj.fetchall():
            mytable.insert_row(tup)
        conobj.close()    


    open_btn=Button(frm,text="Open ACN",width=10,fg="#8c00ff",bd=5,font=('Arial',20,),command=open)
    open_btn.place(relx=.001,rely=.1)

    close_btn=Button(frm,text="Close ACN",width=10,fg='red',bd=5,font=('Arial',20,),command=close)
    close_btn.place(relx=.001,rely=.3)

    view_btn=Button(frm,text="View ACN",width=10,fg='blue',bd=5,font=('Arial',20),command=view)
    view_btn.place(relx=.001,rely=.5)

def user_screen(uacn,uname):
    frm=Frame(root,highlightbackground='brown',highlightthickness=2)
    frm.configure(bg="#00ddff")
    frm.place(relx=0,rely=.12,relwidth=1,relheight=.8) 

    conobj=sqlite3.connect(database='bank.sqlite')
    curobj=conobj.cursor()
    query='select * from accounts where acn_acno=?'
    curobj.execute(query,(uacn,))
    row=curobj.fetchone()
    conobj.close()

    def logout():
        frm.destroy()
        main_screen()
    
    def check():
        ifrm=Frame(frm,highlightbackground='black',highlightthickness=2)
        ifrm.configure(bg="white")
        ifrm.place(relx=.23,rely=.2,relwidth=.7,relheight=.6) 

        t_lbl=Label(ifrm,text='This is check details screen',font=('Calibri',20,'bold'),bg='white',fg='purple')
        t_lbl.pack()

        acn_lbl=Label(ifrm,text=f"Account No.\t=\t{row[0]}",font=('Calibri',18),bg='white',fg='black')
        acn_lbl.place(relx=.2,rely=.1)

        bal_lbl=Label(ifrm,text=f"Account Bal.\t=\t{row[8]}",font=('Calibri',18),bg='white',fg='black')
        bal_lbl.place(relx=.2,rely=.3)

        opendate_lbl=Label(ifrm,text=f"Open Date\t=\t{row[9]}",font=('Calibri',18),bg='white',fg='black')
        opendate_lbl.place(relx=.2,rely=.5)

        dob_lbl=Label(ifrm,text=f"Date of Birth\t=\t{row[7]}",font=('Calibri',18),bg='white',fg='black')
        dob_lbl.place(relx=.2,rely=.7)

        adhar_lbl=Label(ifrm,text=f"ADHAR NO.\t=\t{row[5]}",font=('Calibri',18),bg='white',fg='black')
        adhar_lbl.place(relx=.2,rely=.9)

    def update():
        ifrm=Frame(frm,highlightbackground='black',highlightthickness=2)
        ifrm.configure(bg="white")
        ifrm.place(relx=.23,rely=.2,relwidth=.7,relheight=.6) 

        t_lbl=Label(ifrm,text='This is update details screen',font=('Calibri',20,'bold'),bg='white',fg='purple')
        t_lbl.pack()


        def update_details():
            uname=name_e.get()
            upass=pass_e.get()
            uemail=email_e.get()
            umob=mob_e.get()

            conobj=sqlite3.connect(database='bank.sqlite')
            curobj=conobj.cursor()
            query='update accounts set acn_name=?,acn_pass=?,acn_email=?,acn_mob=? where acn_acno=?'
            curobj.execute(query,(uname,upass,uemail,umob,uacn))
            conobj.commit()
            conobj.close()
            messagebox.showinfo("Update","Details Updated")
            frm.destroy()
            user_screen(uacn,None)

        name_lbl=Label(ifrm,text='Name',font=('Calibri',20,'bold'),bg='white')
        name_lbl.place(relx=.05,rely=.15)

        name_e=Entry(ifrm,font=('Calibri',20,'bold'),bd=5)
        name_e.place(relx=.15,rely=.15)
        name_e.focus()  
        name_e.insert(0,row[1])

        email_lbl=Label(ifrm,text='Email',font=('Calibri',20,'bold'),bg='white')
        email_lbl.place(relx=.05,rely=.4)

        email_e=Entry(ifrm,font=('Calibri',20,'bold'),bd=5)
        email_e.place(relx=.15,rely=.4)
        email_e.insert(0,row[3])

        mob_lbl=Label(ifrm,text='Mob',font=('Calibri',20,'bold'),bg='white')
        mob_lbl.place(relx=.5,rely=.4)

        mob_e=Entry(ifrm,font=('Calibri',20,'bold'),bd=5)
        mob_e.place(relx=.6,rely=.4)
        mob_e.insert(0,row[4])

        pass_lbl=Label(ifrm,text='Pass',font=('Calibri',20,'bold'),bg='white')
        pass_lbl.place(relx=.5,rely=.15)

        pass_e=Entry(ifrm,font=('Calibri',20,'bold'),bd=5)
        pass_e.place(relx=.6,rely=.15)
        pass_e.insert(0,row[2])

        update_btn=Button(ifrm,text="Update⟳",width=10,fg='black',bd=5,font=('Arial',20),command=update_details)
        update_btn.place(relx=.4,rely=.65)


    def deposit():
        ifrm=Frame(frm,highlightbackground='black',highlightthickness=2)
        ifrm.configure(bg="white")
        ifrm.place(relx=.23,rely=.2,relwidth=.7,relheight=.6) 

        t_lbl=Label(ifrm,text='This is deposit screen',font=('Calibri',20,'bold'),bg='white',fg='purple')
        t_lbl.pack()

        def deposit_amt():
            uamt=float(amt_e.get())
            conobj=sqlite3.connect(database='bank.sqlite')
            curobj=conobj.cursor()
            query='update accounts set acn_bal=acn_bal+? where acn_acno=?'
            curobj.execute(query,(uamt,uacn))
            conobj.commit()
            conobj.close()
            messagebox.showinfo('Deposit',f"{uamt} Amount Deposited")
            frm.destroy()
            user_screen(uacn,None)


        amt_lbl=Label(ifrm,text='Amount',font=('Calibri',20,'bold'),bg='white')
        amt_lbl.place(relx=.3,rely=.15)

        amt_e=Entry(ifrm,font=('Calibri',20,'bold'),bd=5)
        amt_e.place(relx=.4,rely=.15)
        amt_e.focus()

        deposit_btn=Button(ifrm,text="Deposit",width=10,fg='green',bd=5,font=('Arial',20),command=deposit_amt)
        deposit_btn.place(relx=.6,rely=.3)


    def withdraw():
        ifrm=Frame(frm,highlightbackground='black',highlightthickness=2)
        ifrm.configure(bg="white")
        ifrm.place(relx=.23,rely=.2,relwidth=.7,relheight=.6) 

        t_lbl=Label(ifrm,text='This is withdraw screen',font=('Calibri',20,'bold'),bg='white',fg='purple')
        t_lbl.pack()

        def withdraw_amt():
            uamt=float(amt_e.get())
            if row[8]>=uamt:
                conobj=sqlite3.connect(database='bank.sqlite')
                curobj=conobj.cursor()
                query='update accounts set acn_bal=acn_bal-? where acn_acno=?'
                curobj.execute(query,(uamt,uacn))
                conobj.commit()
                conobj.close()
                messagebox.showinfo('Withdraw',f"{uamt} Amount Withdrawn")
                frm.destroy()
                user_screen(uacn,None)
            else:
                messagebox.showerror("Withdraw","Insufficent Balance")    


        amt_lbl=Label(ifrm,text='Amount',font=('Calibri',20,'bold'),bg='white')
        amt_lbl.place(relx=.3,rely=.15)

        amt_e=Entry(ifrm,font=('Calibri',20,'bold'),bd=5)
        amt_e.place(relx=.4,rely=.15)
        amt_e.focus()

        withdraw_btn=Button(ifrm,text="Withdraw",width=10,fg='brown',bd=5,font=('Arial',20),command=withdraw_amt)
        withdraw_btn.place(relx=.6,rely=.3)


    def transfer():
        ifrm=Frame(frm,highlightbackground='black',highlightthickness=2)
        ifrm.configure(bg="white")
        ifrm.place(relx=.23,rely=.2,relwidth=.7,relheight=.6) 

        t_lbl=Label(ifrm,text='This is transfer screen',font=('Calibri',20,'bold'),bg='white',fg='purple')
        t_lbl.pack()   

        def transfer_amt():
            toacn=to_e.get()
            uamt=float(amt_e.get())

            conobj=sqlite3.connect(database='bank.sqlite')
            curobj=conobj.cursor()
            query='select * from accounts where acn_acno=?'
            curobj.execute(query,(toacn,))
            torow=curobj.fetchone()
            if torow==None:
                messagebox.showinfo("Transfer","To ACN does not exist")
            else:
                if row[8]>=uamt:
                    otp=random.randint(1000,9999)
                    send_otp(row[3],otp,uamt)
                    messagebox.showinfo("Transfer","OTP send to registerd email,kindlty verify")

                    def verify_otp():
                        uotp=int(otp_e.get())
                        if otp==uotp:
                            conobj=sqlite3.connect(database='bank.sqlite')
                            curobj=conobj.cursor()

                            query1='update accounts set acn_bal=acn_bal-? where acn_acno=?'
                            query2='update accounts set acn_bal=acn_bal+? where acn_acno=?'

                            curobj.execute(query1,(uamt,uacn))
                            curobj.execute(query2,(uamt,toacn))

                            conobj.commit()
                            conobj.close()
                            messagebox.showinfo('Transfer',f"{uamt} Amount Transfered")
                            frm.destroy()
                            user_screen(uacn,None) 
                        else:
                            messagebox.showerror("Transfer","Invalid OTP")

                    otp_e=Entry(ifrm,font=('Calibri',20,'bold'),bd=5)
                    otp_e.place(relx=.4,rely=.7)
            

                    verify_btn=Button(ifrm,text="Verify",width=10,fg='black',bd=5,font=('Arial',15),command=verify_otp)
                    verify_btn.place(relx=.8,rely=.8)
                else:  
                    messagebox.showinfo("Transfer","Insufficient Balance") 


        to_lbl=Label(ifrm,text='To ACN',font=('Calibri',20,'bold'),bg='white')
        to_lbl.place(relx=.3,rely=.15)

        to_e=Entry(ifrm,font=('Calibri',20,'bold'),bd=5)
        to_e.place(relx=.4,rely=.15)
        to_e.focus()

        amt_lbl=Label(ifrm,text='Amount',font=('Calibri',20,'bold'),bg='white')
        amt_lbl.place(relx=.3,rely=.3)

        amt_e=Entry(ifrm,font=('Calibri',20,'bold'),bd=5)
        amt_e.place(relx=.4,rely=.3)

        transfer_btn=Button(ifrm,text="Transfer",width=10,fg='brown',bd=5,font=('Arial',20),command=transfer_amt)
        transfer_btn.place(relx=.6,rely=.45)
         

    logout_btn=Button(frm,text="Logout",bg='white',bd=5,font=('Arial',20,'bold'),command=logout)
    logout_btn.place(relx=.92,rely=0) 

    welcome_lbl=Label(frm,text=f'Welcome,{row[1]}',font=('Calibri',20,'bold'),bg="#00ddff",fg='black')
    welcome_lbl.place(relx=0,rely=0)

    check_btn=Button(frm,text="Check Details",width=15,fg="brown",bd=5,font=('Arial',20,),command=check)
    check_btn.place(relx=.001,rely=.15)

    update_btn=Button(frm,text="Update Details",width=15,fg='blue',bd=5,font=('Arial',20),command=update)
    update_btn.place(relx=.001,rely=.3)

    deposit_btn=Button(frm,text="Deposit",width=15,fg='green',bd=5,font=('Arial',20),command=deposit)
    deposit_btn.place(relx=.001,rely=.45)

    withdraw_btn=Button(frm,text="Withdraw",width=15,fg='red',bd=5,font=('Arial',20),command=withdraw)
    withdraw_btn.place(relx=.001,rely=.6)

    transfer_btn=Button(frm,text="Transfer",width=15,fg='purple',bd=5,font=('Arial',20),command=transfer)
    transfer_btn.place(relx=.001,rely=.75)


main_screen()
root.mainloop()