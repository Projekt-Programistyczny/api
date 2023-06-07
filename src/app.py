from database import select_offer_details, select_offers
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import uvicorn
import os

app = FastAPI()
templates = Jinja2Templates(directory=f"{os.path.dirname(__file__)}/templates")
app.mount("/static", StaticFiles(directory=f"{os.path.dirname(__file__)}/templates/static"), name="static")


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
    return templates.TemplateResponse("index.html", {"request": request, "cities": cities})



@app.get("/offers", response_class=JSONResponse)
def get_oferty_mieszkan(city: str = "all", type_of_offer: str = "all", type_of_estate: str ="all", sort_by: str = "Default"):
    if city:
        print(city)
        print(type(city))
        print(type_of_offer)
        print(type(type_of_offer))
        print(type_of_estate)
        print(type(type_of_estate))
        # if city == "all":
        #     print(city)
        #     print(type(city))
        # else:
        print(select_offers(city, type_of_offer, type_of_estate))
    else:
        return 


@app.get("/offer_detail", response_class=JSONResponse)
def get_offer_details(url: str = None):
    if url:
        return select_offer_details(url)
    else:
        return 


if __name__ == '__main__':
    uvicorn.run("app:app", host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))