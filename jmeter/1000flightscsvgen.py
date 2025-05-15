import random
import csv
from datetime import datetime, timedelta

# === PASTE ALL YOUR AIRLINE UIDS HERE ===
AIRLINE_UIDS = [
    "6823a7ed17be1b0f5750c153",  # Emirates
    "6823a7fb17be1b0f5750c156",
    "68254481f0a705d6efbfb919",  # Singapore Airlines
    "68254481f0a705d6efbfb91b",  # Air France
    "68254481f0a705d6efbfb91d",
    "68254481f0a705d6efbfb91f",
    "68254481f0a705d6efbfb921",
    "68254481f0a705d6efbfb923",
    "68254481f0a705d6efbfb925",
    "68254481f0a705d6efbfb927",
]

# If you have more, keep adding!

# === LIST OF CITIES FOR REALISTIC FLIGHT DATA ===
CITIES = [
    "New York", "London", "Paris", "Tokyo", "Dubai", "Singapore",
    "Los Angeles", "Sydney", "Berlin", "Toronto", "Mumbai", "Beijing",
    "Rome", "Bangkok", "Moscow", "Chicago", "Madrid", "Seoul", "San Francisco", "Melbourne"
]

# === DATE RANGE FOR FLIGHTS ===
DATE_RANGE_START = datetime(2025, 5, 16)
DATE_RANGE_END = datetime(2025, 7, 30)

# === HELPER FUNCTIONS ===
def random_date(start, end):
    """Generate a random date between start and end"""
    return start + timedelta(
        seconds=random.randint(0, int((end - start).total_seconds()))
    )

def random_time():
    """Generate a random time in HH:mm format"""
    hour = random.randint(0, 23)
    minute = random.randint(0, 59)
    return f"{hour:02d}:{minute:02d}"

def random_price():
    """Generate a realistic flight price"""
    return round(random.uniform(100, 1500), 2)

# === MAIN SCRIPT ===
with open('flights.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    
    # Write header
    writer.writerow([
        "from", "to", "departDate", "arriveDate", 
        "departTime", "arriveTime", "airlineUid", "price"
    ])

    # Generate 1000 flights
    for _ in range(1000):
        from_city = random.choice(CITIES)
        to_city = random.choice([city for city in CITIES if city != from_city])
        
        depart_date = random_date(DATE_RANGE_START, DATE_RANGE_END)
        arrive_date = depart_date + timedelta(days=random.randint(0, 3))
        
        depart_time = random_time()
        arrive_time = random_time()

        airline_uid = random.choice(AIRLINE_UIDS)
        price = random_price()

        # Format dates as strings
        depart_date_str = depart_date.strftime('%Y-%m-%d')
        arrive_date_str = arrive_date.strftime('%Y-%m-%d')

        # Write row
        writer.writerow([
            from_city, to_city,
            depart_date_str, arrive_date_str,
            depart_time, arrive_time,
            airline_uid, price
        ])

print("✅ Generated flights.csv with 1000 flights using all airline UIDs.")