from urllib.request import urlopen
from urllib.parse import quote_plus
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import  Keys
import time
import requests
import shutil

baseUrl2 = 'https://www.instagram.com/explore/tags/'
baseUrl = 'https://www.instagram.com/'

plusUrl = '증명사진'
url2 = baseUrl2 + quote_plus(plusUrl) # 원하는 이미지 파일의 tag를 활용해 이미지를 확인.
url = baseUrl

driver = webdriver.Chrome()
driver.get(url)
time.sleep(2)

input_pass = driver.find_elements_by_class_name('sqdOP')[1]
input_pass.click()

input_id = driver.find_elements_by_class_name('inputtext')[0]
input_id.send_keys('ID')
input_pass = driver.find_elements_by_class_name('inputtext')[1]
input_pass.send_keys('PASSWORD')
input_pass.send_keys(Keys.ENTER)
time.sleep(7)

input_pass = driver.find_elements_by_class_name('HoLwm')[0]
input_pass.click()

driver.get(url2)
time.sleep(3)

# time.sleep(3)
# input_pass = driver.find_elements_by_class_name('XTCLo')[0]
# input_pass.send_keys('증명사진')
# input_pass.send_keys(Keys.ENTER)
# time.sleep(1)
# input_pass.send_keys(Keys.ENTER)



html = driver.page_source
soup = BeautifulSoup(html,'html.parser')
imglist = []
count_2 = 0

time.sleep(1)
start = time.time()

for i in range(0, 3000):
    print(i)
    insta = soup.select('.v1Nh3.kIKUG._bz0w')
    count = len(imglist)
    for i in insta:
        # print('https://www.instagram.com' + i.a['href'])
        imgUrl = i.select_one('.KL4Bh').img['src']
        imglist.append(imgUrl)
        imglist = list(set(imglist))
    print(len(imglist))
    # height = driver.execute_script("return document.body.scrollHeight")
    # print("height : ",height)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        # height_2 = driver.execute_script("return document.body.scrollHeight")
        # # print("height_2 : ", height_2)
    time.sleep(1)

    if(len(imglist) == count):
        print(count_2)
        count_2 += 1
        if (count_2 == 7 ):
            driver.execute_script("window.scrollTo(document.body.scrollHeight/8,0);")
            count_2 = 0

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    print(time.time() - start)

n = 0


for i in range(len(imglist)):
    # This is the image url.
    print(i)
    image_url = imglist[n]
    print(image_url)
    # Open the url image, set stream to True, this will return the stream content.
    resp = requests.get(image_url, stream=True)
    # Open a local file with wb ( write binary ) permission.
    local_file = open('./img2/' + plusUrl + str(n) + '.jpg', 'wb')
    # Set decode_content value to True, otherwise the downloaded image file's size will be zero.
    resp.raw.decode_content = True
    # Copy the response stream raw data to local image file.
    shutil.copyfileobj(resp.raw, local_file)
    # Remove the image url response object.
    n += 1
    del resp

driver.close()
