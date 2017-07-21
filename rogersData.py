from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import yaml
import time
import os
from twilio.rest import Client

class Configs(object):

	def config():
		os.chdir(os.path.dirname(os.path.abspath(__file__)))
		with open('rogersConfig.yml', 'r') as config:
			return yaml.load(config)

class CheckData(Configs):

	def __init__(self, email, password):
		self.email = email
		self.password = password
		self.driver = webdriver.Chrome()
		self.driver.implicitly_wait(10)
		self.driver.set_page_load_timeout(10)

	def login(self):
		"""LOGS IN TO YOUR ACCOUNT - TRIES 3 TIMES"""
		for i in range(3):
			try:
				self.driver.get('https://www.rogers.com/web/totes/#/signin')
				self.driver.find_element_by_id('USER').send_keys(self.email)
				self.driver.find_element_by_id('password').send_keys(self.password)
				self.driver.find_element_by_class_name('btn-signin').click()
				break
			except:
				print('Could not login, trying {} more times.'.format(i))

	def getAccountOverview(self):
		"""NAVIGATES TO ACCOUNT OVERVIEW"""
		self.driver.find_element_by_xpath('//*[@id="topP"]/div[4]/ute-user-if-any-granted[2]/div/ng-transclude/ute-rogers-second-level-navigation/ute-user-if-any-granted[1]/div/ng-transclude/ute-rogers-second-level-navigation-consumer/div/ute-second-level-navigation/div[1]/div/div[1]/div[1]/div[2]/md-toolbar/div/md-menu-bar/md-menu[4]/button/div/div/span').click()
		time.sleep(5)
		self.driver.find_element_by_xpath('//*[@id="menu_container_3"]/md-menu-content/md-menu-item/button/span').click()

	def getHTML(self):
		"""GETS HTML ON CURRENT PAGE"""
		html = self.driver.page_source.encode('utf-8')
		soup = BeautifulSoup(html, 'html.parser')
		return soup

	def getDataRemaining(self, soup):
		"""GET VALUE OF DATA USED"""
		time.sleep(2)
		spans = soup.find_all('span', attrs={'class':'ute-dataManager-usageDialContent-gbAmount'})
		if 'GB' in spans[0].text:
			dataRemaining = float(spans[0].text.strip(' GB'))
		elif 'MB' in spans[0].text:
			dataRemaining = float(spans[0].text.strip(' MB'))
		else:
			print('Cannot retrieve rogers data. Please try again.')
		return dataRemaining

	def getDaysLeft(self, soup):
		"""GET VALUE OF DAYS LEFT"""
		spans = soup.find_all('span', attrs={'class':'ute-dataManager-headTextSecondary-redCopy'})
		daysLeft = int(spans[0].text.strip(' days'))
		return daysLeft

	def getTotalData(self, soup):
		"""GET TOTAL DATA"""
		spans = soup.find_all('span', attrs={'class':'ute-dataManager-sharedUsageBar-indicatorCopy ute-dataManager-sharedUsageBar-indicatorCopyThird'})
		totalData = float(spans[0].text.strip('GB'))
		return totalData

	def getAverageDay(self):
		"""GET AVERAGE PER DAY (REMAINING DAYS)"""
		dataRemaining = self.getDataRemaining(self.getHTML())
		daysLeft = self.getDaysLeft(self.getHTML())

		if dataRemaining <= 20:
			return str(round(dataRemaining / daysLeft, 1)) + ' GB'
		else:
			return str(round(dataRemaining / daysLeft, 1)) + ' MB'

# SEND A TEXT WITH DATA REMAINING
class SendSMS(CheckData):

	def __init__(self, accountSID, authToken):
		self.accountSID = accountSID
		self.authToken = authToken


	def sendMessage(self, sender, receiver, message):
		twilioCli = Client(self.accountSID, self.authToken)
		message = twilioCli.messages.create(body=message, from_=sender, to=receiver)

class Main(SendSMS):

	def run():
		config = Configs.config()
		dataChecker = CheckData(config['email'], config['password'])
		dataChecker.login()
		dataChecker.getAccountOverview()
		html = dataChecker.getHTML()
		dataRemaining = dataChecker.getDataRemaining(html)
		sendSMS = SendSMS(config['twilio-accountSID'], config['twilio-authToken'])
		sendSMS.sendMessage(config['fromNumber'], config['toNumber'], 'You have {} GB left out of {} GB. You have {} days left until it resets. This leaves you {} per day.'.format(dataChecker.getDataRemaining(html), dataChecker.getTotalData(html), dataChecker.getDaysLeft(html), dataChecker.getAverageDay()))

Main.run()
