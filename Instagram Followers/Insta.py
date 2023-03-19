from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
import csv


FollowersCount=2000

try:
	chrome_options = Options()
	chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:8000")
	#Change chrome driver path accordingly
	s=Service(ChromeDriverManager().install())
	driver = webdriver.Chrome(service=s,options=chrome_options)

	with open(f"Followers.csv","w", newline='' , encoding='UTF8') as A:
		header = ["User Name","Profile URL"]
		writer = csv.writer(A)
		writer.writerow(header)
		
		with open("InstagramProfiles.txt","r") as R:
			for i in R.readlines():
				FList=[]
				driver.get(i.replace("\n",""))
				wait = WebDriverWait(driver, 10)
				element = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[contains(text(),' followers')]")))

				FollowersButton=driver.find_element(By.XPATH,"//*[contains(text(),' followers')]")
				driver.execute_script("arguments[0].click();",FollowersButton)

				while True:
					# driver.execute_script("arguments[0].scrollTo(0, document.body.scrollHeight);",driver.find_element(By.CSS_SELECTOR,"div[aria-label='Following']"))
					time.sleep(2)
					following = driver.find_element(By.CSS_SELECTOR,"div[aria-label='Followers']").find_elements(By.CSS_SELECTOR,"ul>div>li")
					print(len(following))
					FList.append(len(following))
					if FList.count(len(following))>=25:
						break

					try:
						driver.execute_script("arguments[0].scrollIntoView();", following[-1])
					except:
						pass
					if (len(following))>=FollowersCount:
						break
				following = driver.find_element(By.CSS_SELECTOR,"div[aria-label='Followers']").find_elements(By.CSS_SELECTOR,"ul>div>li")
				for follow in following:
					try:
						FURL=follow.find_element(By.TAG_NAME,'a').get_attribute('href')
					except:
						FURL=""
					try:	
						UName=FURL.split("/")[-2]
					except:
						UName=""
					if FURL!="":
						writer.writerow([UName,FURL])
except Exception as E:
	print("Error!!!")
	# print(E)
else:
	print("Done O_o")
