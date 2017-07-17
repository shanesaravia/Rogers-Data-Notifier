# Rogers-Data-Notifier
This project was created for those who constantly go over on their phone data. This script can be setup on any interval you want, and will provide you with information on your total data, how much you have used, the date that it resets, and the average amount of data that can be used per day until your data reset date without going over.

## Getting Started
Following these instructions will get the code up and running on your local machine.

## Quick Guide
1. Download Rogers-Data-Notifier and extract zip file to where you want to store the software.
2. Navigate to https://www.twilio.com/try-twilio and sign up for an account.
3. Open rogersConfig.yml and fill out your information/configuration.
4. Run rogersData.py manually, or use Windows Task Scheduler (Windows), or Chrontab (Linux) to schedule it to run whenever you want updates. (Ex. Once a week)

## Dependencies
[Python 3](https://www.python.org/)  
[Selenium 3.0.2](http://www.seleniumhq.org/)  
[Yaml 3.12](http://www.yaml.org/start.html)  
[Twilio 6.4.2](https://www.twilio.com/docs/libraries/python)  
Beautiful Soup 4.6.0  
Time  
OS

## Setting Up Twilio
Follow these instructions to retrieve your Twilio Account SID, Twilio AuthToken, and Twilio Phone Number. (This information is needed for the config file)

1. Once you are logged in, go to your [Dashboard](https://www.twilio.com/console). You will then see your AccountSID and your AuthToken. Click the eyeball next to your AuthToken to reveal the code. Copy and paste these into your config file.
2. Then click on the [#](https://www.twilio.com/console/phone-numbers/incoming) sign on the left to retrieve your phone number. If you are not already assigned a phone number, sign up for one (This is free of charge). Copy your "Twilio Number" and paste it into the config file under the "fromNumber"

## Setting Up Windows Task Scheduler
Follow these instructions to have Windows Task Scheduler setup to run this script on any interval you want.

1. Open "Task Scheduler" which is pre installed on all windows devices. Click on "Create Task" and fill out the name of your task, and a brief description. The rest can stay the same and click the next tab (Triggers).
2. On the triggers tab you will select the interval you want the script to be run at.
3. On the next tab(Actions) you will click "New", then click "Browse", and find your rogersData.py file. Once done click OK and then click OK on the main window. Your Rogers App is now scheduled to run at the interval you selected.

## Example Config File
```
'email': 'myUsername@hotmail.com'
'password' : 'password123'
'twilio-accountSID' : 'abc123abc123abc123abc123abc123abc'
'twilio-authToken' : '111uuu111uuu111uuu111uuu111uuu111'
'fromNumber' : '4161231234'
'toNumber' : '6471231234'
```
