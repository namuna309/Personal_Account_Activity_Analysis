from apscheduler.schedulers.background import BackgroundScheduler
from apps.explore_tab_crawling.views import *
from datetime import datetime


def job():
    now = datetime.now()
    print(now.strftime('%Y-%m-%d %H:%M:%S'), " start instagram crawling")

    try:
        save_contents()
        save_hashtags()
        print(now.strftime('%Y-%m-%d %H:%M:%S'),
              " instagram crawling completed")
    except Exception as e:
        print(e)
        print(now.strftime('%Y-%m-%d %H:%M:%S'), " instagram crawling failed")


def schedule_job():
    sched = BackgroundScheduler()

    sched.add_job(job, 'interval', hours=1, jitter=0.15)
    sched.start()
