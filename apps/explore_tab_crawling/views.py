from django.shortcuts import render
from apps.explore_tab_crawling.crawler.explore_tab import InstagramCrawler
from .models import *
# Create your views here.

def save_contents():
    username = "namuna_crawl"
    password = "dbsdk309!"    

    # 인스타그램 크롤러 인스턴스 생성
    crawler = InstagramCrawler(username, password)
    
    # 로그인
    crawler.login()
    
    # 데이터 크롤링
    likes, comments, hashtags, datetimes, slide, urls = crawler.crawl_data()

    crawler.quit()

    for i in range(len(likes)):
        content = Content(
            hashtags = hashtags[i],
            likes = likes[i],
            comments = comments[i],
            slide = slide[i],
            url = urls[i],
            created_at = datetimes[i]
        )

        content.save()

def save_hashtags() :
    contents = Content.objects.all()

    for content in contents :
        hashtags = content.hashtags.split(' ')
        for hash in hashtags:
            if hash == '' :
                continue
            else :
                try :
                    hashtag = Hashtag(
                        content_id = content,
                        text = hash,
                        frequency = 1
                    )
                    hashtag.save()
                except Exception as e :
                    continue

        
