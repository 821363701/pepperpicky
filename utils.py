__author__ = 'yu'

import smtplib
from email.mime.text import MIMEText


def send_mail(text):
    msg = MIMEText(text)
    msg['Subject'] = text

    msg['From'] = '821363701@qq.com'
    msg['To'] = '821363701@qq.com'

    s = smtplib.SMTP_SSL('smtp.qq.com')
    s.login('821363701@qq.com', '821363701pepper')
    s.sendmail('821363701@qq.com', ['821363701@qq.com'], msg.as_string())
    s.quit()


def send_mail_ex(title, text):
    msg = MIMEText('<html><p>Test your WatchOS 2 apps and App Thinning on iOS............</p><p>'+title+'</p><a href="'+text+'">jump to</a></html>', 'html', 'utf-8')
    msg['Subject'] = 'Apple Developer'

    msg['From'] = '821363701@qq.com'
    msg['To'] = '821363701@qq.com'

    s = smtplib.SMTP_SSL('smtp.qq.com')
    s.login('821363701@qq.com', '821363701pepper')
    s.sendmail('821363701@qq.com', ['821363701@qq.com'], msg.as_string())
    s.quit()