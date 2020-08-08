# bot.py
import os, discord, html, requests,re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

TOKEN = os.environ.get('DISCORD')
client = discord.Client()


fireFoxOptions = webdriver.FirefoxOptions()
fireFoxOptions.set_headless()  # Last I checked this was necessary.
driver = webdriver.Firefox(firefox_options=fireFoxOptions)


@client.event
async def on_ready():
    print(f'{client.user.name} has connected to Discord!')

@client.event
async def on_message(message):
    if message.author == client.user:
        return


    if message.content[0:3] == '!tb':
        content = getData(message.content[4::])
        embed=discord.Embed(title=content[2], url=content[3])
        embed.set_author(name=content[1])
        embed.set_thumbnail(url=content[0])
        await message.channel.send(embed=embed)
        

def getData(request):
    request = request.replace(" ","+")
    request = request.replace ("#","%23")
    request = html.escape(request)
    URL = f'https://libgen.lc/search.php?req={request}&lg_topic=libgen&open=0&view=simple&res=25&phrase=1&column=def'
    driver.get(URL)
    while True:
        try:
            elem = driver.find_elements_by_tag_name("table")[3].find_elements_by_tag_name("tr")[1].find_elements_by_xpath(".//*")
            break
        except:
            print("CANT FIND")
            continue
    for i in elem:
        print(i.text)
    bookAuthor = elem[1].text
    bookTitle = elem[3].text
    link = elem[3].find_element_by_xpath("//a[string-length(@id)>0]").get_attribute("href")
    linkEnding = link[37:]
    driver.get(f"https://libgen.lc/ads.php?md5={linkEnding}")
    downloadLink = driver.find_element_by_xpath('//td[2]').find_element_by_tag_name('a').get_attribute("href")
    textBookImg = driver.find_element_by_xpath('//img[1]').get_attribute("src")
    returnArray = [textBookImg,bookAuthor,bookTitle,downloadLink]
    return(returnArray)
    

client.run(TOKEN)