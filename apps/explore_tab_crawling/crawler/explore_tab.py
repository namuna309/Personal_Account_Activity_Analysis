import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver import Keys, ActionChains
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException


class InstagramCrawler:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.driver = self._setup_driver()

    def _setup_driver(self):
        # WebDriver 설정
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        options.add_argument('--disable-gpu')
        options.add_argument('lang=ko_KR')

        return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    def login(self):
        # 로그인 메서드
        self.driver.get("https://instagram.com")
        time.sleep(1)

        id_input = self.driver.find_element(
            By.XPATH, '//*[@id="loginForm"]/div/div[1]/div/label/input')
        ActionChains(self.driver).send_keys_to_element(
            id_input, self.username).perform()
        time.sleep(0.5)

        password_input = self.driver.find_element(
            By.XPATH, '//*[@id="loginForm"]/div/div[2]/div/label/input')
        ActionChains(self.driver).send_keys_to_element(
            password_input, self.password).perform()
        time.sleep(1)

        login_button = self.driver.find_element(
            By.XPATH, '//*[@id="loginForm"]/div/div[3]/button')
        ActionChains(self.driver).click(login_button).perform()
        time.sleep(3)

    def crawl_data(self):
        # 데이터 크롤링 메서드
        self.driver.get("https://instagram.com/explore")
        time.sleep(2)
        contents = self.driver.find_elements(By.CLASS_NAME, '_aagw')

        likes = []
        comments = []
        datetimes = []
        slide = []
        hashtags = []
        urls = []

        for content in contents[:10]:
            ActionChains(self.driver).move_to_element(content).perform()
            time.sleep(1.5)

            data = self.driver.find_elements(By.CLASS_NAME, '_abpm')
            if len(data) == 1:
                if self.driver.find_element(By.CLASS_NAME, '_abpn._9-j_'):
                    like = data[0].text
                    comment = 0
                    comments.append(comment)
                    if ',' in like:
                        like = like.replace(',', '')
                    if 'K' in like:
                        likes.append(int(float(like.replace('K', '')) * 1000))
                    elif 'M' in like:
                        likes.append(
                            int(float(like.replace('M', '')) * 1000000))
                    else:
                        likes.append(int(like))
                else:
                    like = 0
                    comment = data[0].text
                    likes.append(like)
                    if ',' in comment:
                        comment = comment.replace(',', '')
                    if 'K' in comment:
                        comments.append(
                            int(float(comment.replace('K', '')) * 1000))
                    elif 'M' in comment:
                        comments.append(
                            int(float(comment.replace('M', '')) * 1000000))
                    else:
                        comments.append(int(comment))
            elif len(data) == 0:
                likes.append(0)
                comments.append(0)
            else:
                like = data[0].text
                comment = data[1].text
                if ',' in like:
                    like = like.replace(',', '')
                if 'K' in like:
                    likes.append(int(float(like.replace('K', '')) * 1000))
                elif 'M' in like:
                    likes.append(int(float(like.replace('M', '')) * 1000000))
                else:
                    likes.append(int(like))

                if ',' in comment:
                    comment = comment.replace(',', '')
                if 'K' in comment:
                    comments.append(
                        int(float(comment.replace('K', '')) * 1000))
                elif 'M' in comment:
                    comments.append(
                        int(float(like.replace('M', '')) * 1000000))
                else:
                    comments.append(int(comment))

            ActionChains(self.driver).click(content).perform()
            time.sleep(0.5)

            urls.append(self.driver.current_url)
            try:
                self.driver.find_element(By.CLASS_NAME, '_9zm2')
            except NoSuchElementException as e:
                slide.append(False)
            else:
                slide.append(True)

            datetime_data = self.driver.find_element(By.CLASS_NAME, '_aaqe')
            datetimes.append(datetime_data.get_attribute('datetime'))
            hash_data = self.driver.find_element(By.CLASS_NAME, '_a9zs')
            hashtag_text = ''
            try:
                hashtags_data = hash_data.find_elements(By.TAG_NAME, 'a')
                for hashtag_data in hashtags_data:
                    if '@' in hashtag_data.text:
                        continue
                    hashtag_text += hashtag_data.text + ' '
            except NoSuchElementException as e:
                hashtags.append(' ')
            else:
                hashtags.append(hashtag_text[:-1])
            time.sleep(1)
            webdriver.ActionChains(self.driver).send_keys(
                Keys.ESCAPE).perform()

        print(likes)
        print(comments)
        print(hashtags)
        print(datetimes)
        print(slide)
        print(urls)

        return likes, comments, hashtags, datetimes, slide, urls

    def quit(self):
        # 브라우저 종료
        self.driver.quit()
