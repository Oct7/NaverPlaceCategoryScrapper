
from dotenv import load_dotenv
from time import sleep
from multiprocessing import Pool
from concurrent.futures import ThreadPoolExecutor
from bs4 import BeautifulSoup
import os
import asyncio
import concurrent.futures
import requests
import time
import openpyxl
from aiohttp import ClientSession
import re


 
excel = openpyxl.load_workbook("data.xlsx", data_only=True)

 
def getData(index): 
    url = 'https://pcmap.place.naver.com/restaurant/' + str(index)
    html = requests.get(url)
    sleep(0.5)
    while(html.status_code!=200):
        print(html.status_code)
        html = requests.get(url)
        sleep(0.5)
    
    soup = BeautifulSoup(html.content,'html.parser',from_encoding='utf-8')
    if len( soup(text=re.compile('_3ocDE')))>0:
        return soup.select('span._3ocDE')[0].text
    


 

# async def getData(index): 
#     url = 'https://pcmap.place.naver.com/restaurant/' + str(index)
#     async with ClientSession() as session:
#         async with session.get(url,headers = {'User-agent': 'your bot 0.1'}) as response:
#             r = await response.read()
#             sleep(1)
#             print(response.status)
#             print(index)
#             if response.status != 200:
#                 await getData(index)
#                 # return None
#             else:
#                 soup = BeautifulSoup(r,'html.parser',from_encoding='utf-8')
#                 # print(index)
#                 # print(soup(text=re.compile('_3ocDE')))
#                 if len( soup(text=re.compile('_3ocDE')))>0:
#                     return soup.select('span._3ocDE')[0].text
    


def incrementID():
    
    with open(".env",'r') as f: #open a file in the same folder
        currentId = f.readlines() 
    b = int(currentId[0].split('=')[1])                    #get integer at first position
    b = b+1                          #increment
    with open(".env",'w') as f: #open same file
        f.write('CURRENT_ID='+str(b))
    
def loadCurrentIdFromEnv():
    return os.getenv('CURRENT_ID')
    
def addDataToExcel(data):
    # 엑셀파일 쓰기
    sheet = excel.worksheets[0]
    titles = sheet['A']
    isAdded = False
    for index in range(0, len(titles)):
        if titles[index].value == data:
            sheet.cell(row=index+1,column=2).value = str(int(sheet.cell(row=index+1,column=2).value) + 1)
            isAdded = True
            break
        
    if isAdded != True :
        sheet.append([data,'1'])
    
    # excel.worksheets[0] = sheet
    excel.save(filename="data.xlsx")


def main(value,):
    print(value)
    addData = getData(value)
    print(addData)
    if(addData!=None):
        addDataToExcel(addData,)
        
        
def main_exec(value,):
    thread_list=list()
    with ThreadPoolExecutor(max_workers=8) as executor:
        for index in range(value*100,(value+1)*100):
            thread_list.append(executor.submit(main(index,)))
        for execution in concurrent.futures.as_completed(thread_list):
            incrementID()
            




if __name__ == "__main__":
    load_dotenv()
    currentId = loadCurrentIdFromEnv()
    addData = ''
    start_time = time.time()
    with Pool(processes=8) as pool:  
        pool.map(main_exec,[0,1,2,3],)
    


        
    print("--- elapsed time %s seconds ---" % (time.time() - start_time))