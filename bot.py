#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler
from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
import logging
import json
from datetime import datetime, timedelta
import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pprint import pprint
import pandas as pd
import re

scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)
client = gspread.authorize(creds)
sheet = client.open("msbaMailingList") # file-level
mailSheet = sheet.worksheet("mailingList") # sheet-level
mailSheet = pd.DataFrame(mailSheet.get_all_records())

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)
logger = logging.getLogger(__name__)

# newUser2, CONT, DATE, TIME, OVER_1830H, OVER_1830H_2, GETATT1 = range(7) # states
# reason_cache, userInputName, gmail, day_cache, date_cache, time_cache = range(6) # variables

CONT, LEARNMORE2, LEARNMORECATCH, PROGOVERVIEW2 = range(4)

def start(update, context):
    user = update.message.from_user
    logger.info("User {} has started to use MSBA bot".format(user.first_name, update.message.text))
    context.bot.send_message(chat_id=update.effective_chat.id, text="👋👋 Hey there! Welcome to the MSc in Business Analytics (MSBA) Bot 🤖🤖🤖")
    context.bot.send_message(chat_id=update.effective_chat.id, text="🎓🎓🎓 **MSBA** is the Programme to take you into the World of **Data Analytics** 🎓🎓🎓", parse_mode=telegram.ParseMode.MARKDOWN)
    context.bot.send_message(chat_id=update.effective_chat.id, text='''
    Serving as a bridge between the business and technology functions, business analysts play a critical role in guiding businesses through today’s environment of digital disruption, analysing and utilising data to drive digital transformation, redefine the customer experience and deliver profitable outcomes.

The MSc in Business Analytics (MSBA) programme offers a unique curriculum shaped through engagement with leading industry partners to reflect real industry needs. Cutting-edge modules such as Analytics and Machine Learning in Business provide an understanding of technologies that will impact business environments in the future. A practical hands-on approach coupled with internship opportunities with industry leaders equips MSBA students to switch from classroom to workplace with ease.

Developed in collaboration with NTU’s SCSE (School of Computing Science and Engineering) and SPMS (School of Physical and Mathematical Sciences), the programme also allows participants to take cross-listed modules to customise the depth of learning in areas of interest.​

The programme can be completed on a full time (1 year) or on a part-time (1.5 years to 2 years) schedule. This allows participant a flexibility to choose a schedule that best fits their career needs and pace of learning. 
    ''')
    kb = [[telegram.KeyboardButton('➡ Learn more')],
          [telegram.KeyboardButton('📩 Download brochure')],
          [telegram.KeyboardButton('💌 Join mailing list')]]
    kb_markup = telegram.ReplyKeyboardMarkup(kb, one_time_keyboard=True)
    update.message.reply_text("🚀 To continue, please kindly select one of the options 🚀\n\n Alternatively, type /No anywhere to cancel.", reply_markup=kb_markup)
    return CONT
    
def learnMore(update, context):
    user = update.message.from_user
    logger.info("User {} has selected to 'Learn More'".format(user.first_name, update.message.text))
    context.bot.send_message(chat_id=update.effective_chat.id, text="🔥 Thank you for your interest! 🔥")
    context.bot.send_message(chat_id=update.effective_chat.id, text="📚 We have a plethora of resources available to help you to make this important decision.")
    kb = [[telegram.KeyboardButton('📝 Programme Overview')],
          [telegram.KeyboardButton('❓ Why MSc Business Analytics')],
          [telegram.KeyboardButton('💯 Admission Requirements')],
          [telegram.KeyboardButton('🤝 Exchange Partners')],
          [telegram.KeyboardButton('💼 Career Development')],
          [telegram.KeyboardButton('🧙‍♂️ FAQ')]]
    kb_markup = telegram.ReplyKeyboardMarkup(kb, one_time_keyboard=True)
    update.message.reply_text("🚀 To continue, please kindly select one of the options 🚀\n\n Alternatively, type /No anywhere to cancel.", reply_markup=kb_markup)
    return LEARNMORE2

def dlBrochure(update, context):
    user = update.message.from_user
    logger.info("User {} has selected to 'Download Brochure'".format(user.first_name, update.message.text))
    context.bot.send_message(chat_id=update.effective_chat.id, text="🙏 Thank you, please allow 2-5s for the attachment to be sent. 🙏")   
    return ConversationHandler.END  
    
