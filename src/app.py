from src.database import select_offer_details, select_offers
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import uvicorn
import yaml
import os

app = FastAPI()
templates = Jinja2Templates(directory=f"{os.path.dirname(__file__)}/templates")
app.mount("/static", StaticFiles(directory=f"{os.path.dirname(__file__)}/templates/static"), name="static")


with open(f"{os.path.dirname(__file__)}/cities.yaml", 'r') as f:
    cities_yaml = yaml.safe_load(f)

CITY_TO_EXPLORE = cities_yaml["region"]["cities"]


oferty = [
    {
        "city": "Failed",
        "description": "Failed",
        "total_price": "Failed",
        "price": "Failed",
        "rent": "Failed",
        "area": "Failed",
        "rooms": "Failed",
        "deposit": "Failed",
        "floor": "Failed",
        "type": "Failed",
        "status": "Failed"
        }
]

@app.get("/", response_class=HTMLResponse)
def get_homepage(request: Request):
    cities = ['katowice','tychy', 'sosnowiec']
    return templates.TemplateResponse("index.html", {"request": request, "cities": CITY_TO_EXPLORE})



@app.get("/offers", response_class=JSONResponse)
def get_offers(city: str = "all", type_of_offer: str = "all", type_of_estate: str ="all", sort_by: str = "Default"):
    print(city)
    print(type(city))
    print(type_of_offer)
    print(type(type_of_offer))
    print(type_of_estate)
    print(type(type_of_estate))

    return select_offers(city, type_of_offer, type_of_estate)

    return [{  "city":f"katowice", \
                "type_of_estate":f"test", \
                "type_of_offer":f"test", \
                "url":f"https://test.html", \
                "description":f"test", \
                "total_price":f"934883", \
                "price":f"4235435", \
                "rent":f"23423453", \
                "currency":f"zł", \
                "area":f"54", \
                'rooms':f"2", \
                "deposit":f"-1", \
                'floor':f"3", \
                "type":f"test", \
                "status":f"test", \
                "region":f"test"},
                {  "city":f"katowice", \
                "type_of_estate":f"test", \
                "type_of_offer":f"test", \
                "url":f"https://test.html", \
                "description":f"test", \
                "total_price":f"934883", \
                "price":f"4235435", \
                "rent":f"23423453", \
                "currency":f"zł", \
                "area":f"54", \
                'rooms':f"2", \
                "deposit":f"-1", \
                'floor':f"3", \
                "type":f"test", \
                "status":f"test", \
                "region":f"test"}]


@app.get("/offer_detail", response_class=JSONResponse)
def get_offer_details(url: str = None):
    return select_offer_details(url)
    # return {  "city":f"katowice", \
    #             "type_of_estate":f"test", \
    #             "type_of_offer":f"test", \
    #             "url":f"https://test.html", \
    #             "description":f"testsadfasf asdfr edsw fdsaf aefsda efwesdaf", \
    #             "total_price":f"934883", \
    #             "price":f"4235435", \
    #             "rent":f"23423453", \
    #             "currency":f"zł", \
    #             "area":f"54", \
    #             'rooms':f"2", \
    #             "deposit":f"-1", \
    #             'floor':f"3", \
    #             "type":f"test", \
    #             "status":f"test", \
    #             "region":f"test"},




# if __name__ == '__main__':
#     uvicorn.run("app:app", host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))