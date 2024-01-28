from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep

class InstaBot():
    def __init__(self, username, pw):
        self.driver = webdriver.Chrome()
        self.username = username
        self.driver.get('https://instagram.com')
        sleep(2)
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys(pw)
        self.driver.find_element(By.XPATH, '//button[@type="submit"]').click()
        sleep(3)
        

    def get_unfollowers(self):
        self.driver.find_element(By.XPATH, "//a[contains(@herf, '/{}')]".format(self.username)).click()
        sleep(2)
        #load all account which you follow
        self.driver.find_element(By.XPATH, "//a[contains(@herf,'/following')]").click()
        following = self._get_names()
        #load all account which follow you
        self.driver.find_element(By.XPATH, "//a[contains(@herf,'/followers')]").click()
        followers = self._get_names()
        not_follow_back = [user for user in following if user not in followers]
        print(not_follow_back)
        

    def _get_names(self):
        sleep(2)
        sugs = self.driver.find_element(By.XPATH, '//h4[contains(text(), Suggestions)]')
        self.driver.execute_script('arguments[0].scrollIntoView()', sugs)
        sleep(2)
        scroll_box = self.driver.find_element(By.XPATH, "/html/body/div[3]/div/div[2]")
        last_ht, ht = 0, 1
        while last_ht != ht:
            last_ht = ht
            sleep(1)
            ht = self.driver.execute_script("""
                arguments[0].scrollTo(0, arguments[0].scrollHeight); 
                return arguments[0].scrollHeight;
                """, scroll_box)
        links = scroll_box.find_elements_by_tag_name('a')
        names = [name.text for name in links if name.text != '']
        # close button
        self.driver.find_element(By.XPATH, "/html/body/div[3]/div/div[1]/div/div[2]/button").click()
        return names



mybot = InstaBot('<username>', '<pw>')
mybot.get_unfollowers()