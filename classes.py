class OfferList:
    def __init__(self, store_name):
        self.offers = []
        self.store_name = store_name

    def median_savings(self) -> tuple:
        savings = [offer.savings for offer in self.offers if offer.savings]
        percent_savings = [offer.percent_savings for offer in self.offers if offer.percent_savings]
        return sum(savings) / len(savings), sum(percent_savings) / len(percent_savings)
    
    def median_price(self) -> float:
        prices = [offer.price for offer in self.offers]
        return sum(prices) / len(prices)

    def best_offers(self, n=None) -> list:
        n = n if n else len(self.offers)
        filtered_offers = [offer for offer in self.offers if offer.savings]
        return sorted(filtered_offers, key=lambda x: x.savings, reverse=True)[:n]

    def __len__(self):
        return len(self.offers)

    def __getitem__(self, index):
        return self.offers[index]

    def __iter__(self):
        return iter(self.offers)

    def __str__(self):
        return f"OfferList: {self.offers}"

    def to_list(self):
        return [offer.to_dict() for offer in self.best_offers()]

class Offer:
    def __init__(self, name, price, old_price=None, image=None, min_quantity=None):
        self.name = name
        self.price = price
        self.old_price = old_price
        self.image = image
        self.savings = old_price - price if old_price else None
        self.percent_savings = (self.savings / old_price) * 100 if old_price else None
        self.min_quantity = min_quantity

    def __str__(self):
        return f"Offer: {self.name} - {self.price}"

    def to_dict(self):
        return {
            'name': self.name,
            'price': self.price,
            'old_price': self.old_price,
            'image': self.image,
            'savings': self.savings,
            'percent_savings': self.percent_savings,
            'min_quantity': self.min_quantity
        }