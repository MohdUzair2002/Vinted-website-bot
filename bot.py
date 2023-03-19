from selenium import webdriver
import requests
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time
import csv
image_l=[]
title_l=[]
description_l=[]
size_l=[]
brand_l=[]
condition_l=[]
colour_l=[]
price_l=[]
links_all=[]
with open('link_all.csv', 'r') as file:
    reader = csv.reader(file)
    for row in reader:
        links_all.append(row[0])
        print(row[0])
chrome_options =webdriver.ChromeOptions()
s=Service(ChromeDriverManager().install())
chrome_options.add_argument("user-data-dir=C:/Users/User/AppData/Local/Google/Chrome/User Data")

chrome_options.add_argument("--start-maximized")
driver = webdriver.Chrome(service=s,options=chrome_options)
wait=WebDriverWait(driver, 60)
i=0
while(i<len(links_all)):
    url=links_all[i]
    driver.get(url)

    image= wait.until(EC.element_to_be_clickable((By.XPATH,"//a[@class='item-thumbnail is-loaded']")))
    image=driver.find_elements(By.XPATH,"//a[@class='item-thumbnail is-loaded']")
    print(len(image))
    n=0
    length=len(image)
    image_l_l=[]
    while(n <length ):

        image=driver.find_elements(By.XPATH,"//a[@class='item-thumbnail is-loaded']")[n].get_attribute('href')
        image_l_l.append(image)
        print(image)
        print(image_l_l)
        
        n=n+1
    
    image_l.append(image_l_l)
    title=driver.find_element(By.XPATH,"//h2[@class='web_ui__Text__text web_ui__Text__title web_ui__Text__left']").text
    title_l.append(title)
    print(title)
    v=0
    while(v<len(image_l_l)):
        with open(f'{title}{v+1}.jpg', 'wb') as handle:
            response = requests.get(image_l_l[v], stream=True)

            if not response.ok:
                print(response)

            for block in response.iter_content(1024):
                if not block:
                    break

                handle.write(block)
        v+=1
    description=driver.find_element(By.XPATH,"//span[@class='web_ui__Text__text web_ui__Text__body web_ui__Text__left web_ui__Text__format']").text
    description_l.append(description)
    print(description)

    print("-------")
    brand=driver.find_element(By.XPATH,"//div[@itemprop='brand']").text
    brand_l.append(brand)
    print(brand)

    condition=driver.find_elements(By.XPATH,"//div[@itemprop='itemCondition']")[0].text
    condition_l.append(condition.split('\n')[0])
    print(condition.split('\n')[0])

    colour=driver.find_element(By.XPATH,"//div[@itemprop='color']").text
    colour_l.append(colour)
    print(colour)
    size_checker_l=[]
    size_checker_l.append('a')
    try:
        time.sleep(10)
        size_checker_l[0]=('n')
        size_checker=driver.find_element(By.XPATH,"//*[text()='Tamaño']").click()
        
    except:
        size_checker_l[0]=('y')
    if(size_checker_l[0]!='y'):
        size=driver.find_elements(By.XPATH,"//div[@class='details-list__item-value']")[1].text
        size_l.append((size.split('\n')[0]))
        print((size.split('\n')[0]))
        size_checker_l=[]
    else:
        size_l.append('y')
    price=driver.find_element(By.XPATH,"//h1[@class='web_ui__Text__text web_ui__Text__heading web_ui__Text__left']").text
    price_l.append(price)
    print(price)
    delete_order=driver.find_elements(By.XPATH,"//*[@class='c-button__label']")[-1]
    driver.execute_script("arguments[0].click();", delete_order)
    confirm= wait.until(EC.element_to_be_clickable((By.XPATH,"//*[@value='Confirmar y eliminar']")))
    confirm=driver.find_element(By.XPATH,"//*[@value='Confirmar y eliminar']")
    driver.execute_script("arguments[0].click();", confirm)
    wait.until(EC.element_to_be_clickable((By.XPATH,"//h1[@class='web_ui__Text__text web_ui__Text__heading web_ui__Text__left web_ui__Text__amplified web_ui__Text__bold']")))
    # //h1[@class='web_ui__Text__text web_ui__Text__heading web_ui__Text__left web_ui__Text__amplified web_ui__Text__bold']
    i+=1

