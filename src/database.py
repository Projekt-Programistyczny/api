import os

from dotenv import load_dotenv

from sqlalchemy import create_engine, desc 
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from src.models.links import Link as ModelLink
from src.models.real_estates import RealEstates as ModelRealEstates

load_dotenv(f"{os.path.dirname(__file__)}/.env")

SQLALCHEMY_DATABASE_URL = os.environ["DATABASE_URI"]
engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def add_offers(list_of_offers) -> None:
    offers_to_save = []
    with SessionLocal() as db:
        for offer in list_of_offers:
            offers_to_save.append(ModelRealEstates(url = offer["url"],
                                    description = offer["description"],
                                    total_price = offer["total_price"],
                                    price = offer["price"],
                                    rent = offer["rent"],
                                    currency = offer["currency"],
                                    area = offer["area"],
                                    rooms = offer["rooms"],
                                    deposit = offer["deposit"],
                                    floor = offer["floor"],
                                    type = offer["type"],
                                    status = offer["status"],
                                    region = offer["region"],
                                    )
                                )
        db.add_all(offers_to_save)
        db.commit()


def set_link_as_used(url):
    with SessionLocal() as db:
        row = db.query(ModelLink).filter_by(url=url).first()
        row.used = True
        db.commit()
    

def select_unused_and_active_links(city: str):
    with SessionLocal() as db:
        links_details = db.query(ModelLink).filter_by(city_name=city,
                                                      used=False,
                                                      is_active=True).all()
        return links_details


def select_offers(city: str, type_of_offers: str, type_of_estate: str):
    with SessionLocal() as db:

        if city != "all" and type_of_offers != "all" and type_of_estate != "all":
            offers = db.query(ModelRealEstates).join(ModelLink, ModelLink.url == ModelRealEstates.url).\
                filter(ModelLink.city_name == city,
                       ModelLink.type_of_offer == type_of_offers,
                       ModelLink.type_of_estate == type_of_estate,
                       ModelLink.is_active == True)
        elif city != "all" and type_of_offers != "all" and type_of_estate == "all":
            offers = db.query(ModelRealEstates).join(ModelLink, ModelLink.url == ModelRealEstates.url).\
                filter(ModelLink.city_name == city,
                       ModelLink.type_of_offer == type_of_offers,
                       ModelLink.is_active == True)
        elif city != "all" and type_of_offers == "all" and type_of_estate == "all":
            offers = db.query(ModelRealEstates).join(ModelLink, ModelLink.url == ModelRealEstates.url).\
                filter(ModelLink.city_name == city,
                       ModelLink.is_active == True)
        elif city != "all" and type_of_offers == "all" and type_of_estate != "all":
            offers = db.query(ModelRealEstates).join(ModelLink, ModelLink.url == ModelRealEstates.url).\
                filter(ModelLink.city_name == city,
                       ModelLink.type_of_estate == type_of_estate,
                       ModelLink.is_active == True)
        elif city == "all" and type_of_offers == "all" and type_of_estate == "all":
            offers = db.query(ModelRealEstates).join(ModelLink, ModelLink.url == ModelRealEstates.url).\
                filter(ModelLink.is_active == True)
        elif city == "all" and type_of_offers == "all" and type_of_estate != "all":
            offers = db.query(ModelRealEstates).join(ModelLink, ModelLink.url == ModelRealEstates.url).\
                filter(ModelLink.type_of_estate == type_of_estate,
                       ModelLink.is_active == True)
        elif city == "all" and type_of_offers != "all" and type_of_estate == "all":
            offers = db.query(ModelRealEstates).join(ModelLink, ModelLink.url == ModelRealEstates.url).\
                filter(ModelLink.type_of_offer == type_of_offers,
                       ModelLink.is_active == True)
        elif city == "all" and type_of_offers != "all" and type_of_estate != "all":
            offers = db.query(ModelRealEstates).join(ModelLink, ModelLink.url == ModelRealEstates.url).\
                filter(ModelLink.type_of_estate == type_of_estate,
                       ModelLink.type_of_offer == type_of_offers,
                       ModelLink.is_active == True)
            
        i = 0
        results = []
        for data in offers:
            if data.description != "Failed":

                result = {"id":f"{i+1}", \
                            "city":f"{city}", \
                            "url":f"{data.url}", \
                            "description":f"{data.description}", \
                            "total_price":f"{data.total_price}", \
                            "price":f"{data.price}", \
                            "rent":f"{data.rent}", \
                            "currency":f"{data.currency}", \
                            "area":f"{data.area}", \
                            'rooms':f"{data.rooms}", \
                            "deposit":f"{data.deposit}", \
                            'floor':f"{data.floor}", \
                            "type":f"{data.type}", \
                            "status":f"{data.status}", \
                            "region":f"{data.region}"}
                results.append(result)
                i+=1

        # Sort here


        return results
    

def select_offer_details(url: str):
    with SessionLocal() as db:

        link_detail  = db.query(ModelLink).filter_by(url=url).first()
        offer_detail = db.query(ModelRealEstates).filter_by(url=url).first()
        
        result = {  "city":f"{link_detail.city_name}", \
                    "type_of_estate":f"{link_detail.type_of_estate}", \
                    "type_of_offer":f"{link_detail.type_of_offer}", \
                    "url":f"{offer_detail.url}", \
                    "description":f"{offer_detail.description}", \
                    "total_price":f"{offer_detail.total_price}", \
                    "price":f"{offer_detail.price}", \
                    "rent":f"{offer_detail.rent}", \
                    "currency":f"{offer_detail.currency}", \
                    "area":f"{offer_detail.area}", \
                    'rooms':f"{offer_detail.rooms}", \
                    "deposit":f"{offer_detail.deposit}", \
                    'floor':f"{offer_detail.floor}", \
                    "type":f"{offer_detail.type}", \
                    "status":f"{offer_detail.status}", \
                    "region":f"{offer_detail.region}"}


        return result