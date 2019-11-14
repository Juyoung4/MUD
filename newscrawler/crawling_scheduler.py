# 스케줄 종류에는 여러가지가 있는데 대표적으로 BlockingScheduler, BackgroundScheduler 이다.
#  BlockingScheduler 는 단일수행에, BackgroundScheduler은 다수 수행에 사용된다.
from apscheduler.schedulers.background import  BackgroundScheduler
from apscheduler.jobstores.base import JobLookupError
import time
from newscrawler import news_crawler

def job():
    print("I'm working...", "| [time] " , str(time.localtime().tm_hour) + ":" + str(time.localtime().tm_min) + ":" + str(time.localtime().tm_sec))
def job_2():
    print("Job2 실행: ", "| [time] " ,str(time.localtime().tm_hour) + ":" +str(time.localtime().tm_min) + ":" +str(time.localtime().tm_sec))

# Backgroundscheduler를 사용하면 stat를 먼저하고 add_job을 이용해 수행할 것을 등록하낟
sched = BackgroundScheduler()
sched.start()

#interval - 매 3초마다 실행
sched.add_job(job,'interval',seconds=3,id='test_2')

#cron 사용 - 매 5초마다 job 실행
sched.add_job(job,'cron',second='*/5',id='test_1')

#cron으로 하는 경우 다르게 시간을 주어질수도 있다[아래와 같은 경우 10분10초간 실행싷킨다]
sched.add_job(job_2,'cron',minute="10",second='10',id="test_10")

while True:
    print("running!!")
    time.sleep(1)