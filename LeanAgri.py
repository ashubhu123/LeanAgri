import pandas as pd
from selenium import webdriver
import urllib.request

base_url = 'http://www.agriculture.gov.au/pests-diseases-weeds/plant#identify-pests-diseases'
driver = webdriver.Firefox(executable_path=r'D:/geckodriver.exe')
downloaded_data = (r"D:\Python -exapmles\monadplus\data.xlsx")
driver.get(base_url)
page_links = []
pests =[]
img_links=[]
origin=[]
How_to_identify =[]
suspect_speciman = []
What_alloewd =[]
xpath=[]
img=[]
img_name=[]
driver.implicitly_wait(10)
data = driver.find_element_by_xpath('/html/body/form/div[3]/div[2]/div[7]/span/div[1]/div[3]/div/ul[2]').find_elements_by_class_name('flex-item')
l = len(data)
try:
    for i in data:
        pests.append(i.text)
        page_links.append(i.find_element_by_tag_name('a').get_attribute('href'))
        img_links.append(i.find_element_by_tag_name('img').get_attribute('src'))
except Exception as e:
    print(e)

for i in range(l)[0:26]:
    path = '//*[@id="collapsefaq"]/ul[2]/li[' + str(i+1) + ']'
    xpath.append(path)
    # driver.implicitly_wait(2)
try:
    for i in xpath:
        a = driver.find_element_by_xpath(i).find_element_by_tag_name('a').find_element_by_tag_name('img').get_attribute('src')
        n ,ext= a.split('.jpg')
        img.append(a)
    for i in img:
        images = urllib.request.urlretrieve(i,filename= str(img.index(i))+'.jpg')
        img_name.append(images[0])#creating list of image name list to save
except :
    print('nothing to do')
# print(img_name[0:5])
for i in page_links:
    driver.get(i)
    try:
        event4 = driver.find_element_by_xpath('/html/body/form/div[3]/div[2]/div[7]/span/div[1]/div[3]/div[1]/div[2]')# or '/html/body/div[1]/div[3]/div[1]/h1')
        string = event4.text
        new = (string.split('\n'))
        n = new[3].split(':')[1]
        origin.append(n)
    except :
        origin.append('Unknown')

    try:
        event1 = driver.find_element_by_xpath('//*[@id="collapsible-trigger-link-0"]').click()
        driver.implicitly_wait(10)
        a = driver.find_element_by_class_name('collapsefaq-content').find_elements_by_tag_name('p')
        one = []
        for i in a[0:5]:
            data =(i.text)
            one.append(data)
        How_to_identify.append(one)
    except :
        How_to_identify.append('Data not available')
        # print('Data not available')

    try:
        event3 = driver.find_element_by_id('collapsible-trigger-link-2').click()
        driver.implicitly_wait(10)
        data = driver.find_element_by_css_selector('#collapsefaq > div:nth-child(11)').find_elements_by_tag_name('p')
        l = []
        for i in data[0:3]:
            a= i.text
            l.append(a)
        suspect_speciman.append(l)
    except:
        # print('None')
        suspect_speciman.append('Data not available')
    #
    try:
        event3 = driver.find_element_by_id('collapsible-trigger-link-1').click()
        driver.implicitly_wait(10)
        data = driver.find_element_by_css_selector('#collapsefaq > div:nth-child(9)').find_elements_by_tag_name('p')
        data1 = driver.find_element_by_css_selector('#collapsefaq > div:nth-child(9)').find_elements_by_tag_name('li')
        li_text=[]
        p_t=[]
        all=[]
        for i in data[0:3]:
            a = i.text
            p_t.append(a)
        for j in data1:
            l= j.find_element_by_tag_name('a')
            t, links =l.text, l.get_attribute('href')
            li_text.append(t+links)
        all.append(p_t + li_text)
        What_alloewd.append(all)
    except:
        # print('None')
        What_alloewd.append('Data not available')

driver.implicitly_wait(20)
driver.close()

#writing data to file
row=1
df = pd.DataFrame(data ={'Disease/Pests':pests,'Image link':img_links,'Origin':origin,'How to identify the pest':How_to_identify,'Secure any suspect specimens':suspect_speciman,'What id allowed in Australia?':What_alloewd})
df.to_excel('data.xlsx',index=False)
#inserting images to file
writer = pd.ExcelWriter('data.xlsx', engine='xlsxwriter')
df.to_excel(writer,sheet_name='Sheet1')
workbook=writer.book
worksheet=writer.sheets['Sheet1']
for i in img_name:
    worksheet.write('H0','Images')
    worksheet.insert_image(row,col=7,filename=i,options={'x_scale':0.1, 'y_scale':0.1,'x_offset':1,'y_offste':1,'positioning':1})
    row +=1
writer.save()

