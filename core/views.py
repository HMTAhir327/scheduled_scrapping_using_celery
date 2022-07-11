from django.shortcuts import render
import requests
from bs4 import BeautifulSoup
import re
from .tasks import test_fun, send_mail_func
from .models import *
from django.core.mail import send_mail, EmailMessage
from django.conf import settings


from django_celery_beat.models import PeriodicTask, CrontabSchedule
import json

def getTime():
    USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"
    LANGUAGE = "en-US,en;q=0.5"
    session = requests.Session()
    session.headers['User-Agent'] = USER_AGENT
    session.headers['Accept-Language'] = LANGUAGE
    session.headers['Content-Language'] = LANGUAGE
    html_content = session.get(f'https://www.google.com/search?q=google+dubai+time&oq=google+dubai+time').text
    # 'for pmص''مfor am'
    soup = BeautifulSoup(html_content, 'html.parser')
    got_time = soup.find("div", attrs={"class": "BNeawe iBp4i AP7Wnd"}).text
    tiem_last_char = got_time.split()[-1]
    if tiem_last_char == 'ص':
        got_time = re.sub(r".$", "AM", got_time)
    elif tiem_last_char == 'م':
        got_time = re.sub(r".$", "PM", got_time)

    return got_time


def home(request):
    # test_fun.delay()
    send_mail_func.delay()
    users = CustomUser.objects.all()
    for user in users:
        print('user.email:',user.email)
    
    
    return render(request, 'index.html', {'time': getTime(),'View': 'Home'})


#Note without running celery command just run django project and this will automatically
# schedule the task to run at the specified time
def schedule_mail(request):
    schedule, created = CrontabSchedule.objects.get_or_create(hour = 19, minute = 57)
    task = PeriodicTask.objects.create(crontab=schedule, name="schedule_mail_task_"+"5", task='core.tasks.send_mail_func')#, args = json.dumps([[2,3]]))
    return render(request, 'index.html', {'time': getTime(),'View': 'Schedule Mail'})