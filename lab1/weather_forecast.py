from VirtualCopernicusNG import TkCircuit

# initialize the circuit inside the

configuration = {
    "name": "CopernicusNG Weather Forecast",
    "sheet": "sheet_forecast.png",
    "width": 343,
    "height": 267,

    "servos": [
        {"x": 170, "y": 150, "length": 90, "name": "Servo 1", "pin": 17}
    ],
    "buttons": [
        {"x": 295, "y": 200, "name": "Button 1", "pin": 11},
        {"x": 295, "y": 170, "name": "Button 2", "pin": 12},
    ]
}

circuit = TkCircuit(configuration)


def get_angle(weather):
    if weather.status != "Clouds":
        return weather_map[weather.status] * 20
    else:
        return clouds_map[weather.detailed_status] * 20


def change_city():
    global count
    count += 1
    city = cities[count % len(cities)]

    from pyowm.owm import OWM
    weather = OWM('4526d487f12ef78b82b7a7d113faea64').weather_manager().weather_at_place(city).weather

    print(f"Current city: {city}")
    print(weather.detailed_status, "\n")

    servo.angle = get_angle(weather)


@circuit.run
def main():
    from gpiozero import AngularServo, Button
    from time import sleep

    global weather_map
    weather_map = {
        "Clear": 1,
        "Clouds": 5,
        "Drizzle": 6,
        "Rain": 7,
        "Thunderstorm": 7,
        "Snow": 7,
        "Mist": 6,
        "Smoke": 5,
        "Haze": 5,
        "Dust": 5,
        "Fog": 6,
        "Sand": 5,
        "Ash": 5,
        "Squall": 7,
        "Tornado": 8
    }

    global clouds_map
    clouds_map = {
        "few clouds": 2,
        "scattered clouds": 3,
        "broken clouds": 4,
        "overcast clouds": 5
    }

    global cities
    cities = [
        'Krakow,PL', 'Istanbul,TR', 'Stockholm,SE', 'Glasgow,GB'
    ]

    global servo
    servo = AngularServo(17, min_angle=0, max_angle=180)

    global count
    count = -1
    button = Button(11)
    button.when_pressed = change_city

    while True:
        sleep(1)
