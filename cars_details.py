import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
import time

def scrape_car_details(page_number, master_list):
    base_url = "https://www.glenmarch.com/cars/results?make=290&model=2016&auction_house_id=&auction_location=&year_start=2000&year_end=&low_price=&high_price=&auction_id=&fromDate=&toDate=&keywords=&only_online=0&show_unsold_cars=1&page="
    url = f"{base_url}{page_number}&sort=AuctionCars.finish_time&direction=desc"

    try:
        html = requests.get(url).text
        soup = bs(html, "html.parser")

        cars = soup.find_all("div", {"data-type": "car_grid_item"})

        for car in cars:
            car_brand = car.find("div", {"class": "make"}).text.split()[1]

            cm = car.find("div", {"class": "make"}).text.split()[2:]
            car_model = " ".join(cm)

            car_year = car.find("div", {"class": "make"}).text.split()[0]

            car_price = car.find("div", {"class": "price"}).text if car.find("div", {"class": "price"}) else ""

            auction_country = car.find("div", {"class": "auctionHouse"}).text.split()[-1] if car.find("div", {"class": "auctionHouse"}) else ""

            currency = car.find("div", {"class": "price"}).text.split()[0] if car.find("div", {"class": "price"}) else ""

            auction_year = car.find("div", {"class": "auctionHouse"}).next_sibling.text.split()[-1] if car.find("div", {"class": "auctionHouse"}) and car.find("div", {"class": "auctionHouse"}).next_sibling else ""

            car_info = {
                "Brand of Car": car_brand,
                "Model of car": car_model,
                "Year of Car": car_year,
                "Price sold (or unsold)": car_price,
                "Country  of auction": auction_country,
                "Currency": currency,
                "Year of Auction": auction_year
            }

            master_list.append(car_info)

    except requests.RequestException as e:
        print(f"Error on page {page_number}: {e}")

def main():
    master_list = []

    for page_number in range(1, 22):
        scrape_car_details(page_number, master_list)
        time.sleep(3)

    df = pd.DataFrame(master_list)
    df.to_csv("cars_details.csv", index=False)

if __name__ == "__main__":
    main()
