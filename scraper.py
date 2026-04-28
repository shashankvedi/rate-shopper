import json
import datetime

def get_rates():
    # Capture today's exact date
    today = str(datetime.date.today())
    
    # This is the simulated market data we will eventually pull from OTAs
    market_data = {
        "date_checked": today,
        "competitor_1": "₹2,500",
        "competitor_2": "₹2,800"
    }

    # Save this data into a JSON file so your dashboard can read it later
    with open('live_rates.json', 'w') as json_file:
        json.dump(market_data, json_file, indent=4)
        
    print(f"Rates successfully saved for {today}")

if __name__ == "__main__":
    get_rates()