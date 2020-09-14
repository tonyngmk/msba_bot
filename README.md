<h1 align=center><div>
<img src="https://raw.githubusercontent.com/tonyngmk/free_storage/master/Images/NTU%20Logo.png " width="500" height="175" align="middle">
</div>

<h1 align=center><font color='Blue'>BC3409</font> - 
<font color='red'>AI in Accounting & Finance</font>

<font size = 5>Semester 1, AY2020-21</font>

<br></br>
<font size = 5>Chatbot Assignment</font>


# MSBA Telegram Bot
Search `@MSBA_NTU_Bot` in Telegram. 

<p align="center">
  <img src="https://raw.githubusercontent.com/tonyngmk/msba_bot/master/msbaBot.png" />
</p>

**Highlights in Project:**
- Using a full programming language (Python) as backend for Telegram chatbot
- Seamlessly adding fields of data as rows to Google Sheets
- Capable of uploading user's attachment to Google Drive
- Able to send images and text to replicate a full website
- Send documents by users' command as well

Created for Chatbot Assignment in BC3409 - AI in Accounting and Finance AY2020/21 Sem 1.

## Commands
1. **/start** - Start conversation
2. **/join** - Join mailing list
3. **/upload** - Upload CV for pre-assessment
4. **/help** - See all commands

## Diagram

<p align="center">
	insert diagram here
</p>


## Replication instructions

### 1. Google Cloud Platform (GCP)

GCP console free-tier provides more than adequate resources for this project. It is required for both Google Drive and Google Sheets services.

### 1.1 Google Drive API

Steps to obtain credentials for Google Drive API:
1. Google Drive API > Enable > Create Credentials 
2. Select Google Drive API > Web Server > Application Data > No I'm not using them
3. Any name > Editor > JSON
4. Download JSON credentials > Copy client_email > Share to this email in Google Sheets
5. Rename JSON credentials to creds.json and move it to current working directory (cwd).

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

This project is using Python programming language. 

Perks of using a programming language instead of 3rd-party platforms such as SnatchBot is that one can be self-reliant, and harness the full capability of utilizing a full-programming language for backend logic.

#### 2.1 Python-Google Spreadsheet

In essence, the bot will be able to query and insert rows to gsheets directly.

	python3 -m pip install --user gspread oauth2client

References: https://gspread.readthedocs.io/en/latest/

To make sure to distinguish *'file-level'* and *'sheet-level'* when updating.

<p align="center">
  <img src="https://raw.githubusercontent.com/tonyngmk/msba_bot/master/sheetsDemonstration.png" />
</p>

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

#### 2.2 Google-API

Google-API is a library in Python that can be used to talk to Google services, and this is used to interact with Google Drive.

	python3 -m pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib

<p align="center">
  <img src="https://raw.githubusercontent.com/tonyngmk/msba_bot/master/driveDemonstration.png" />
</p>

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
- Google OAuth2 API as **client_secrets.json**
