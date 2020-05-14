import csv
import os
import requests
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver import ActionChains


with open("FGDURLS.csv") as csvfile:
    urls = csvfile.read()
    urllist = urls.split("\n")


for FGDURL in urllist:
    NoIntrons = False
    data = requests.get(FGDURL)
    soup = BeautifulSoup(data.text, 'html.parser')
    maintable = soup.find(
        "table", {"class": "table table-striped table-hover"})
    maintabletrs = maintable.find_all("tr")
    ths = []
    for tr in maintabletrs:
        trths = tr.find_all("th")
        trtds = tr.find_all("tds")
        for th in trths:
            if th.text.strip() == "Transcript Length(bp)":
                tdofinterest = ((tr.find("td")).text.strip())
                tdofinterest = tdofinterest.replace("Download", "")
                tdofinterest = tdofinterest.replace("View", "")
                tdofinterest = tdofinterest.replace("\n", "")
                tdofinterest = tdofinterest.replace(",", "")
                tdofinterest.strip()
                TranscriptLength = float(tdofinterest.strip())
                print("Transcript Length = " + tdofinterest)
            if th.text.strip() == "CDS Length(bp)":
                tdofinterest = ((tr.find("td")).text.strip())
                tdofinterest = tdofinterest.replace("Download", "")
                tdofinterest = tdofinterest.replace("View", "")
                tdofinterest = tdofinterest.replace("\n", "")
                tdofinterest = tdofinterest.replace(",", "")
                tdofinterest.strip()
                CDSLength = float(tdofinterest.strip())
                print("CDS Length = " + tdofinterest)
    if CDSLength == TranscriptLength:
        NoIntrons = True
        strippedURL = FGDURL.replace(
            "https://cottonfgd.org/profiles/transcript/", "")
        strippedURL = strippedURL.replace("/structure/", "")
        print("No introns for " + strippedURL)
    else:
        NoIntrons = False
        strippedURL = FGDURL.replace(
            "https://cottonfgd.org/profiles/transcript/", "")
        strippedURL = strippedURL.replace("/structure/", "")
        print("Found introns for " + strippedURL)

    if NoIntrons == False:
        modifiedURL = (
            "https://cottonfgd.org/profiles/transcript/" + strippedURL + "/structure")
        print(modifiedURL)
        data = requests.get(modifiedURL)
        soup = BeautifulSoup(data.text, 'html.parser')
        maintable = soup.find(
            "table", {"class": "table table-striped table-hover exon-intron-table"})
        if maintable != None:
            maintabletrs = maintable.find_all("tr")
            for tr in maintabletrs:
                trtds = tr.find_all("td")
                if len(trtds) > 6:
                    print("Type = " + trtds[1].text +
                          " Length = " + trtds[7].text)
        else:
            pass