def joinMailList(update, context):
    user = update.message.from_user
    logger.info("User {} has selected to 'Join Mailing List'".format(user.first_name, update.message.text))
    context.bot.send_message(chat_id=update.effective_chat.id, text="🔥 Thank you for your enthusiasm! 🔥")  
    return ConversationHandler.END
    
def programmeOverview(update, context):
    user = update.message.from_user
    logger.info("User {} has selected to 'Learn More -> Programme Overview'".format(user.first_name, update.message.text))
    context.bot.send_message(chat_id=update.effective_chat.id, text="📝 Thank you for selecting Programme Overview! 📝")
    context.bot.send_message(chat_id=update.effective_chat.id, text='''The MSc Business Analytics (MSBA) equips participants to excel in the domain of business analytics. The curriculum imparts a strong business sense through the teaching of business strategy and the tools to ​appreciate the insights from the analysis of data through courses such as AI and Big Data in Business and Data Management and Visualisation. The learning for this programme adopts a very hands-on approach, with two projects allowing participants to apply classroom knowledge to real-world business situations.  

MSBA graduates will be in a position to perform the role of leading analytics projects in their domain, double-hat as both the head of a business unit and analytics business lead, or serve as a professional consultant with business domain expertise.

The highly flexible programme allows students to study for the programme either on a full time (1 year) or on a part time (1.5 years to 2 years) schedule. 

Full-time participants of MSBA programme are required to complete 8 core modules (inclusive of 2 Projects) and 4 full electives. Part-time participants of MSBA programme are required to complete 7 core modules (inclusive of 2 Projects) and 5 full electives.

Requirements to graduate: 36 Academic Units
Full Course: 3 Academic Units
Half Course: 1.5 Academic Units''')
    context.bot.send_message(chat_id=update.effective_chat.id, text='''
<pre>    
| Core modules                               | No. Of Academic Units |
|--------------------------------------------|:---------------------:|
| Data Management and Visualisation          |           3           |
| Introduction to Statistical Analysis       |           3           |
| Analytics and Machine Learning in Business |           3           |
| AI and Big Data in Business                |           3           |
| Analytics Strategy                         |           3           |
| Project I                                  |           3           |
| Project II                                 |           3           |
</pre>
    ''', parse_mode=telegram.ParseMode.HTML)
    context.bot.send_message(chat_id=update.effective_chat.id, text='''
<pre>    
| Electives                                         | No. Of Academic Units |
|---------------------------------------------------|:---------------------:|
| Programming Essentials*                           |           3           |
| Lean Operations & Analytics                       |           3           |
| AI with Advanced Predictive Techniques in Finance |          1.5          |
| AI in Enterprise                                  |          1.5          |
| Marketing and Customer Analytics                  |          1.5          |
| Supply Chain Analytics                            |           3           |
| Design Thinking & Technology Management           |          1.5          |
| Cybersecurity and Blockchain Technology           |          1.5          |
| Fundamentals of Machine Learning                  |          1.5          |
| Data Analytics for Credit and Related Risk        |          1.5          |
| Deep Learning and Contemporary AI in Business     |          1.5          |
</pre>
    ''', parse_mode=telegram.ParseMode.HTML)
    context.bot.send_message(chat_id=update.effective_chat.id, text='''
*The module "Programming Essentials" will be applicable to full-time participants to take as a compulsory elective.​​​

All Core Modules and Electives might be subject to changes​
​ ​''')
    kb = [[telegram.KeyboardButton('ℹ Module Information')],
          [telegram.KeyboardButton('Programme Calendar (Full Time)')],
          [telegram.KeyboardButton('Programme Calendar (Part Time)')],
          [telegram.KeyboardButton('Faculty Information')]
          ]
    kb_markup = telegram.ReplyKeyboardMarkup(kb, one_time_keyboard=True)
    update.message.reply_text("➡ Please select the following options to delve deeper \n\n Alternatively, type /No anywhere to cancel.", reply_markup=kb_markup)
    return PROGOVERVIEW2
    # kb = [[telegram.KeyboardButton('➡ Learn more')],
          # [telegram.KeyboardButton('🏠 Main Menu')],
          # [telegram.KeyboardButton('/No')]]
    # kb_markup = telegram.ReplyKeyboardMarkup(kb, one_time_keyboard=True)
    # update.message.reply_text("🚀 That is all. Do you want to continue learning more or return to main menu? 🚀\n\n Alternatively, type /No anywhere to cancel.", reply_markup=kb_markup)
    # return LEARNMORECATCH

