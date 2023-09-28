from CsFloatScraper import CsFloatScraper
from ItemInfo import ItemInfo
import time, random, json, urllib.parse, requests

# get_items_api_url = 'http://csgobackpack.net/api/GetItemsList/v2/'

# response = requests.get(get_items_api_url)

# data = response.json()

# all_csgo_skins = list(data['items_list'].keys())

moonrise_skin = 'Glock-18 | Moonrise (Minimal Wear)'
moonrise_decoded = urllib.parse.quote(moonrise_skin)
start = 0
NUMERO_ITEMS_POR_PAGINA = 100
NUMERO_ITEMS_A_PEGAR_INFO = 400
NUMERO_PAGINAS_DEFINIDOS_PELO_PADUA = int(NUMERO_ITEMS_A_PEGAR_INFO/NUMERO_ITEMS_POR_PAGINA)
DOLLAR_PRICE_BY_INDIGENA = 4.92
anuncions_moonrise_url = 'https://steamcommunity.com/market/listings/730/' + moonrise_decoded  +'/render/?query=&start='+ str(start) +'&count='+ str(NUMERO_ITEMS_POR_PAGINA) +'&country=BR&language=brazilian&currency=7&format=json'
items_info = {}
items = {}

def get_preco(value):
    return ((value['converted_price'] + value['converted_fee']))/100

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

def get_inspect_game_url(id_anuncio, info_anuncio, asset_id):
    inspect_game_url = info_anuncio['asset']['market_actions'][0]['link']
    inspect_game_url = inspect_game_url.replace('%listingid%', id_anuncio)
    inspect_game_url = inspect_game_url.replace('%assetid%', asset_id)
    return inspect_game_url

def preenche_info_anuncios(anuncions_moonrise_url, items_info, pagina):
    response = requests.get(anuncions_moonrise_url)
    if response.status_code == 200:
        salva_novos_anuncios(response.json(), pagina)
    
    data = get_anuncios_salvos_json(pagina)
    fill_lista_items_info(data, items_info, pagina)

def salva_novos_anuncios(anuncios_salvos, pagina):
    with open ("GlockMoonriseMinimalWearAnuncios" + str(pagina) + ".json", 'w') as file:
        json.dump(anuncios_salvos, file)

def get_anuncios_salvos_json(pagina):
    with open ("GlockMoonriseMinimalWearAnuncios" + str(pagina) + ".json", 'r') as file:
        anuncios_json = json.load(file)
    return anuncios_json

def preenche_info_cs_float_api_about_item(items_info):
    for id_anuncio, item in items_info.items():
        scraper = CsFloatScraper()
        scraper.get_item_info(item)     

for pagina in range(1, NUMERO_PAGINAS_DEFINIDOS_PELO_PADUA):
    preenche_info_anuncios(anuncions_moonrise_url, items_info, pagina)
    start += NUMERO_ITEMS_POR_PAGINA
    preenche_info_cs_float_api_about_item(items_info)
    
    items["Pagina " + pagina] = items_info

    with open("GlockMoonriseMinimalWearInfo.json", "w") as file:
        json.dump(item_info_json, file)

    items_info.clear()
    time.sleep(300)
        
