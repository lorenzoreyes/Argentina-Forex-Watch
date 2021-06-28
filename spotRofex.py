from selenium import webdriver
from selenium import common
from selenium.webdriver.common import keys
from selenium.webdriver.chrome.options import Options
import pandas as pd
import time
import os, shutil

options = Options()
options.binary_location = '/usr/bin/brave-browser'
driver_path = '/usr/local/bin/chromedriver'
options.add_experimental_option("prefs",{'download.prompt_for_download': False})
bot = webdriver.Chrome(options = options, executable_path = driver_path)

bot.get('https://www.rofex.com.ar/cem/Spot.aspx')
time.sleep(1)
checkGtia = bot.find_element_by_id('ctl00_ContentPlaceHolder1_chkDLRRofex')
checkGtia.click()
checkRango = bot.find_element_by_name('ctl00$ContentPlaceHolder1$ddlPeriodo')
checkRango.click()
checkRango.send_keys(keys.Keys.ARROW_DOWN)
bot.implicitly_wait(10)
checkRango.click()
checkVer = bot.find_element_by_name('ctl00$ContentPlaceHolder1$btnVer')
checkVer.click()
bot.implicitly_wait(100)
checkExportar = bot.find_element_by_id('ctl00_ContentPlaceHolder1_btnExportar')
checkExportar.click()