def moduleInformation(update, context):
    user = update.message.from_user
    logger.info("User {} has selected to 'Learn More -> Programme Overview -> Module Information'".format(user.first_name, update.message.text))
    context.bot.send_photo(chat_id=update.effective_chat.id, photo = "https://nbs.ntu.edu.sg/Programmes/Graduate/MScBusinessAnalytics/PublishingImages/MscBAMI.jpg")
    context.bot.send_message(chat_id=update.effective_chat.id, text='''
1. Core Module

Introduction to Statistical Analysis [3AUs]

This course introduces the concepts and methods of statistical inferences: the process of inferring unknowns based on collected data. Students of this course will also learn basic programming skills to conduct statistical analyses in the R environment

This course consists of three main modules. Module 1 introduces basic elements of probability theory. Module 2 covers confidence intervals and hypothesis testing. Module 3 introduces two applications of statistical inferences, linear regression and simulation analysis. Each weekly topic will be supplemented with relevant computer applications in the R environment.

Analytics and Machine Learning in Business [3AUs]

Technological advancement renders both opportunity and shortfall for business organisation. The difference lies on the business leaders’ perspectives and understanding on technologies. Appreciation of analytics and machine learning can often turn the shortfall into opportunity and transforms a business. In this age of Artificial Intelligence, the speed for human to catch up with technology is often the key for a business to stay relevant. This course introduces the concept of analytics with machine learning and how can business embed and embrace them in its operation. 

This course will walk participants through different types of analytics and machine learning deployed in major sectors, from there deduce possible actionable of the given organization. Participants will learn about the current state of the art of machine learning development. This course condenses the main concepts in developing machine learning artefacts. Participants will also learn to start creating an Artificial Intelligence prototype and appreciate how the artificial “intelligence” is derived from human intelligence. 

Data Management and Visualisation [3AUs]

This course presents fundamental concepts and techniques in managing and presenting data for effective data-driven decision making. Topics in data management and design include data design approaches for performance and availability, such as data storage and indexing strategies; and data warehousing, such as requirement analysis, dimensional modeling, and ETL (extract, transform, load) processing. Topics in data visualisation include understanding data types, data dimensionalities, such as time-series and geospatial data; forms of data visualisation to include heat maps; and best practices for usable, consumable, and actionable data/analytic presentation.

Analytics Strategy [3AUs]

Analytics, Data Science and Artificial Intelligence are transforming business, social and government’s way of work and way of life. This course will show how important ideas and concepts were applied in real world applications to change the way we live, work and play.

AI and Big Data in Business [3AUs]

AI and Big Data make analyzing businesses has become easier through the set of data tools such as Tensor Flow and Hadoop. AI is the most in-demand methodology to solve business problems today. This module will equip students with the ability to apply AI in areas like HR, Marketing, Operation Management, Business Law, Strategic Management. Student will learn to utilize modern development tools to turn information into insights, learn to understand the development environment of AI including cloud-based AI.

Project I & II [3AUs/each]

The aim of Project I & II are to create sharp business analysis to ensure that right decisions are made. These will enable students to harness the power of data science, big data, statistics and machine learning to optimize results and achieve strategic objectives. 

Students will work on relevant industry projects from any 1 of the following categories: -

1)Work-study arrangement with organizations and industry partners;

2)Any one research laboratory in NTU; or

3)Faculty-supervised research project 

Projects will be mentored by instructors and industry mentors.
''')
    context.bot.send_message(chat_id=update.effective_chat.id, text='''
2. Electives

Programming Essentials [3AUs]*

This is an introductory course designed for post-graduate business analytics student who has no programming background and is interested to learn how to manage data and conduct business analytics programmatically. It is oriented to enhance the student technical skillset. The aim of this course is to provide a broad understanding on programming paradigms, coding techniques, how to manage data, the process of preparing data for analysis, basic of analytics, and the means to communicate analytics outcome. This course will equip the students with the ability to write customized solutions to inform business decision, integrate statistical libraries for data analysis, and construct visuals or reports for business understanding. This module will provide students with individual hands-on practices to hone the coding skillset and opportunity to develop coding solution in a team. Python language will be used as the main medium of learning because it is one of the most in-demand coding language and its user-friendly syntax is well suited for beginner level.

*The module "Programming Essentials" will be applicable to full-time participants to take as a compulsory elective.​

Lean Operations & Analytics [3AUs]

Lean operations refer to the broad managerial approaches that focus on the elimination of waste in all forms coupled with smooth, efficient flow of materials and information throughout the value chain to obtain faster customer response, higher quality and lower inventory/costs. The use of these approaches will be facilitated by the increasing computing capability within the organization coupled with greater sharing of data between different functions/entities in the organization as well as the emergence of analytics-based decision making. This represents the next frontier of competition that will distinguish winners and losers in the marketplace.

The main objectives of this course are (i) to gain an appreciation of the key principles/approaches of lean operations including waste elimination, increased speed and response, improved quality and reduced cost and (ii) to gain an understanding of the methodologies, tools and techniques necessary for analyzing, implementing, managing and continuously improving lean operations in both manufacturing and service industries.
''')
    context.bot.send_message(chat_id=update.effective_chat.id, text='''
AI with Advanced Predictive Techniques in Finance [1.5AUs]

This is an introductory course designed for students who are interested to learn how to manage data, conduct business analytics programmatically, create Artificial Intelligence (AI) model to automate business processes and create predictive model to increase profitability or returns. It is oriented to enhance the individual’s technical skillset. 

The aim is to provide a broad understanding on how to manage data, the process of preparing data for analysis, basics of analytics, using AI to automate financial analysis process and generate accounting reports. This course will equip you with the ability to write customized solutions to make informed business decisions, integrate statistical libraries for data analysis, create AI models to automate accounting and financial process. This module will provide you with individual hands-on practices to hone coding skills and creates opportunities to develop coding solutions in a team. They will utilize R and Python language as the medium of learning because it is one of the most in-demand coding language and its user-friendly syntax is well suited for the beginners. They will utilise modern development tools to turn information into insights including Keras’ Deep Learning model, Google Brain TensorFlow, Hadoop, Spark and Amazon Web Service (AWS).

AI in Enterprise [1.5AUs]

The aim of this course is to provide a broad understanding on how to use Machine Learning and Artificial Intelligence (AI) technology to solve enterprise problem or to improve the efficiency and effectiveness of enterprise processes. This course will equip you with different Machine Learning and AI model such as Regression, Decision Tree and Neural Network using AI cloud base such as Google Colab. Non-coding AI platform such as Weka will be another important part of this course.
''')
    context.bot.send_message(chat_id=update.effective_chat.id, text='''
Marketing and Customer Analytics [1.5AUs]

Business analytics —the art and science of developing useful information and insights from large amounts of data—is of growing importance in today’s world. The modern organization has scores of data (e.g. web retail traffic data) that are often under-utilized for business planning and market research opportunities. This course equips participants with the knowledge and skills, to investigate existing business operational data to continually develop innovative marketing insights and new solutions for marketing decisions. 

Participants will be exposed to various data modeling techniques using real-life business data that will allow them to provide useful predictions such as supply and demand forecast, pricing and profitability forecast, consumer trend analysis and the likes. This course systematically introduces the process of developing a strong business analytic case starting from the exploration of the data context to finally obtaining the explanatory or predictive results. The students will learn how to ask the right questions and how to draw inferences from the data by using the appropriate data mining tools. Overall, the course will enable students to approach marketing problems data-analytically, envision data-mining opportunities in organizations, and also follow up on ideas or opportunities that present themselves.
    
Supply Chain Analytics [3AUs]

Supply chain analytics is a set of approaches utilized to efficiently integrate suppliers, manufacturers, warehouses and retail stores and to efficiently manage material, information and financial flows so that merchandise is produced and distributed at the right quantities, to the right locations, and at the right time, in order to maximize system-wide surplus or value. In this course, students will learn analytics techniques (e.g. optimization, stochastic modeling, game theory) to leverage on the six drivers of facilities, inventory, transportation, information, sourcing and pricing in order to address the four supply chain challenges of complexity, uncertainty, dynamic environment and fragmented ownership. 

Design Thinking & Technology Management [1.5AUs]

Innovation is the lifeblood of organizations today, fueling continued growth and sustainability of the firm. This course will introduce to participants the key innovation skills that leaders and managers need to identify new business opportunities and to drive innovation in their firms.  Through a series of highly interactive sessions, participants will learn to apply Design Thinking to identify key customer needs and derive solutions to key problems. 

Students will also learn to apply analytics to create business models for business ideas. Students will also learn about the lean startup approach which advocates the iteration of a business model. Applying the concepts, students learn to analyze business and market opportunity through testing assumptions embedded in the business model. 

The course will further discuss the management of the latest technologies impacting the 4th industrial revolution. We discuss concepts of blockchain, examine the blockchain using cases and challenges related to its implementation. We also discuss about cases of firms commercializing artificial intelligence. 
''')
    context.bot.send_message(chat_id=update.effective_chat.id, text='''
Cybersecurity and Blockchain Technology [1.5AUs]

A full understanding and appreciation of Cybersecurity and Blockchain is critical to any business in this era of hyper-connected digital economy. With great collaborations, come greater risks, and every business moving out of silos into the ocean of data-driven applications is facing the challenges thereof. This course will introduce you to the cybersecurity landscape of the current computing ecosystem, enabling glimpses into computer security, network security, application security, cloud security and security of critical infrastructure. This course will also present to you the fundamentals of Bitcoin, cryptocurrencies and blockchain technology, to illustrate the core principles of immutability, consistency, attribution, authenticity and automation, which enable the modern fabric of decentralized applications.

Fundamentals of Machine Learning [1.5AUs]

This course covers essential concepts of machine learning and various supervised learning and unsupervised learning algorithms, such as Support Vector Machines (SVM), K-Nearest Neighbor (K-NN) classifiers, decision tree, K-means clustering, hierarchical clustering etc. This course also discusses their applications and their weaknesses. 

Data Analytics for Credit and Related Risk [1.5AUs]

This course provides fundamental tools for credit risk modeling and evaluation by data analytic techniques. This includes stochastic modeling techniques and statistical approaches to data mining based on decision trees, logistic regression and neural networks. Course concepts are illustrated by R and Python codes applied to credit rating and scoring. 

Deep Learning and Contemporary AI in Business [1.5AUs]​

​The aim of this course is to provide a broad understanding on how to use Deep Learning and Contemporary Artificial Intelligence (AI) to solve complex business problem and improve business process efficiency and effectiveness. This course will include advance AI technology like Convolution Neural Network, Generative Adversarial Network and Recurrent Neural Network including Long-Short-Term-Memory. This course will include high level application such as creating chatbot using Snatchbot. Deep Learning libraries will be used together with Python such as Google Brain Tensor Flow and Keras.
​​ ​''')

    kb = [[telegram.KeyboardButton('➡ Learn more')],
          [telegram.KeyboardButton('🏠 Main menu')],
          [telegram.KeyboardButton('/No')]]
    kb_markup = telegram.ReplyKeyboardMarkup(kb, one_time_keyboard=True)
    update.message.reply_text("🚀 That is all. Do you want to continue learning more or return to main menu? 🚀\n\n Alternatively, type /No anywhere to cancel.", reply_markup=kb_markup)
    return LEARNMORECATCH
    
