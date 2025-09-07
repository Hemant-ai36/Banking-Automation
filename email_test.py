import gmail
# replace with your email_id  & app_pass 
email_id='tripathihemant36@gmail.com'
app_pass='???????????'

def send_openacn_ack(uemail,uname,uacn,upass):
    con=gmail.GMail(email_id,app_pass)
    sub="Congratulations😊,Account opened successfully"
    utext=f"""Hello,{uname}
Welcome to Kotak Bank
Your AC No is {uacn}
Your Password is {upass}
Kindly change your password when you login first time

Thanks
Kotak Bank
New Delhi
"""
    msg=gmail.Message(to=uemail,subject=sub,text=utext)
    con.send(msg)



def send_otp(uemail,otp,amt):
    con=gmail.GMail(email_id,app_pass)
    sub="OTP fro fund transfer"
    utext=f"""Your OTP is {otp} to tarnsfer amount {amt}
    
Kindly use this OTP to complete transaction
Please don't share to anyone else 

Thanks
Kotak Bank
New Delhi
"""
    msg=gmail.Message(to=uemail,subject=sub,text=utext)
    con.send(msg)


def send_otp_for_pass(uemail,otp):
    con=gmail.GMail(email_id,app_pass)
    sub="OTP fro password recovery"
    utext=f"""Your OTP is {otp} to recover password
Please don't share to anyone else 

Thanks
Kotak Bank
New Delhi
"""
    msg=gmail.Message(to=uemail,subject=sub,text=utext)
    con.send(msg)
