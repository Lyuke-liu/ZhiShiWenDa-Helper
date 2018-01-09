# -*- coding:utf-8 -*-
import requests, base64, json, os, time,config
from PIL import Image
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from aip import AipOcr

driver = webdriver.Chrome(config.driver_location)
# 访问百度
driver.get('http://www.baidu.com')

count = 0
screenpath = config.image_directory

def get_words(image):
  # 定义常量
  APP_ID = 'xxxxxx'
  API_KEY = 'xxxxxx'
  SECRET_KEY = 'xxxxxx'
  
  # 初始化AipFace对象
  aipOcr = AipOcr(APP_ID, API_KEY, SECRET_KEY)

  # 定义参数变量
  options = {
    'detect_direction': 'true',
    'language_type': 'CHN_ENG',
    }

  # 调用通用文字识别接口
  result = aipOcr.basicGeneral(image, options)
  return json.dumps(result,ensure_ascii=False)
  
while True:
  text = input('按下回车发起搜索')

  start = time.time()
  count = count+1
  imagepath = config.image_directory+"screen" + str(count) +".png"
  region_path = config.image_directory+"region" + str(count) +".png"

  if not os.path.exists(config.image_directory):
    os.mkdir(config.image_directory)
  os.system("adb shell /system/bin/screencap -p /sdcard/screenshot.png")
  os.system("adb pull /sdcard/screenshot.png " + imagepath)

  im = Image.open(imagepath)
  img_size = im.size
  w = im.size[0]
  h = im.size[1]

  region = im.crop((config.left, config.top, w - config.right, config.bottom))  # 裁剪的区域
  region.save(region_path)
  #选择图片
  f = open(region_path, 'rb')
  image_byte = f.read()
  f.close()
  
  content = get_words(image_byte)
    
  json_data = json.loads(content)

  # 输出文字
  keyword = ""
  for word in json_data["words_result"]:
    keyword = keyword + str(word["words"])
    
  print("OCR识别内容: " + keyword.split('.')[1])

  driver.find_element_by_id('kw').send_keys(Keys.CONTROL, 'a')
  driver.find_element_by_id('kw').send_keys(Keys.BACK_SPACE)
  driver.find_element_by_id('kw').send_keys(keyword)
  driver.find_element_by_id('su').send_keys(Keys.ENTER)

  end = time.time()
  print('程序用时：' + str(end - start) + '秒')
