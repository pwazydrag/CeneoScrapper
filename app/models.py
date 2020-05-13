import textwrap
import requests
from bs4 import BeautifulSoup

class Product:
    def __init__(self, product_id = None, name = None, opinions = []):
        self.product_id = product_id
        self.name = name
        self.opinions = opinions
    def __str__(self):
        return f"Product id: {self.product_id}\nName: {self.name}\nOpinions:\n"+"\n".join(textwrap.indent(str(opinion), "    ") for opinion in self.opinions)
    def __repr__(self):
        pass
    def extract_product(self):
        url_prefix="https://www.ceneo.pl"
        url_postfix = "#tab=reviews"
        url =  url_prefix + "/" + self.product_id + url_postfix
        page_respons = requests.get(url)
        page_tree = BeautifulSoup(page_respons.text, 'html.parser')
        self.name = page_tree.find("h1","product-name").get_text().strip()
        try:
            opinions_count = int(page_tree.find("a","product-reviews-link").find("span").get_text().strip())
        except AttributeError:
            opinions_count = 0
        if opinions_count>0:
            while url:
                #pobranie kodu html strony z podanego URL
                page_respons = requests.get(url)
                page_tree = BeautifulSoup(page_respons.text, 'html.parser')

                #wydobycie z kodu HTML strony fragmentów odpowiadających poszczególnym opisom
                opinions = page_tree.find_all("li", "js_product-review")

                #wydobycie składowych dla pojedynczych opinii
                for opinion in opinions:
                    op = Opinion()
                    op.extract_opinion(opinion)
                    op.transform_opinion
                    self.opinions.append(op)

                    try:
                        url = url_prefix+page_tree.find("a", "pagination__next")["href"]
                    except TypeError:
                        url = None

class Opinion:
    #słownik z składowymi opinii i ich selektorami
    tags = {
        "recommendation":["div", "product-review-summary", "em" ],
        "stars":["span", "review-score-count"],
        "content":["p","product-review-body"],
        "author":["div", "reviewer-name-line"],
        "pros":["div", "pros-cell", "ul"],
        "cons":["div", "cons-cell", "ul"],
        "useful":["button", "vote-yes", "span"],
        "useless":["button", "vote-no", "span"],
        "purchased":["div", "product-review-pz", "em"]
    }
    #funkcja do ekstrakcji składowych opinii
    def extract_feature(opinion, tag, tag_class, child=None):
        try:
            if child:
                return opinion.find(tag, tag_class).find(child).get_text().strip()
            else:
                return opinion.find(tag, tag_class).get_text().strip()
        except AttributeError:
            return None

    #definicja instruktora (inicjalizatora) klasy
    def __init__(self, opinion_id=None, author=None, recommendation=None, stars=None, content=None, pros=None, cons=None, useful=None, useless=None, purchased=None, purchase_date=None, review_date=None):
        self.opinion_id = opinion_id
        self.author = author
        self.recommendation = recommendation
        self.stars = stars
        self.content = content
        self.pros = pros
        self.cons = cons
        self.useful = useful
        self.useless = useless
        self.purchased = purchased
        self.purchase_date = purchase_date
        self.review_date = review_date
    def __str__(self):
        return f"Opinion id: {self.opinion_id}\nAuthor: {self.author}\nStars: {self.stars}\n"
    def extract_opinion(self, opinion):
        for key, args in self.tags:
            setattr(self, key, extract_feature(opinion, *args))
        self.opinion_id = int(opinion["data-entry-id"]
        dates = opinion.find("span", "review-time").find_all("time")
        features["review_date"] = dates.pop(0)["datetime"]

        features = {key:extract_feature(opinion, *args)
        for key, args in tags.items()}
                    
        features["opinion_id"] = int(opinion["data-entry-id"])

        try:
            features["purchase_date"] = dates.pop(0)["datetime"]
        except IndexError:
            features["purchase_date"] = None

    def transform_opinion(self):
        features["purchased"] = (features["purchased"]=="Opinia potwierdzona zakupem")
        features["useful"] = int(features["useful"])
        features["useless"] = int(features["useless"])
        features["content"] = remove_whitespaces(features["content"])
        features["pros"] = remove_whitespaces(features["pros"])
        features["cons"] = remove_whitespaces(features["cons"])



opinion = Opinion()
product = Product("84507187")