j=0
while(j<len(links_all)):
    driver.get("https://www.vinted.es/items/new")
    b=0
    while(b<len(image_l[j])):
        image_upload=wait.until(EC.element_to_be_clickable((By.XPATH,"//input[@class='c-input__value c-input__value--with-suffix u-cursor-pointer']")))
        image_upload=driver.find_element(By.XPATH,"//input[@type='file']")
        image_upload.send_keys(f'W:/vinted bot/{title_l[j]}{b+1}.jpg')
        print(f"{title_l[j]}{b+1}")
        b+=1
        time.sleep(3)

    title=driver.find_elements(By.XPATH,"//input[@class='web_ui__Input__value']")[0]
    title.send_keys(title_l[j])


    description=driver.find_elements(By.XPATH,"//textarea[@class='web_ui__Input__value']")[0]
    description.send_keys(description_l[j])

    wait.until(EC.element_to_be_clickable((By.XPATH,"//div[@class='web_ui__Image__image web_ui__Image__cover web_ui__Image__square web_ui__Image__rounded web_ui__Image__scaled web_ui__Image__ratio']")))
    
    time.sleep(2)
    category=driver.find_element(By.XPATH,"//input[@class='c-input__value c-input__value--with-suffix u-cursor-pointer']")
    # category.click()
    driver.execute_script("arguments[0].click();", category)
    wait.until(EC.element_to_be_clickable((By.XPATH,"//*[@class='web_ui__Radio__button'][@tabindex='0']")))
    category=driver.find_elements(By.XPATH,"//*[@class='web_ui__Radio__button'][@tabindex='0']")[0]
    driver.execute_script("arguments[0].click();", category)
    # time.sleep(5)
    brand1=brand_l[j]
    brand1=brand1.lower()
    brand1=brand1.capitalize()
    brand1=brand1.replace(" ","")
    brand_input=driver.find_elements(By.XPATH,"//input[@class='c-input__value c-input__value--with-suffix']")[-1].click()
    wait.until(EC.element_to_be_clickable((By.XPATH,f"//*[text()='{brand1.capitalize()}']")))
    brand_input=driver.find_element(By.XPATH,f"//*[text()='{brand1.capitalize()}']")
    driver.execute_script("arguments[0].click();", brand_input)


    time.sleep(1.25)
    if(size_l[j]!='y'):
        size=driver.find_elements(By.XPATH,"//input[@class='c-input__value c-input__value--with-suffix u-cursor-pointer']")[1]
        size.click()
        wait.until(EC.element_to_be_clickable((By.XPATH,f"//*[text()={size_l[j]}]")))
        size_select=driver.find_element(By.XPATH,f"//*[text()={size_l[j]}]")
        size_select.click()

        condition1=condition_l[j]
        condition1=condition1.lower()
        condition1=condition1.capitalize()
        condition=driver.find_elements(By.XPATH,"//input[@class='c-input__value c-input__value--with-suffix u-cursor-pointer']")[2]
        driver.execute_script("arguments[0].click();", condition)
        print(condition1)
        wait.until(EC.element_to_be_clickable((By.XPATH,f"//*[text()='{condition1}']")))
        condition=driver.find_element(By.XPATH,f"//*[text()='{condition1}']")
        driver.execute_script("arguments[0].click();", condition)

        no_of_colours=colour_l[j].split(",")
        colour=driver.find_elements(By.XPATH,"//input[@class='c-input__value c-input__value--with-suffix u-cursor-pointer']")[3].click()
        for color2 in no_of_colours:  
            color1=color2.lower()
            color3=color1.capitalize()
            color=color3.replace(" ","")
            print(color.capitalize())
            wait.until(EC.element_to_be_clickable((By.XPATH,f"//*[text()='{color.capitalize()}']")))
            colour=driver.find_element(By.XPATH,f"//*[text()='{color.capitalize()}']")
            driver.execute_script("arguments[0].click();", colour)
            print(f"//*[text()='{color.capitalize()}']")
        
        close_tab=driver.find_elements(By.XPATH,"//span[@class='web_ui__Icon__icon web_ui__Icon__small']")[-1]
        driver.execute_script("arguments[0].click();", close_tab)
  
    else:
        condition1=condition_l[j]
        condition1=condition1.lower()
        condition1=condition1.capitalize()
        condition=driver.find_elements(By.XPATH,"//input[@class='c-input__value c-input__value--with-suffix u-cursor-pointer']")[1]
        driver.execute_script("arguments[0].click();", condition)
        print(condition1)
        wait.until(EC.element_to_be_clickable((By.XPATH,f"//*[text()='{condition1}']")))
        condition=driver.find_element(By.XPATH,f"//*[text()='{condition1}']")
        driver.execute_script("arguments[0].click();", condition)

        # category=driver.find_element(By.XPATH,"//input[@class='c-input__value c-input__value--with-suffix u-cursor-pointer']")
        # # category.click()
        # driver.execute_script("arguments[0].click();", category)
        # time.sleep(10)
        # category=driver.find_elements(By.XPATH,"//div[@class='web_ui__Cell__title']")[0]
        # driver.execute_script("arguments[0].click();", category)
        # time.sleep(3)
        # no_of_colours=colour_l[j].split(",")
        # time.sleep(200)
        no_of_colours=colour_l[j].split(",")
        colour=driver.find_elements(By.XPATH,"//input[@class='c-input__value c-input__value--with-suffix u-cursor-pointer']")[2].click()
        for color2 in no_of_colours:  
            color1=color2.lower()
            color3=color1.capitalize()
            color=color3.replace(" ","")
            print(color.capitalize())
            wait.until(EC.element_to_be_clickable((By.XPATH,f"//*[text()='{color.capitalize()}']")))
            colour=driver.find_element(By.XPATH,f"//*[text()='{color.capitalize()}']")
            driver.execute_script("arguments[0].click();", colour)
            print(f"//*[text()='{color.capitalize()}']")
        
        close_tab=driver.find_elements(By.XPATH,"//span[@class='web_ui__Icon__icon web_ui__Icon__small']")[-1]
        driver.execute_script("arguments[0].click();", close_tab)

    price=driver.find_elements(By.XPATH,"//input[@class='web_ui__Input__value']")[1]
    price.send_keys(price_l[j])
    
    
    select_package=driver.find_elements(By.XPATH,"//*[@class='web_ui__Text__text web_ui__Text__title web_ui__Text__left web_ui__Text__parent']")[0]
    select_package.click()
    select_package.click()
    

    submit=driver.find_elements(By.XPATH,"//span[@class='web_ui__Button__label']")[-1]
    submit.click()
    j+=1
time.sleep(10)
# time.sleep(100)
# time.sleep(1000)
