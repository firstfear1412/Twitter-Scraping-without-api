import time, re, os
from datetime import datetime
import pandas as pd
######## SELENIUM ########
# from selenium.webdriver import chrome
from selenium.webdriver import firefox
# from selenium.webdriver.chrome.options import Options
from selenium.webdriver.firefox.options import Options
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
######## SELENIUM ########



PATH =  "/home/lori/Visual_Code/Tweet-Scraper/chromedriver" # Note chromedriver must match with your current chrome browser's version 
URL = "https://twitter.com/"


class TwitCollect:
    
    def __init__(self):
        pass
    

    def login(self):
        # input username and password twitter
        usernameStr = ''
        passwordStr = ''

        firefox_options = Options()
        firefox_options.add_argument('--headless')
        firefox_options.add_argument('--no-sandbox')
        firefox_options.add_argument('--disable-dev-shm-usage')

        driver = webdriver.Firefox(options = firefox_options)
        driver.implicitly_wait(10)

        login_page = "i/flow/login"
        finalURL = f"{URL}{login_page}"
        time.sleep(1)
        driver.get(finalURL)

        
        xpath_sign_in = "/html/body/div/div/div/div[1]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/div[5]/label/div"
        sign_in = driver.find_element(By.XPATH,xpath_sign_in)
        sign_in.click()

        xpath_username = "//input[@autocomplete='username']"
        username = driver.find_element(By.XPATH,xpath_username)
        username.send_keys(usernameStr)
        print("put username success")
        time.sleep(3)

        xpath_next = "/html/body/div/div/div/div[1]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/div[6]/div"
        nextButton = driver.find_element(By.XPATH,xpath_next)
        nextButton.click()
        print("click next success")
        
        
        
        xpath_password = "//input[@autocomplete='current-password']"
        password = driver.find_element(By.XPATH,xpath_password)
        password.send_keys(passwordStr)
        print("put password success")
        time.sleep(5)
        
        xpath_login = "/html/body/div/div/div/div[1]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div/div[1]/div/div/div/div"
        signInButton = driver.find_element(By.XPATH,xpath_login)
        signInButton.click()
        print("log in success")
        time.sleep(5)
        return driver

    def get_tweet_data(self,card):
        """Extract data from tweet card"""
        username = card.find_element(By.XPATH,'.//span').text
        try:
            handle = card.find_element(By.XPATH,'.//span[contains(text(), "@")]').text
            
        except NoSuchElementException:
            return
        
        try:
            postdate = card.find_element(By.XPATH,'.//time').get_attribute('datetime')

        except NoSuchElementException:
            return
        
        comment = card.find_element(By.XPATH,'.//div[2]/div[2]/div[1]').text
        responding = card.find_element(By.XPATH,'.//div[2]/div[2]/div[2]')
        
        try:
            text = responding.find_element(By.XPATH,".//span").text
        except NoSuchElementException:
            text = "NULL"        

        reply_cnt = card.find_element(By.XPATH,'.//div[@data-testid="reply"]').text
        retweet_cnt = card.find_element(By.XPATH,'.//div[@data-testid="retweet"]').text
        like_cnt = card.find_element(By.XPATH,'.//div[@data-testid="like"]').text
        href = card.find_element(By.XPATH,'.//div[@data-testid="User-Name"]/div[2]/div/div[3]/a').get_attribute("href")
        
        
        
        if len(text) == 0: 
            print("Caution : Scraped tweet is empty, taking action ") 
            print("Trying to scrape again : ")
            
            responding = card.find_element(By.XPATH,'.//div[2]/div[2]/div[2]')
            try:
                text = responding.find_element(By.XPATH,".//span").text
            except NoSuchElementException:
                text = "NULL"
            
            if (len(text) == 0) : 
                print("Problem is not solved, take action ! ")
                
        
        emoji_tags = card.find_elements(By.XPATH,'.//img[contains(@src, "emoji")]')
        
        emoji_list = []
        for tag in emoji_tags:
            filename = tag.get_attribute('src')
            try:
                emoji = chr(int(re.search(r'svg\/([a-z0-9]+)\.svg', filename).group(1), base=16))
            except AttributeError:
                continue
            if emoji:
                emoji_list.append(emoji)
        emojis = ' '.join(emoji_list)
        
        tweet = (username, handle, postdate, text, emojis, reply_cnt, retweet_cnt, like_cnt, href)
        
        # DEBUG 
        print(tweet)
        
        return tweet


    def get_trends_data(self,card):
        """Extract data from tweet card"""
        username = card.find_element(By.XPATH,'.//span').text
        try:
            handle = card.find_element(By.XPATH,'.//span[contains(text(), "@")]').text
        except NoSuchElementException:
            return
        
        try:
            postdate = card.find_element(By.XPATH,'.//time').get_attribute('datetime')

        except NoSuchElementException:
            return
        
        comment = card.find_element(By.XPATH,'.//div[2]/div[2]/div[1]').text    
        responding = card.find_element(By.XPATH,'.//div[@data-testid="tweetText"]')

        # ค้นหาและดึงข้อความทั้งหมดใน span ที่อยู่ในโพสต์
        spans = responding.find_elements(By.XPATH, './/span')
        
        # สร้างตัวแปร text และรวมข้อความใน span ทั้งหมด
        text = ''
        for span in spans:
            text += span.text + '\n'

        reply_cnt = card.find_element(By.XPATH,'.//div[@data-testid="reply"]').text
        retweet_cnt = card.find_element(By.XPATH,'.//div[@data-testid="retweet"]').text
        like_cnt = card.find_element(By.XPATH,'.//div[@data-testid="like"]').text
        href = card.find_element(By.XPATH,'.//div[@data-testid="User-Name"]/div[2]/div/div[3]/a').get_attribute("href")
        
        
        
        if len(text) == 0: 
            print("Caution : Scraped tweet is empty, taking action ") 
            print("Trying to scrape again : ")
            responding = card.find_element(By.XPATH,'.//div[2]/div[2]/div[2]')
            try:
                text = responding.find_element(By.XPATH,".//span").text
            except NoSuchElementException:
                text = "NULL"
            
            if (len(text) == 0) : 
                print("Problem is not solved, take action ! ")
                
        emoji_tags = card.find_elements(By.XPATH,'.//img[contains(@src, "emoji")]')
        
        emoji_list = []
        for tag in emoji_tags:
            filename = tag.get_attribute('src')
            try:
                emoji = chr(int(re.search(r'svg\/([a-z0-9]+)\.svg', filename).group(1), base=16))
            except AttributeError:
                continue
            if emoji:
                emoji_list.append(emoji)
        emojis = ' '.join(emoji_list)
        
        tweet = (username, handle, postdate, text, emojis, reply_cnt, retweet_cnt, like_cnt, href)
        
        # DEBUG 
        print(tweet)
        
        return tweet


    def scrapeTweets(self, Twitterusername, minAmountTweet = 20, height = 700):

        firefox_options = Options()
        firefox_options.add_argument('--headless')
        firefox_options.add_argument('--no-sandbox')
        firefox_options.add_argument('--disable-dev-shm-usage')

        driver = webdriver.Firefox(options = firefox_options)
        driver.implicitly_wait(10)
        
        finalURL = f"{URL}{Twitterusername}"
        
        driver.get(finalURL)
        driver.maximize_window()
        time.sleep(1)
        
        
        print("Scraping started : ")
        print("Scraping status : ")
        print("--------------------")
        print(f"URL : {finalURL}")
        print(f"Profile : {Twitterusername}")        
        print("--------------------")
        
        data = []
        tweet_ids = set()
        
        last_position = driver.execute_script("return window.pageYOffset;")
        scrolling = True
                
        totalTweet = 0

        while scrolling:
            # page_cards = driver.find_elements_by_xpath('//article[@data-testid="tweet"]')
            page_cards = driver.find_elements(By.XPATH,'//article[@data-testid="tweet"]')
            for card in page_cards:
                tweet = self.get_tweet_data(card)
                if tweet:
                    tweet_id = ''.join(tweet)
                    if tweet_id not in tweet_ids:
                        tweet_ids.add(tweet_id)
                        data.append(tweet)  
                        
            totalTweet+=len(page_cards)
            
            # Check if data is empty --> Caution 
            if len(data) == 0 : 
                print("Caution : Unable collect data from Twitter ! ")
                print("Collected data is empty ! ")
            
            if totalTweet >= minAmountTweet:
                print("Total number of tweet collected : ", totalTweet)
                break             
        
            scroll_attempt = 0
            while True:
                # check scroll position
                
                driver.execute_script(f'window.scrollTo(0, {height});')
                height += 900
                time.sleep(2)
                curr_position = driver.execute_script("return window.pageYOffset;")
                if last_position == curr_position:
                    scroll_attempt += 1
                    
                    # end of scroll region
                    if scroll_attempt >= 3:
                        scrolling = False
                        break
                    else:
                        time.sleep(2) # attempt another scroll
                else:
                    last_position = curr_position
                    break        
        
        
        
        
        if(os.path.isfile(f"{Twitterusername}_tweets.csv")):
            td = datetime.today()
            print("Appending Dataframes ...")
            header = ['UserName', 'Handle', 'Timestamp', 'Text', 'Emojis', 'Comments', 'Retweets', 'Likes', 'href']
            df1 = pd.DataFrame(data = data , columns= header)
            df1["ScrapedDate"] = td
            df = pd.read_csv(f"{Twitterusername}_tweets.csv")
            df = pd.concat([df, df1], ignore_index=True)  # Use pd.concat to concatenate DataFrames
            df.to_csv(f"{Twitterusername}_tweets.csv", index = False)
            print(f"{Twitterusername} is scraped successfully ! Appended to related dataframe")
            
        else :      
            td = datetime.today()
            header = ['UserName', 'Handle', 'Timestamp', 'Text', 'Emojis', 'Comments', 'Retweets', 'Likes', "href"]
            df = pd.DataFrame(data = data , columns = header)   
            df["ScrapedDate"] = td
            df.to_csv(f"{Twitterusername}_tweets.csv", index = False)
            
            
        
        driver.close()
    
    def scrapeTrends(self, TrendsName, minAmountTweet = 20, height = 700):
        
        driver = self.login()
        driver.implicitly_wait(10)
        time.sleep(2)
        finalURL = f'{URL}search?q="{TrendsName}"&src=trend_click&vertical=trends'
        time.sleep(3)
        driver.get(finalURL)
        driver.maximize_window()
        time.sleep(1)
        
        
        print("Scraping started : ")
        print("Scraping status : ")
        print("--------------------")
        print(f"URL : {finalURL}")
        print(f"Trend : {TrendsName}")        
        print("--------------------")
        
        data = []
        tweet_ids = set()
        
        last_position = driver.execute_script("return window.pageYOffset;")
        scrolling = True
                
        totalTweet = 0

        while scrolling:
            page_cards = driver.find_elements(By.XPATH,'//article[@data-testid="tweet"]')
            for card in page_cards:
                tweet = self.get_trends_data(card)
                if tweet:
                    tweet_id = ''.join(tweet)
                    if tweet_id not in tweet_ids:
                        tweet_ids.add(tweet_id)
                        data.append(tweet)  
                        
            totalTweet+=len(page_cards)
            
            # Check if data is empty --> Caution 
            if len(data) == 0 : 
                print("Caution : Unable collect data from Twitter ! ")
                print("Collected data is empty ! ")
            
            if totalTweet >= minAmountTweet:
                print("Total number of tweet collected : ", totalTweet)
                break             
        
            scroll_attempt = 0
            while True:
                # check scroll position
                
                driver.execute_script(f'window.scrollTo(0, {height});')
                height += 900
                time.sleep(2)
                curr_position = driver.execute_script("return window.pageYOffset;")
                if last_position == curr_position:
                    scroll_attempt += 1
                    
                    # end of scroll region
                    if scroll_attempt >= 3:
                        scrolling = False
                        break
                    else:
                        time.sleep(2) # attempt another scroll
                else:
                    last_position = curr_position
                    break        
        
        
        
        
        if(os.path.isfile(f"{TrendsName}_tweets.csv")):
            td = datetime.today()
            print("Appending Dataframes ...")
            # header = ['UserName', 'Handle', 'Timestamp', 'Text', 'Emojis', 'Comments', 'Retweets', 'Likes']
            header = ['UserName', 'Handle', 'Timestamp', 'Text', 'Emojis', 'Comments', 'Retweets', 'Likes', 'href']
            df1 = pd.DataFrame(data = data , columns= header)
            df1["ScrapedDate"] = td
            df = pd.read_csv(f"{TrendsName}_tweets.csv")
            # df = df.append(df1)
            # df.reset_index(drop = True, inplace = True)
            df = pd.concat([df, df1], ignore_index=True)  # Use pd.concat to concatenate DataFrames
            df.to_csv(f"{TrendsName}_tweets.csv", index = False)
            print(f"{TrendsName} is scraped successfully ! Appended to related dataframe")
            
        else :      
            td = datetime.today()
            # header = ['UserName', 'Handle', 'Timestamp', 'Text', 'Emojis', 'Comments', 'Retweets', 'Likes']
            header = ['UserName', 'Handle', 'Timestamp', 'Text', 'Emojis', 'Comments', 'Retweets', 'Likes', "href"]
            df = pd.DataFrame(data = data , columns = header)   
            df["ScrapedDate"] = td
            df.to_csv(f"{TrendsName}_tweets.csv", index = False)
            
            
        
        driver.close()



###### TEST ######
if __name__ == "__main__":

    test = TwitCollect()
    # twitter_user = "FabrizioRomano"
    # trend_name = "Congratulations Lisa"
    # trend_name = "บิ๊กโจ๊ก"
    trend_name = "เอเลี่ยนบุกโลก"
    # twitter_user = "FabrizioRomano" 
    minAmountTweet = 5
    height = 700

    # login
    # test.login()
    # test.scrapeTweets(Twitterusername= twitter_user, minAmountTweet=minAmountTweet, height= height)
    test.scrapeTrends(TrendsName= trend_name, minAmountTweet=minAmountTweet, height= height)



