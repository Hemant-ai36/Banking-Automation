import random

def generate_captcha():
    a=str(random.randint(0,9))
    b=chr(random.randint(65,80))
    c=str(random.randint(0,9))
    d=chr(random.randint(96,112))
    e=str(random.randint(0,9))
    f=chr(random.randint(65,80))
    captcha=' '+a+' '+b+' '+c+' '+d+' '+e+' '+f' '
    return captcha