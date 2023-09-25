from CsFloatScraper import CsFloatScraper
from ItemInfo import ItemInfo
import time, random, json, urllib.parse, requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

# get_items_api_url = 'http://csgobackpack.net/api/GetItemsList/v2/'

# response = requests.get(get_items_api_url)

# data = response.json()

# all_csgo_skins = list(data['items_list'].keys())
CS_FLOAT_CHECKER_URL = 'https://csfloat.com/checker'
moonrise_skin = 'Glock-18 | Moonrise (Minimal Wear)'
moonrise_decoded = urllib.parse.quote(moonrise_skin)
start = 0
NUMERO_ITEMS_POR_PAGINA = 100
NUMERO_ITEMS_A_PEGAR_INFO = 400
NUMERO_PAGINAS_DEFINIDOS_PELO_PADUA = int(NUMERO_ITEMS_A_PEGAR_INFO/NUMERO_ITEMS_POR_PAGINA)
DOLLAR_PRICE_BY_INDIGENA = 4.92
anuncions_moonrise_url = 'https://steamcommunity.com/market/listings/730/' + moonrise_decoded  +'/render/?query=&start='+ str(start) +'&count='+ str(NUMERO_ITEMS_POR_PAGINA) +'&country=BR&language=brazilian&currency=7&format=json'
items_info = {}
SERVICE = Service(executable_path=r"D:\caiom\Documents\chromedriver-win64\chromedriver.exe")
OPTIONS = webdriver.ChromeOptions()
OPTIONS.add_argument('--headless')
DRIVER = webdriver.Chrome(service=SERVICE, options=OPTIONS)

def get_preco(value):
    return ((value['converted_price'] + value['converted_fee'])*DOLLAR_PRICE_BY_INDIGENA)/100

def fill_lista_items_info(data, items_info, pagina):
    if data != None:
        for id_anuncio, info_anuncio in data['listinginfo'].items():
            item_info = ItemInfo() #ItemInfo itemInfo = new ItemInfo()

            asset_id = info_anuncio['asset']['id']


            inspect_game_url = get_inspect_game_url(id_anuncio, info_anuncio, asset_id)
            item_info.inspect_url = inspect_game_url
            item_info.page = pagina + 1
            item_info.preco = get_preco(info_anuncio)
            item_info.anuncio_id = id_anuncio
            items_info[id_anuncio] = item_info
            print("Adicionei o anuncio " + str(id_anuncio))
            time.sleep(1 + random.random())
            print("Vou para o Próximo Anúncio")

def get_inspect_game_url(id_anuncio, info_anuncio, asset_id):
    inspect_game_url = info_anuncio['asset']['market_actions'][0]['link']
    inspect_game_url = inspect_game_url.replace('%listingid%', id_anuncio)
    inspect_game_url = inspect_game_url.replace('%assetid%', asset_id)
    return inspect_game_url

for pagina in range(NUMERO_PAGINAS_DEFINIDOS_PELO_PADUA):
    response = requests.get(anuncions_moonrise_url)
    data = response.json()
    fill_lista_items_info(data, items_info, pagina)
    time.sleep(90)
    start += NUMERO_ITEMS_POR_PAGINA
        
DRIVER.get(CS_FLOAT_CHECKER_URL)
for id_anuncio, item in items_info.items():
    scraper = CsFloatScraper()
    scraper.get_item_info(item, DRIVER)

print(items_info)

with open("GlockMoonriseMinimalWear.json", 'w') as file:
    json.dump(items_info, file)
