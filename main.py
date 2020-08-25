from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

import os

logInFacebook = False

LOGINFB_XPath = '/html/body/div[1]/section/main/article/div[2]/div[1]/div/form/div/div[5]/button/span[2]'
FBEMAILFORM_XPath = '/html/body/div[1]/div[3]/div[1]/div/div/div[2]/div[1]/form/div/div[1]/input'
FBPASSWORDFORM_XPath = '/html/body/div[1]/div[3]/div[1]/div/div/div[2]/div[1]/form/div/div[2]/input'
FBLOGINBUTTON_XPath = '/html/body/div[1]/div[3]/div[1]/div/div/div[2]/div[1]/form/div/div[3]/button'

EMAIL_XPath = '/html/body/div[1]/section/main/article/div[2]/div[1]/div/form/div/div[1]/div/label/input'
PASSWORD_XPath = '/html/body/div[1]/section/main/article/div[2]/div[1]/div/form/div/div[2]/div/label/input'
LOGINBUTTON_XPath = '/html/body/div[1]/section/main/article/div[2]/div[1]/div/form/div/div[3]/button'
REJECTLOGININFO_XPath = '/html/body/div[1]/section/main/div/div/div/div/button'

NOTNOW_XPath = '/html/body/div[4]/div/div/div/div[3]/button[2]'
USERSEARCHBOX_XPath = '/html/body/div[1]/section/nav/div[2]/div/div/div[2]/input'
PICKFIRSTUSER_XPath = '/html/body/div[1]/section/nav/div[2]/div/div/div[2]/div[3]/div[2]/div/a[1]/div'
INSTAGRID_XPath = '/html/body/div[1]/section/main/div/div[3]/article/div'
IMAGEPOP_XPath = '/html/body/div[4]/div[3]/button/div'

INSTAIMG_XPath = '//*[@id="react-root"]/section/main/div/div[contains(@class," _2z6nI")]/article/div/div/div[{}]/div[{}]'
POSTNUMBER_XPath = '//*[@id="react-root"]/section/main/div/header/section/ul/li[1]/span/span'
LIKE_XPath = '/html/body/div[4]/div[2]/div/article/div[3]/section[1]/span[1]/button'

print('\nInstagram profile Bomber\n')
print('Please make sure the chrome window is maximise at all time.')
while(True):
    logInFacebooks = input("Login using Facebook?(y/n): ")
    if  logInFacebooks.lower()=='y'::
        logInFacebook = True
        break
    elif  logInFacebooks.lower()=='n'::
        logInFacebook = False
        break
    else:
        print('Input not clear. Please try again.')   
email = input("Please enter your Instagram email: ")
password = input("Please enter the Instagram password: ")
igusername = input("Please enter the the profile's username: ")
succeedLogin = False

#need to have this func to export to .exe
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.dirname(__file__)
    return os.path.join(base_path, relative_path)

driver = webdriver.Chrome(resource_path('./drivers/chromedriver.exe'))
driver.maximize_window()
driver.get('https://www.instagram.com')

if logInFacebook:
    try:
        print('-Logging in with Facebook')
        #click login with fb button
        element = WebDriverWait(driver,10).until(
        EC.presence_of_element_located((By.XPATH,LOGINFB_XPath))
        )
        element.click()
        #fill in fb email
        element = WebDriverWait(driver,10).until(
        EC.presence_of_element_located((By.XPATH,FBEMAILFORM_XPath))
        )
        element.send_keys(email)
        #fill in fb password
        element = driver.find_element_by_xpath(FBPASSWORDFORM_XPath)
        element.send_keys(password)
        #click login 
        element = driver.find_element_by_xpath(FBLOGINBUTTON_XPath)
        element.click()
        #click not now
        element = WebDriverWait(driver,10).until(
            EC.presence_of_element_located((By.XPATH,NOTNOW_XPath))
        )
        element.click()
        succeedLogin = True
        print('-Succeed login with Facebook.')
    except:
        print('-Failed login with Facebook.')
else:
    try:
        print('-Loggin in with email and password')
        #fill in email
        element = WebDriverWait(driver,10).until(
        EC.presence_of_element_located((By.XPATH,EMAIL_XPath))
        )
        element.send_keys(email)
        #fill in password
        element = driver.find_element_by_xpath(PASSWORD_XPath)
        element.send_keys(password)
        #click login
        element = driver.find_element_by_xpath(LOGINBUTTON_XPath)
        element.click()
        #reject save login info
        element = WebDriverWait(driver,10).until(
        EC.presence_of_element_located((By.XPATH,REJECTLOGININFO_XPath))
        )
        element.click()
        succeedLogin = True
        print('-Succeed login with email and password.')   
        #click not now
        element = WebDriverWait(driver,10).until(
            EC.presence_of_element_located((By.XPATH,NOTNOW_XPath))
        )
        element.click()
    except:
        print('-Failed login with email and password.')   

if succeedLogin:
    try:       
        #type in username in search box
        element = WebDriverWait(driver,10).until(
            EC.presence_of_element_located((By.XPATH,USERSEARCHBOX_XPath))
        )
        element.send_keys(igusername)
        #pick first name from list
        element = WebDriverWait(driver,10).until(
            EC.presence_of_element_located((By.XPATH,PICKFIRSTUSER_XPath))
        )
        element.click()
        #wait for profile load
        element = WebDriverWait(driver,10).until(
            EC.presence_of_element_located((By.XPATH,INSTAGRID_XPath))
        )
        #get post number
        element = driver.find_element_by_xpath(POSTNUMBER_XPath)
        postNumber = int(element.text)
        print('The profile contains {} posts'.format(postNumber))
        totalRow = postNumber/3 + (postNumber%3 > 0)
        isBreaked = False
        column = 0
        row = 0
        #like posts process
        for row in range(1,int(totalRow)+1):
            if isBreaked:
                break
            for column in range(1,4):
                image = WebDriverWait(driver,10).until(
                    EC.presence_of_element_located((By.XPATH,INSTAIMG_XPath.format(row ,column)))
                )
                # image.location_once_scrolled_into_view
                image.click()
                print('Post {}'.format((row-1)*3 + column),end = '')
                try:
                    likeButton = WebDriverWait(driver,10).until(
                        EC.presence_of_element_located((By.XPATH,LIKE_XPath))
                    )
                    liked = str(likeButton.find_element_by_css_selector('svg').get_attribute("aria-label"))
                    if liked=='Like':
                        likeButton.click()
                        print(' - Pressed Like')
                    else:
                        print()
                except:
                    print(' - Problem liking')   
                finally:     
                    popout = driver.find_element_by_xpath(IMAGEPOP_XPath)
                    popout.click()
                    if (row-1)*3+column == postNumber:
                        isBreaked = True
                        break   
        print('-Done bombing!')            
    except:
        print()
        print('The program counter an error, please try again.')
    finally: 
        driver.quit()
else:
    driver.quit()
    print()
    print('Please try again by running the script again.')  

