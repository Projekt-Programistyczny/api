from src.database import select_offer_details, select_offers
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import uvicorn
import yaml
import os

app = FastAPI()
templates = Jinja2Templates(directory=f"{os.path.dirname(__file__)}/src/templates")
app.mount("/static", StaticFiles(directory=f"{os.path.dirname(__file__)}/src/templates/static"), name="static")


with open(f"{os.path.dirname(__file__)}/src/cities.yaml", 'r') as f:
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
def get_offers(city: str="all", type_of_offer: str="all", type_of_estate: str ="all", sort_by: str="default", category: int=0):
    # Below debug part :) 
    # print(city)
    # print(type(city))
    # print(type_of_offer)
    # print(type(type_of_offer))
    # print(type_of_estate)
    # print(type(type_of_estate))
    # print(category)
    # print(type(category))
    return select_offers(city, type_of_offer, type_of_estate, sort_by, category)


@app.get("/offer_detail", response_class=JSONResponse)
def get_offer_details(url: str = None):
    return select_offer_details(url)



# if __name__ == '__main__':
#     uvicorn.run("main:app", host='0.0.0.0', port=int(os.environ.get("PORT", 8080)))