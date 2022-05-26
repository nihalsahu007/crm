from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.core.mail import send_mail


def create_user(sender, created, **kwargs):
    if created:
        subject = "Confirmation"
        from_mail = "abc@gmail.com"
        message = "your are successfully created account"
        send_mail(subject,message,from_mail,['nihalgopaani@gmail.com'])

post_save.connect(create_user, sender=User)