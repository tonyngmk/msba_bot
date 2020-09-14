# MSBA Telegram Bot
Search `@MSBA_NTU_Bot` in Telegram. 

Created for Chatbot Assignment in BC3409 - AI in Accounting and Finance AY2020/21 Sem 1.

This project primary shows how we can create or customizable telegram bot using Python.

Also, this also shows how one is able to seamlessly integrate **Telegram** with **Google Sheets** through the use of Python.

## Diagram

<p align="center">
	insert diagram here
</p>

### 1. Google Cloud Platform (GCP)

#### 1.1 Google Drive API

Steps to obtain credentials for Google Drive API:
1. Google Drive API > Enable > Create Credentials 
2. Select Google Drive API > Web Server > Application Data > No I'm not using them
3. Any name > Editor > JSON
4. Download JSON credentials > Copy client_email > Share to this email in Google Sheets

### 1.2 Google Sheets API

Integrating Drive with Sheets
- Google Sheets API > Enable

### 1.3 Google APIs & Service

1. Ensure you have a project created and Google Drive API enabled.
2. APIs & Service > Credentials > Create Credentials > Create OAuth client ID
3. Application Type: Web application
4. Authorized JavaScript Origins URLs: http://localhost:8080
5. Authorized redirect URls: http://localhost:8080/
6. Download client secrets and rename as client_secrets.json and move to cwd

### 2. Python 

python-telegram-bot is used to talk from python-telegram, gspread is used to talk from python-(google spreadsheet)

#### 2.1 Python-Google Spreadsheet

	python3 -m pip install --user gspread oauth2client

References: https://gspread.readthedocs.io/en/latest/

In essence, the bot is able to query and insert rows to gsheets directly.

###### Get Methods:
- get_all_records()
- row_values(row)
- col_values(col)
- cell(row, col).value

###### Insert Methods:
- insert_row(array, rowNo)
- delete_row(rowNo)
- update_cell(rowNo, colNo, value)

###### Sheet integrated in bot:
- Mailing List
- Pre-Assessment

#### 2.2 Google

Google-API is a library in Python that can be used to talk to Google Drive.

	python3 -m pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib



#### 2.3 Python-Telegram

	python3 -m pip install --user python-telegram-bot

Thereafter, just edit along **bot.py** file and execute it. The python script must continually run for the bot to work. 
To do so, one can run it perpetually using a cloud virtual machine, e.g. AWS EC2, Google Compute Engine, etc. 

I've tried running on free tier t2 micro and the CPU Credit Usage for 2 bots is negligible, so it should be essentially free.

<p align="center">
  <img src="https://raw.githubusercontent.com/tonyngmk/my-stoic-telebot/master/cpu_cred_usage.png" />
</p>


##### Dump of codes to get it hosted on AWS EC2 Linux2 AMI:

	sudo yum update -y 

	sudo amazon-linux-extras install python3.8

	alias python3='/usr/bin/python3.8'

	python3 --version

	sudo yum install git -y

	sudo yum -y install python3-pip

	git clone https://github.com/tonyngmk/msba_bot.git

	cd telegram-ntudb-bot

	chmod 755 ./bot.py

	python3 -m pip install --user python-telegram-bot

	python3 -m pip install --user gspread oauth2client
	
	python3 -m pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib

	python3 -m pip install --user pandas

	screen

	ctrl + a + c (create new screen)

	ctrl + a + n (switch screens)

	python3 bot.py

### Note

This git repo does not have certain files containing credentials excluded in .gitignore. In case you are reusing the script, store:
- Telegram bot's API as **botapi.txt**
- Google Drive API as **creds.json**
