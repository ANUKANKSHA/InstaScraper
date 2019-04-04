from bs4 import BeautifulSoup
from selenium import webdriver
from time import sleep
import os
import requests
import shutil


class App():
    def __init__(self, username='sarahsan0', password='ilovemumma',
                target_username='bhumikasingh__', path='C:/Users/DELL/Desktop/scrape_insta_shivya'):

        self.username = username
        self.password = password
        self.path = path
        self.target_username = target_username
        self.driver = webdriver.Chrome('C:/Users/DELL/Downloads/chromedriver_win32/chromedriver.exe')
        self.main_url = 'https://www.instagram.com'
        self.driver.get(self.main_url)
        self.error = False
        self.all_images = []
        self.log_in()
        if self.error is False:
            self.close_notify_box()
            self.search_target()
        if self.error is False:
            self.scroll_down()
        if self.error is False:
            if not os.path.exists(path):
                os.mkdir(path)
            self.downloading_images()

        input('Stop for now')
        sleep(3)
        self.driver.close()

    def downloading_images(self):

        print(len(self.all_images))



        for index,image in enumerate(self.all_images):
            filename = "image_" + str(index) + ".jpg"
            image_path = os.path.join(self.path,filename)
            link = image['src']
            print("Downloading image ", index)

            response = requests.get(link,stream = True)
            try:
                with open(image_path,'wb') as file:
                    shutil.copyfileobj(response.raw,file)
            except Exception as e:
                print(e)
                print('Could not download image no.', index)
                print('Image link',link)






    def scroll_down(self):
        sleep(3)
        try:
            num_posts = self.driver.find_element_by_xpath('//span[text()[contains(.," posts")]]/span[@class="g47SY "]')
            str_num_posts = str(num_posts.text).replace(',','')
            self.int_num_posts = int(str_num_posts)

            if self.int_num_posts > 12:
                num_scrolls = int(self.int_num_posts/12) + 1
                last = self.int_num_posts % 12

            else:
                num_scrolls = self.int_num_posts
                last = 0

            print(num_scrolls)
            sleep(3)
            try:
                soup = BeautifulSoup(self.driver.page_source,'html.parser')
                images = soup.findAll('img')

                self.all_images = images
                last_height = self.driver.execute_script("return document.body.scrollHeight")
                for win in range(num_scrolls):
                    print(win)
                    self.driver.execute_script('window.scrollTo(0,document.body.scrollHeight);')
                    sleep(3)
                    new_height = self.driver.execute_script("return document.body.scrollHeight")
                    if new_height == last_height:
                        break
                    soup = BeautifulSoup(self.driver.page_source,'html.parser')
                    images = soup.findAll('img')
                    self.all_images.extend(images[-12:])
                    last_height = new_height

                if last > 0:
                    images = self.all_images[:(len(self.all_images)-12)]
                    print("a")
                    last_images = self.all_images[-last:]
                    print("a")
                    self.all_images = images
                    print("a")
                    self.all_images.extend(last_images)
                    print("a")


                print(len(self.all_images))
            except Exception as e:
                self.error = True
                print(e)
        except Exception as e:
            self.error = True
            print(e)



    def search_target(self):
        try:
            search_bar = self.driver.find_element_by_xpath('//input[@class="XTCLo x3qfX "]')
            search_bar.send_keys(self.target_username)
            taget_profile_url = self.main_url + '/' + self.target_username + '/'
            self.driver.get(taget_profile_url)
        except Exception as e:
            self.error = True
            print(e)


    def close_notify_box(self):
        try:
            sleep(3)
            not_now_button = self.driver.find_element_by_xpath('//button[@class="aOOlW   HoLwm "]')
            not_now_button.click()
        except Exception:
            pass


    def log_in(self):
        try:
            log_in_button = self.driver.find_element_by_xpath('//p[@class="izU2O"]/a')
            log_in_button.click()
            sleep(3)
            user_name_input = self.driver.find_element_by_xpath('//input[@aria-label="Phone number, username, or email"]')
            user_name_input.send_keys(self.username)
            password_input = self.driver.find_element_by_xpath('//input[@aria-label="Password"]')
            password_input.send_keys(self.password)
            password_input.submit()
        except Exception as e:
            self.error = True
            print(e)


if __name__ == '__main__':
    app = App()