def progFullTime(update, context):
    user = update.message.from_user
    logger.info("User {} has selected to 'Learn More -> Programme Overview -> Programme Calendar (Full Time)'".format(user.first_name, update.message.text))
    context.bot.send_message(chat_id=update.effective_chat.id, text='''
All our courses are conducted in English, on NTU's vibrant campuses in Singapore. Our classes are held during weekdays evenings at an easily accessible location at the One-North campus opposite Buona Vista MRT station^ and/ or on Saturday at the picturesque NTU main campus in Jurong West.

^Classes on weekdays evenings will only be held at One-North campus from Trimester 2 onwards.
 
Full-Time Programme (1 Year)
''')
    context.bot.send_photo(chat_id=update.effective_chat.id, photo = "https://raw.githubusercontent.com/tonyngmk/msba_bot/master/progFullTime.png")
    context.bot.send_message(chat_id=update.effective_chat.id, text='* The programme undergoes continuous improvement. As such, modules might be subject ​to changes')
    kb = [[telegram.KeyboardButton('➡ Learn more')],
          [telegram.KeyboardButton('🏠 Main menu')],
          [telegram.KeyboardButton('/No')]]
    kb_markup = telegram.ReplyKeyboardMarkup(kb, one_time_keyboard=True)
    update.message.reply_text("🚀 That is all. Do you want to continue learning more or return to main menu? 🚀\n\n Alternatively, type /No anywhere to cancel.", reply_markup=kb_markup)
    return LEARNMORECATCH
    
