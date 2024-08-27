# Import OS module to access environmental variables
import os

# Import sleep module
from time import sleep

# Import Selenium libraries
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService

# Import webdriver manager for Chrome
from webdriver_manager.chrome import ChromeDriverManager

# Import Pandas
import pandas as pd

options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)

browser = webdriver.Chrome(options=options, service=ChromeService(ChromeDriverManager().install()))

# Load the webpage in the browser
browser.get("https://www.goodreads.com/user/sign_in")

# Navigate to the email sign-in option
login_with_email_button = browser.find_element(By.CSS_SELECTOR, value=".authPortalConnectButton.authPortalSignInButton")
login_with_email_button.click()
sleep(2)

# Retrieve username & password from env variables
user_email = os.getenv('USER_EMAIL')
user_password = os.getenv('USER_PWD')

# Log in using username & password
log_email = browser.find_element(By.ID, value = "ap_email")
log_pwd = browser.find_element(By.ID, value = "ap_password")
log_email.send_keys(user_email)
log_pwd.send_keys(user_password)
log_pwd.submit()

# Search for book title
browser.get("https://www.goodreads.com/search?q=&qid=")
search_book = browser.find_element(By.CSS_SELECTOR, ".searchBox__input.searchBox__input--navbar")
search_book.send_keys("1984")
search_book.send_keys(Keys.RETURN) # Keys.RETURN simulates pressing Enter key

# Loop through the book searched
item_list = browser.find_elements(By.XPATH, value = "//table/tbody/tr[contains(@itemtype, 'http://schema.org/Book')]")
img = browser.find_elements(By.CLASS_NAME, value = "bookCover")
book_list = list()
for i in range(len(item_list)):
    book_list.append(item_list[i].text.split("\n"))
   
book_list_ap = list()

for i in range(0, len(book_list)):
    # book_list_ap[i] = {
    #     "title":book_list[i][0],
    #     "author":book_list[i][1],
    #     "rating":book_list[i][2],
    #     "cover_img":img[i].get_property("src")
    # }
    book_list_ap.append((book_list[i][0], book_list[i][1], book_list[i][2], img[i].get_property("src")))

# Create data frame with Pandas
df = pd.DataFrame(data=book_list_ap, columns=["title", "author", "rating", "cover_img"])
print(df)
df.to_csv("goodreads_data.csv")
