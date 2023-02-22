import pandas as pd
import numpy as np
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By


def pageTracerse(job,location):
    driver=webdriver.Chrome('chromedriver.exe')
    driver.set_window_size(1120, 1000)
    driver.get('https://www.glassdoor.co.in/Job/index.htm')
    k=0
    
    WebDriverWait(driver,30).until(EC.presence_of_element_located((By.CLASS_NAME,"keyword")))
    driver.find_element(By.CLASS_NAME,'keyword').send_keys(job)
    driver.find_element(By.ID,'LocationSearch').clear()
    driver.find_element(By.ID,'LocationSearch').send_keys(location)
    driver.find_element(By.ID,'HeroSearchButton').click()
    
    dict=[]
    pagerem=True
    c=0
    while(pagerem):
        time.sleep(10)
        WebDriverWait(driver,30).until(EC.presence_of_element_located((By.XPATH,'//*[@id="MainCol"]/div/ul')))
        job_lists = driver.find_element(By.XPATH,'//*[@id="MainCol"]/div/ul')
        job_buttons=job_lists.find_elements(By.TAG_NAME,'li')
        for buttons in job_buttons:
            WebDriverWait(driver,30).until(EC.element_to_be_clickable((buttons)))
            buttons.click()
            if(k==0):
                    WebDriverWait(driver,30).until(EC.presence_of_element_located((By.XPATH,'//*[@id="JAModal"]/div/div[2]/span')))
                    WebDriverWait(driver,30).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="JAModal"]/div/div[2]/span'))).click()
                    #driver.find_element(By.XPATH,'//*[@id="JAModal"]/div/div[2]/span').click()
                    k+=1
            WebDriverWait(driver,30).until(EC.presence_of_element_located((By.XPATH,'//*[@id="JDCol"]/div/article/div/div/div/div/div/div[3]/div/div/div')))
            company_name=driver.find_element(By.XPATH,'//*[@id="JDCol"]/div/article/div/div/div/div/div/div[3]/div/div/div').text
            job_title=driver.find_element(By.XPATH,'//*[@id="JDCol"]/div/article/div/div/div/div/div/div[3]/div/div[2]').text
            location=driver.find_element(By.XPATH,'//*[@id="JDCol"]/div/article/div/div/div/div/div/div[3]/div/div[3]').text
            jobdesc=driver.find_element(By.XPATH,"//*[@id='JobDescriptionContainer']/div/div").text
            #WebDriverWait(driver,30).until(EC.presence_of_element_located((By.XPATH,'//*[@id="JDCol"]/div/article/div/div/div/div/div/div[3]/div/div/div/span')))
            try:
                company_rating=driver.find_element(By.XPATH,'//*[@id="JDCol"]/div/article/div/div/div/div/div/div[3]/div/div/div/span').text
            except:
                company_rating='-1'
            comp_size=comp_type=industry=sector=revenue=-1
            try:
                compdet=driver.find_element(By.XPATH,'//*[@id="EmpBasicInfo"]/div/div')
                compdetc=compdet.find_elements(By.TAG_NAME,'div')
        
                for components in compdetc:
                        elements=components.find_elements(By.TAG_NAME,'span')
                        if(elements[0].text=='Size'):
                                comp_size=elements[1].text
                        if(elements[0].text=='Type'):
                                comp_type=elements[1].text
                        if(elements[0].text=='Industry'):
                                industry=elements[1].text
                        if(elements[0].text=='Sector'):
                                sector=elements[1].text
                        if(elements[0].text=='Revenue'):
                                revenue=elements[1].text
            except:
                comp_size=comp_type=industry=sector=revenue=-1
            try:
                sal=driver.find_element(By.XPATH,'//*[@id="JDCol"]/div/article/div/div[2]/div/div[2]/div/div/div[2]/div').text
                if 'Visit' in sal:
                        sal=-1
            except:
                sal=-1
            dict.append({'Job Title':job_title,
                'Company Name':company_name,
                'Company Rating':company_rating,
                'Location':location,
                'Job Description':jobdesc,
                'Comp Size':comp_size,
                'Comp Type':comp_type,
                'Comp Industry':industry,
                'Comp Sector':sector,
                'Comp Reve':revenue,
                'Salary':sal})
            c+=1
        try:
            WebDriverWait(driver,30).until(EC.element_to_be_clickable((By.XPATH,'//*[@class="pageContainer"]/button[7]')))
            driver.find_element(By.XPATH,'//*[@class="pageContainer"]/button[7]').click()
        except:
            pagerem=False
    driver.close()
    driver.quit()
    return pd.DataFrame(dict)