def progPartTime(update, context):
    user = update.message.from_user
    logger.info("User {} has selected to 'Learn More -> Programme Overview -> Programme Calendar (Part Time)'".format(user.first_name, update.message.text))
    context.bot.send_message(chat_id=update.effective_chat.id, text='''
All our courses are conducted in English, on NTU's vibrant campuses in Singapore. Our classes are held during weekdays evenings at an easily accessible location at the One-North campus opposite Buona Vista MRT station^ and/ or on Saturday at the picturesque NTU main campus in Jurong West.

^Classes on weekdays evenings will only be held at One-North campus from Trimester 2 onwards.

Part-Time Programme (1.5 to 2 Years)
''')
    context.bot.send_photo(chat_id=update.effective_chat.id, photo = "https://raw.githubusercontent.com/tonyngmk/msba_bot/master/progPartTime.png")
    context.bot.send_message(chat_id=update.effective_chat.id, text='''
*Students on the part time programme may choose to schedule their electives workload scheduled in Year 2 Trimester 3 to other Trimester in order to graduate earlier.Do speak to the Programme Lead after enrolling into this programme for more information​ ​​​​​

** The programme undergoes continuous improvement. As such, modules might be subject ​to changes''')
    kb = [[telegram.KeyboardButton('➡ Learn more')],
          [telegram.KeyboardButton('🏠 Main menu')],
          [telegram.KeyboardButton('/No')]]
    kb_markup = telegram.ReplyKeyboardMarkup(kb, one_time_keyboard=True)
    update.message.reply_text("🚀 That is all. Do you want to continue learning more or return to main menu? 🚀\n\n Alternatively, type /No anywhere to cancel.", reply_markup=kb_markup)
    return LEARNMORECATCH
    
