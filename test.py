import json

with open('flight_data.json', 'r') as f:
    flights = json.load(f)['flights']

cheap_flights = [flight for flight in flights if int(flight['price'][1:]) < 100]

for flight in cheap_flights:
    print(flight)

with open('flight_KRK.json', 'r') as z:
    flights = json.load(z)['flights']

    print(len(flights))


