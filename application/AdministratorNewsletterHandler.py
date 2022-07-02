# -*- coding= utf-8 -*-
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage


class AdministratorNewsletter:
    """Отправка email-рассылки зарегистрированным пользователям сайта."""
    def __init__(self, title, text):
        self.addr_from = "None" #email админа
        self.password = "None" #пароль админа
        self.title = title
        self.text = text
        
    def define_newsletter_message(self):
        """Оболочка сообщения."""
        self.message = MIMEMultipart()
        self.message["From"] = self.addr_from
        self.message["Subject"] = self.title
        self.message.attach(MIMEText(self.text, 'plain'))
        try:
            self.server = smtplib.SMTP_SSL("smtp.yandex.ru", 465)
        except Exception:
            print("Error")
            return None
        self.server.set_debuglevel(0)
        self.server.login(self.addr_from, self.password)
        
    def send_newsletter_message(self, contact_list:list):
        """Отправка сообщения через протокол smtp."""
        for email_address in contact_list:
            self.message["To"] = email_address
            self.server.send_message(self.message)
        self.server.quit()
        
    