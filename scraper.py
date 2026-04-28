import os
import json
import datetime
from bs4 import BeautifulSoup
from scraperapi_sdk import ScraperAPIClient
from dotenv import load_dotenv

# 1. Load the hidden .env file locally
load_dotenv()

# 2. Grab the API key securely from the environment
API_KEY = os.getenv('SCRAPER_API_KEY')

# Safety check: ensure the API key was actually loaded
if not API_KEY:
    print("❌ ERROR: API key not found. Make sure your .env file exists and contains SCRAPER_API_KEY=your_key")
    exit()

client = ScraperAPIClient(API_KEY)

def get_real_price(base_url, checkin, checkout):
    # Construct the clean, dynamic URL
    full_url = f"{base_url}?checkin={checkin}&checkout={checkout}"
    print(f"Scraping: {full_url[:60]}...") 
    
    try:
        response = client.get(url=full_url, render=True)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Target the specific price tag Booking.com uses
        price_element = soup.find("span", {"data-testid": "price-and-discounted-price"})
        
        if price_element:
            return price_element.text.strip()
        return "Price tag not found"
        
    except Exception as e:
        return f"API Error: {str(e)}"

def get_rates():
    # Calculate today and tomorrow dynamically
    today = datetime.date.today()
    tomorrow = today + datetime.timedelta(days=1)
    
    print(f"--- Starting Daily Rate Shopper for {today} ---")
    
    # Your clean Base URLs without the tracking junk
    properties = {
        "Luxuria by Moustache (Ours)": "https://www.booking.com/hotel/in/luxuria-varanasi-by-moustache.html",
        "Coco Cabana": "https://www.booking.com/hotel/in/coco-cabana-varanasi.html",
        "Quality Inn City Centre": "https://www.booking.com/hotel/in/quality-inn-city-centre-varanasi.html",
        "Minimalist The Varanasi Edit": "https://www.booking.com/hotel/in/minimalist-the-varanasi-edit.html"
    }
    
    market_data = {
        "date_checked": str(today),
        "checkin_date": str(today),
        "checkout_date": str(tomorrow),
        "rates": {}
    }

    # Loop through each property and fetch the live price
    for name, url in properties.items():
        price = get_real_price(url, today, tomorrow)
        market_data["rates"][name] = price
        print(f"-> {name}: {price}")

    # Save all the real data into your JSON file
    with open('live_rates.json', 'w') as json_file:
        json.dump(market_data, json_file, indent=4)
        
    print(f"\n✅ Live rates successfully saved to live_rates.json")

if __name__ == "__main__":
    get_rates()