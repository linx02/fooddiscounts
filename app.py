from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from scrapers import IcaScraper, WillysScraper, LidlScraper
from classes import OfferList

app = Flask(__name__)
CORS(app, origins=['http://localhost:3000'])

ica_scraper = IcaScraper()
willys_scraper = WillysScraper()
lidl_scraper = LidlScraper()

@app.route('/api', methods=['GET'])
def get_offers():
    ica_soder_offers = ica_scraper.scrape('ica-soder-gavle-1004132')
    ica_fjallbacken_offers = ica_scraper.scrape('ica-kvantum-fjallbacken-1004178')
    ica_maxi_offers = ica_scraper.scrape('maxi-ica-stormarknad-gavle-1003987')
    willys_offers = willys_scraper.scrape()
    lidl_offers = lidl_scraper.scrape()
    
    return jsonify({
        'ica_soder': {'offers': ica_soder_offers.to_list(), 'statistics': statistics(ica_soder_offers)},
        'ica_fjallbacken': {'offers': ica_fjallbacken_offers.to_list(), 'statistics': statistics(ica_fjallbacken_offers)},
        'ica_maxi': {'offers': ica_maxi_offers.to_list(), 'statistics': statistics(ica_maxi_offers)},
        'willys': {'offers': willys_offers.to_list(), 'statistics': statistics(willys_offers)},
        'lidl': {'offers': lidl_offers.to_list(), 'statistics': statistics(lidl_offers)}
    })

def statistics(offer_list):
    return {
        'median_savings_kr': offer_list.median_savings()[0],
        'median_savings_percent': offer_list.median_savings()[1],
        'median_price': offer_list.median_price(),
        'total_offers': len(offer_list)
    }

if __name__ == '__main__':
    app.run(debug=False, port=5000, host='0.0.0.0')