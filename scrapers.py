from classes import Offer, OfferList
import requests
import json
import re

class IcaScraper:
    def scrape(self, store_slug) -> OfferList:
        url = f'https://ica.se/erbjudanden/{store_slug}/'
        res = requests.get(url)

        pattern = r'"details":\s*(\{[^{}]*\})'
        pattern2 = r'"stores"\s*:\s*\[(\{(?:[^{}]|\{[^{}]*\}|[^{}\[\]]*)+\})\]'
        pattern3 = r'"picture":\s*(\{[^{}]*\})'

        # Find all occurrences in the text
        matches = re.findall(pattern, res.text)
        matches2 = re.findall(pattern2, res.text)
        matches3 = re.findall(pattern3, res.text)

        if not len(matches) == len(matches2) == len(matches3):
            print('Error: Number of matches do not match')
            return

        # Convert JavaScript objects to Python dictionaries
        python_dicts = []
        python_dicts2 = []
        pictures = [eval(match, {"__builtins__": None}, {}) for match in matches3]
        for match, match2 in zip(matches, matches2):
            # Replace JavaScript boolean and null with Python equivalents
            python_code = match.replace('false', 'False').replace('true', 'True').replace('null', 'None')
            python_code2 = match2.replace('false', 'False').replace('true', 'True').replace('null', 'None')

            try:
                # Safely evaluate the string as a Python dictionary
                python_dict = eval(python_code, {"__builtins__": None}, {})
                python_dict2 = eval(python_code2, {"__builtins__": None}, {})
                python_dicts.append(python_dict)
                python_dicts2.append(python_dict2)
            except Exception as e:
                print(f"Error evaluating Python code: {e} in {match[:100]}...")

        offer_list = OfferList('Ica')
        for i, offer_data in enumerate(python_dicts):

            old_price = python_dicts2[i]['regularPriceTo']

            if 'betala för' in offer_data['mechanicInfo']:
                min_quantity = int(offer_data['mechanicInfo'].split(' betala')[0].split('Köp ')[1])
                unit_price = int(offer_data['mechanicInfo'].split('för ')[1]) * old_price / min_quantity
            elif '/st' in offer_data['mechanicInfo'] or '/kg' in offer_data['mechanicInfo'] or '/hg' in offer_data['mechanicInfo'] or '/förp' in offer_data['mechanicInfo']:
                min_quantity = 1
                unit_price = float(offer_data['mechanicInfo'].split(' kr')[0].replace(',', '.'))
            elif 'för' in offer_data['mechanicInfo']:
                min_quantity = int(offer_data['mechanicInfo'].split(' för ')[0])
                unit_price = float(offer_data['mechanicInfo'].split(' för ')[1].replace(' kr', '').replace(',', '.')) / min_quantity
            elif '+pant' in offer_data['mechanicInfo']:
                min_quantity = 1
                unit_price = float(offer_data['mechanicInfo'].split(' kr')[0].replace(',', '.'))
            elif 'Rabatt' in offer_data['mechanicInfo']:
                min_quantity = 1
                unit_price = old_price - float(offer_data['mechanicInfo'].split(' ')[1]) / 100 * old_price
            else:
                min_quantity = 1
                unit_price = 0
                print(f"Error: Could not parse offer: {offer_data['mechanicInfo']}")

            offer = Offer(
                f'{offer_data['name']} - {offer_data['brand']} - {offer_data['packageInformation']}',
                unit_price,
                old_price,
                pictures[i]['url'],
                min_quantity
            )
            offer_list.offers.append(offer)

        return offer_list

class WillysScraper:
    def scrape(self) -> OfferList:
        res = requests.get('https://willys.se/search/campaigns/online?q=2110&type=PERSONAL_GENERAL&page=0&size=1').json()
        num_offers = res['pagination']['totalNumberOfResults']
        res = requests.get(f'https://willys.se/search/campaigns/online?q=2110&type=PERSONAL_GENERAL&page=0&size={num_offers}').json()
        offer_list = OfferList('Willys')
        for offer_data in res['results']:
            offer = Offer(
                offer_data['name'],
                offer_data['priceValue'] - offer_data['savingsAmount'],
                offer_data['priceValue'],
                offer_data['thumbnail']['url'],
                offer_data['potentialPromotions'][0]['qualifyingCount'] if offer_data['potentialPromotions'][0]['qualifyingCount'] else 1
                )
            offer_list.offers.append(offer)

        return offer_list


class LidlScraper:
    def scrape(self) -> OfferList:
        # Scrape the website
        url="https://lidl.se/c/mandag-soendag/a10053163?tabCode=Current_Sales_Week"
        res = requests.get(url)
        # Find all occurrences in the text
        pattern = r'productid="\d+"'
        matches = re.findall(pattern, res.text)
        # Extract product ids
        product_ids = [int(match.split('"')[1]) for match in matches]
        # Get unique product ids
        product_ids = list(set(product_ids))

        urls = [f"https://lidl.se/p/api/detail/{id}/SE/sv" for id in product_ids]
        offer_list = OfferList('Lidl')

        for url in urls:
            res = requests.get(url).json()
            image_key = list(res['media']['imageMap'])
            image_key = image_key[0]
            offer = Offer(
                res['keyfacts']['title'],
                res['price']['price'],
                res['price']['price'],
                res['media']['imageMap'][image_key]['largeUrl'],
                res['stockAvailability']['minOrderableQuantity'],
            )
            offer_list.offers.append(offer)

        return offer_list