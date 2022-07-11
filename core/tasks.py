from __future__ import absolute_import, unicode_literals
from email import message
from django.contrib.auth import get_user_model
from .models import *

from celery import shared_task
from django.core.mail import send_mail, EmailMessage
from django.conf import settings
from .views import getTime



#NOTE: this is a celery task AND HAVE TO RUN WORKER ON EVERY CHANGE IN THIS FILE
#celery worker is compulsory to run celery beat,celery results,celery worker
#Note: while run celery beat, celery worker will also have to be run on the same machine 


@shared_task
def send_mail_func():
    #operations
    # users = get_user_model().objects.all()

    print('send_mail_func called')
    getTime() #this recalled on specified period of time
    users = CustomUser.objects.all()
    for user in users:
        subject = 'Celery Testing mail'
        message = 'This is a test mail'
        print('user.email:>>>',user.email)
        to_email = user.email
        email = EmailMessage(
            subject, message, settings.EMAIL_HOST_USER, [to_email])
        email.content_subtype = 'html'
        email.send(fail_silently=True)

        # send_mail(
        #     subject = subject,
        #     message=message,
        #     from_email=settings.EMAIL_HOST_USER,
        #     recipient_list=[to_email],
        #     fail_silently=True,
        # )
    # for i in range(10):
    #     print(i)
    return 'Mail Done'

@shared_task
def test_fun():
    #operations
    for i in range(10):
        print(i)
    return 'Done'