def facultyInformation(update, context):
    user = update.message.from_user
    logger.info("User {} has selected to 'Learn More -> Programme Overview -> Faculty Information'".format(user.first_name, update.message.text))
    kb = [[telegram.KeyboardButton('➡ Learn more')],
          [telegram.KeyboardButton('🏠 Main menu')],
          [telegram.KeyboardButton('/No')]]
    kb_markup = telegram.ReplyKeyboardMarkup(kb, one_time_keyboard=True)
    update.message.reply_text("🚀 That is all. Do you want to continue learning more or return to main menu? 🚀\n\n Alternatively, type /No anywhere to cancel.", reply_markup=kb_markup)
    return LEARNMORECATCH

def cancel(update, context):
    user = update.message.from_user
    logger.info("User %s canceled the conversation via /No.", user.first_name)
    update.message.reply_text('Bye! Hope we can talk again soon. You know where to (/start) 😁',
                              reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END

def help(update, context):
    user = update.message.from_user
    logger.info("User %s queried for commands via /help", user.first_name)
    context.bot.send_message(chat_id=update.effective_chat.id, text="😃 Don't worry, we're here to help! 😃")
    context.bot.send_message(chat_id=update.effective_chat.id, text='''
Commands:
/start - Start the conversation
/help - This again lol''')

def main():
    f = open("botapi.txt")
    TOKEN = f.readlines()[0]
    f.close()
    updater = Updater(TOKEN, use_context=True)
    dispatcher = updater.dispatcher
    
    # Give Attendance
    msba_conv_handler = ConversationHandler(
        entry_points = [CommandHandler('start', start)],
        states={
            CONT : [MessageHandler(Filters.regex('Learn more'), learnMore),
                    MessageHandler(Filters.regex('Download brochure'), dlBrochure),
                    MessageHandler(Filters.regex('Join mailing list'), joinMailList)],
            LEARNMORE2 : [MessageHandler(Filters.regex('Programme Overview'), programmeOverview)],
            PROGOVERVIEW2 : [MessageHandler(Filters.regex('Module Information'), moduleInformation),
                             MessageHandler(Filters.regex('Programme Calendar (Full Time)'), progFullTime),
                             MessageHandler(Filters.regex('Programme Calendar (Part Time)'), progPartTime),
                             MessageHandler(Filters.regex('Faculty Information'), facultyInformation)],
            LEARNMORECATCH : [MessageHandler(Filters.regex('Learn more'), learnMore),
                              MessageHandler(Filters.regex('Main menu'), start)]
            # CONT: [CommandHandler('Yes', cont_to_date), CommandHandler('No', cancel)],
            # TIME: [MessageHandler(Filters.regex('^(Mon|Tue|Wed|Thu|Fri|Sat|Sun), (\d{4})\/(0?[1-9]|1[012])\/(0?[1-9]|[12][0-9]|3[01])'), date_to_time)],
            # OVER_1830H: [MessageHandler(Filters.regex('onwards$'), over_1830H),
                        # MessageHandler(Filters.regex('1730H$'), time1730H   _to_end)],
            # OVER_1830H_2: [MessageHandler(Filters.text, over_1830H_2)]
        },
        fallbacks=[CommandHandler('No', cancel)])
    dispatcher.add_handler(msba_conv_handler)
    # kb = [[telegram.KeyboardButton('ℹ Module Information')],
          # [telegram.KeyboardButton('Programme Calendar (Full Time)')],
          # [telegram.KeyboardButton('Programme Calendar (Part Time)')],
          # [telegram.KeyboardButton('Faculty Information')]
          
          
    # kb = [[telegram.KeyboardButton('📝 Programme Overview')],
          # [telegram.KeyboardButton('❓ Why MSc Business Analytics')],
          # [telegram.KeyboardButton('💯 Admission Requirements')],
          # [telegram.KeyboardButton('🤝 Exchange Partners')],
          # [telegram.KeyboardButton('💼 Career Development')],
          # [telegram.KeyboardButton('🧙‍♂️ FAQ')]]
   
    # Get Attendance
    # getAtt = CommandHandler('getAtt', getAttendance)
    # give_attn_conv_handler = ConversationHandler(
        # entry_points = [CommandHandler('getAtt', getAttendance)],
        # states={
            # GETATT1: [MessageHandler(Filters.text, getAttendance1)]
        # },
        # fallbacks=[CommandHandler('No', cancel)])
    # dispatcher.add_handler(give_attn_conv_handler)
  
    # Users 
    # user_conv_handler = ConversationHandler(
        # entry_points = [CommandHandler('start', newUser)],
        # states={
            # newUser2: [MessageHandler(Filters.text, newUser2), CommandHandler('No', cancel)],
            # newUser3: [MessageHandler(Filters.regex('(.*)@gmail.com$'), newUser3), CommandHandler('No', cancel)]
        # },
        # fallbacks=[CommandHandler('No', cancel)])
    # dispatcher.add_handler(user_conv_handler)
    # getUsers = CommandHandler('getUsers', getUser)
    # dispatcher.add_handler(getUsers)

    # Help
    helpCommand = CommandHandler('help', help)
    dispatcher.add_handler(helpCommand)

    # Launch
    updater.start_polling() # Start locally hosting Bot
    updater.idle()  # Run the bot until you press Ctrl-C or the process receives SIGINT,

    # PORT = int(os.environ.get('PORT', 5000))
    # updater.start_webhook(listen="0.0.0.0",
                          # port=int(PORT),
                          # url_path=TOKEN)
    # updater.bot.setWebhook('https://my-stoic-telebot.herokuapp.com/' + TOKEN)
    
if __name__ == '__main__':
    main()