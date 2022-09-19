from discord_webhook import DiscordWebhook,DiscordEmbed
from geopy.geocoders import Nominatim
from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from PIL import Image
from io import BytesIO
import requests,json,datetime,time
class ISSTrack(object):
    def __init__(self,url):
        self.url = url
    @staticmethod
    def webScrape(item):
        driver = webdriver.Firefox()
        driver.get("http://open-notify.org/Open-Notify-API/")
        element = driver.find_element_by_id(item)
        element.screenshot("/tmp/test.png")
        driver.quit()

    def postData(self):
        req = requests.get("http://api.open-notify.org/iss-now.json").json()
        astro_url = requests.get("http://api.open-notify.org/astros.json").json()
        time_stamp = req['timestamp']
        pos_lat = req['iss_position']['latitude']
        pos_long = req['iss_position']['longitude']
        num_people = astro_url['number']
        webhook = DiscordWebhook(url=self.url)
        embed = DiscordEmbed(title='ISS Tracker', color='1f61cc')
        embed.set_author(
    name="International Space Station",
    url="https://render.fineartamerica.com/images/rendered/default/print/8/6/break/images/artworkimages/medium/2/international-space-station-iss-scibak.jpg",
    icon_url="https://avatars.githubusercontent.com/u/71190959?v=4",
)
        embed.set_thumbnail(url="https://seeklogo.com/images/I/ISS-logo-B16A94899F-seeklogo.com.png")
        embed.add_embed_field(name='Latitude', value=pos_lat)
        embed.add_embed_field(name='Longitude', value=pos_long)
        embed.add_embed_field(name="Number of People",value=num_people)
        embed.add_embed_field(name="Astronaut#1", value=astro_url['people'][0]['name'])
        embed.add_embed_field(name="Astronaut#2", value=astro_url['people'][1]['name'])
        embed.add_embed_field(name="Astronaut#3", value=astro_url['people'][2]['name'])
        embed.add_embed_field(name="Astronaut#4", value=astro_url['people'][3]['name'])
        embed.add_embed_field(name="Astronaut#5", value=astro_url['people'][4]['name'])
        embed.set_footer(text=datetime.datetime.fromtimestamp(int(time_stamp))
      .strftime('%Y-%m-%d %H:%M:%S'), icon_url='https://cdn4.iconfinder.com/data/icons/devine_icons/Black/PNG/System%20and%20Internet/Times%20and%20Dates.png')
        with open("/tmp/test.png", "rb") as f:
            webhook.add_file(file=f.read(), filename='test.png')
        embed.set_image(url="attachment://test.png")
        webhook.add_embed(embed)
        response = webhook.execute()
if __name__ == "__main__":
    x = ISSTrack("https://discord.com/api/webhooks/1008171122778452088/uSndFq3RepbKTD77b7f9riRu76N4UhmRKlkQGpt5D-KISEcEoloyBR3UQq49nRl8RFrU")
    while True:
        x.webScrape("map")
        x.postData()
        time.sleep(5)

