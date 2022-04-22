import smtplib
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
import emailParams


msg=MIMEMultipart()

msg['SUBJECT']=emailParams.EMAIL_SUBJECT
msg['From']=emailParams.SEND_FROM
if type(emailParams.SEND_TO)==list:
    msg['To']=','.join(emailParams.SEND_TO)
else:
    msg['To']=emailParams.SEND_TO
#password=emailParams.PASSWORD



def sendEmail(html):
    try:
        server=smtplib.SMTP(emailParams.HOST,emailParams.PORT)
        server.ehlo()
        server.starttls()
        #server.login(msg['From'], password)
    except Exception as err:
        print('There is an error ',err)
    else:
        for i,htm_iter in enumerate(html):
            if i==0:
                htm=htm_iter+'<br>'
            else:
                htm+=htm_iter
        '''for i,htm_iter in enumerate(systab):
            htm+=htm_iter'''
        attachment=MIMEText(htm,'html')
        msg.attach(attachment)

        server.sendmail(msg['From'],emailParams.SEND_TO,msg.as_string())
