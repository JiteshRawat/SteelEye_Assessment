# -*- coding: utf-8 -*-
"""Steeleye_assignment_final.ipynb

Original file is located at
  https://colab.research.google.com/drive/1yT-peNV7WDiFE_49C9a1axpU_6laPNN4
"""
import xml.etree.ElementTree as ET
import xmltodict, csv, requests, boto3
import logging
from zipfile import ZipFile


logging.basicConfig(filename= 'C:\\Users\\jitez\\Music\\steeleye_assignment\\test.log',level=logging.WARNING)
mytree= ET.parse("C:\\Users\\jitez\\Music\\steeleye_assignment\\select.xml")
root= mytree.getroot()
URL = root[1][0][1].text
response= requests.get(URL)
open('file.zip', 'wb').write(response.content)
with ZipFile('file.zip', 'r') as zipObj:
  # Extract all the contents of zip file in current directory
  zipObj.extractall()

# PARSE XML FILE
with open("DLTINS_20210117_01of01.xml", encoding="utf8") as xmlfile:
  xml = xmltodict.parse(xmlfile.read())

xml1= xml['BizData']['Pyld']['Document']['FinInstrmRptgRefDataDltaRpt']['FinInstrm']
names= ['FinInstrmGnlAttrbts.Id', 'FinInstrmGnlAttrbts.FullNm', 'FinInstrmGnlAttrbts.ClssfctnTp',
        'FinInstrmGnlAttrbts.CmmdtyDerivInd', 'FinInstrmGnlAttrbts.NtnlCcy', 'Issr']

# CREATE CSV FILE
csvfile = open("C:\\Users\\jitez\\Music\\steeleye_assignment\\data.csv",'w',encoding='utf-8')
csvfile_writer = csv.writer(csvfile)
# ADD HEADER
csvfile_writer.writerow(names)
#FOR EACH ITEM IN XML
for i in range(0, len(xml1)):

  # EXTRACT DETAILS
  if 'TermntdRcrd' in xml1[i]:
    csv_line = xml1[i]['TermntdRcrd']['FinInstrmGnlAttrbts'].values()
  elif 'ModfdRcrd' in xml1[i]:
    csv_line = xml1[i]['ModfdRcrd']['FinInstrmGnlAttrbts'].values()
  elif 'NewRcrd' in xml1[i]:
    csv_line = xml1[i]['NewRcrd']['FinInstrmGnlAttrbts'].values()
    
  # ADD A NEW ROW TO CSV FILE
  csvfile_writer.writerow(csv_line)

#Code to upload file in AWS S3 bucket
#3_client=  boto3.client('s3')
#response= s3_client.upload_file('/data.csv', 'my_bucket11', 'data.csv')

