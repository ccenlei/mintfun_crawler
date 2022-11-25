#!/usr/bin/python3

import smtplib

from email.mime.text import MIMEText
from email.utils import formataddr

from utils import database_utils


# 提醒邮件服务
class MailSender:
    def __init__(self, mail_pas: str):
        self.__mail_pass = mail_pas
        # smtp服务相关配置
        self.__mail_host = 'smtp.163.com'
        self.__mail_usr = 'cenuoile'
        self.__sender = 'cenuoile@163.com'

    def mail(self, title, message):
        users = database_utils.user_select_all()
        # step1. 登陆账户
        server = smtplib.SMTP_SSL(host=self.__mail_host, port=465)
        server.login(self.__mail_usr, self.__mail_pass)
        for user in users:
            # step2. 创建邮件
            msg = MIMEText(message, 'plain', 'UTF-8')
            msg['From'] = formataddr(('mint fun', self.__sender))
            msg['To'] = formataddr((user['name'], user['host']))
            msg['Subject'] = title
            # step3. 发送邮件
            server.sendmail(self.__sender, user['host'], msg.as_string())
        print("邮件已发送...")
        server.quit()
