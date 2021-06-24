import smtplib    
from contextlib import contextmanager
from bcra import *         # to run and update data from 
from futuresCurve import * # the rest of the scripts
import pandas as pd, datetime as dt,numpy as np
import re, os, ssl
import credentials, glob 
import base64
from templateReport import * # template html of all content of the email
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email import encoders

today = dt.date.today().strftime('%Y-%m-%d')
hoy = dt.date.today().strftime('%d/%m/%y')
excel = pd.read_csv(f'Dollar Futures {today}.csv')
excel = excel.rename(columns={'Unnamed: 0':''})
excel['Close'] = ['$ {:,.2f}'.format(i).replace('.','p').replace(',','.').replace('p',',') for i in list((excel['Close'].astype(float)).values)]
excel['30 days'] = ['$ {:,.2f}'.format(i).replace('.','p').replace(',','.').replace('p',',') for i in list((excel['30 days'].astype(float)).values[:-2])] + [np.nan,np.nan]
excel['Percent'] = ['{:,.2f}%'.format(i).replace('.','p').replace(',','.').replace('p',',') for i in list((excel['Percent'].astype(float)).values[:-2])] + [np.nan,np.nan]
excel.iloc[:,-4:] = excel.iloc[:,-4:] * 100.0
excel['Impl. Rate'] = [np.nan] + ['{:,.2f}%'.format(i).replace('.','p').replace(',','.').replace('p',',') for i in list((excel['Impl. Rate'].astype(float)).values[1:])]
excel['Previous Impl. Rate'] = [np.nan] + ['{:,.2f}%'.format(i).replace('.','p').replace(',','.').replace('p',',') for i in list((excel['Previous Impl. Rate'].astype(float)).values[1:-2])] + [np.nan,np.nan]
excel['Effective Annual Rate'] = [np.nan] + ['{:,.2f}%'.format(i).replace('.','p').replace(',','.').replace('p',',') for i in list((excel['Effective Annual Rate'].astype(float)).values[1:])]
excel['Impl. Rate 30d'] = [np.nan] + ['{:,.2f}%'.format(i).replace('.','p').replace(',','.').replace('p',',') for i in list((excel['Impl. Rate 30d'].astype(float)).values[1:])]

html_file = excel.to_html(na_rep = "",index=False).replace('<th>','<th  style="background-color: rgb(0,0,0)">').replace('<table>','<table style="width:100%">')

receivers = pd.read_csv('FakeClients.csv')


# We assume that the image file is in the same directory that you run your Python script from
fp = open('ArgentinaFX.png', 'rb')
image1 = MIMEImage(fp.read())
fp.close()
fp = open('SpotnFutures.png', 'rb')
image2 = MIMEImage(fp.read())
fp.close()
fp = open('rateImpl.png', 'rb')
image3 = MIMEImage(fp.read())
fp.close()


def sendEmails(message):
    msg = MIMEMultipart('alternative',text='URGENT!')
    msg['X-Priority'] = '1'
    msg['Subject'] = f"Argentina Forex Report {clients.Names[i]} day {hoy}"
    msg['From'] = credentials.account
    msg['To'] = receivers.Emails.values[i]
    # Adjunto el excel. Descomentar para adjuntarlo.
    fp = open(f'Central Bank Report {today}.xlsx', 'rb')
    part = MIMEBase('application','vnd.ms-excel')
    part.set_payload(fp.read())
    fp.close()
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', 'attachment', filename=f'Argentina Central Bank Report {clients.Names[i]} day {today}.xlsx')
    msg.attach(part)
    # Adjunto el excel. Descomentar para adjuntarlo.
    fp = open(f'Dollar Futures {today}.csv', 'rb')
    portfolio = MIMEBase('application','vnd.ms-excel')
    portfolio.set_payload(fp.read())
    fp.close()
    encoders.encode_base64(portfolio)
    portfolio.add_header('Content-Disposition', 'attachment', filename=f'Argentina Forex Report {today}.xlsx')
    msg.attach(portfolio)
    # body of the email
    part1 = message
    #part1 = _fix_eols(part1).encode('utf-8')
    part1 = MIMEText(part1, 'html')
    msg.attach(part1)
    ## Specify the  ID according to the img src in the HTML part
    image1.add_header('Content-ID', '<ArgentinaFX>')
    msg.attach(image1)
    image2.add_header('Content-ID', '<SpotnFutures>')
    msg.attach(image2)
    image3.add_header('Content-ID', '<rateImpl>')
    msg.attach(image3)
    # send especific email
    s = smtplib.SMTP("smtp.gmail.com")
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    # login account + password
    server.login(credentials.account,credentials.password)
    server.sendmail(credentials.account,
                    receivers.Emails.values[i],
                    msg.as_string())
    s.quit()

for i in range(1):#(len(receivers)):    
  clients = pd.DataFrame(receivers.iloc[i,:].copy())
  clients = clients.T
  plotForex = f"""<img src="cid:ArgentinaFX" style="width:100%; display: block; margin-left: auto; margin-right: auto;" loading="lazy">"""  
  plotFutures = """<img src="cid:SpotnFutures" style="width:100%; display: block; margin-left:auto; margin-right:auto;" loading="lazy">"""
  plotRate = """<img src="cid:rateImpl" style="width:100%; display: block; margin-left:auto; margin-right:auto;" loading="lazy">"""

  message = style + highlight + explanation + plotForex + html_file + curve_futures + plotFutures + plotRate + endWords + end_html 

  e = sendEmails(message)
  print(f"{dt.datetime.now().strftime('%H:%M:%S:%f')} Forex Watch {clients.Names.values[0]} at {receivers.Emails.values[i]} SENT!!!")
  e

