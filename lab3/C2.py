from VirtualCopernicusNG import TkCircuit

# initialize the circuit inside the

configuration = {
    "name": "C2",
    "sheet": "sheet_smarthouse.png",
    "width": 332,
    "height": 300,
    "leds": [
        {"x": 112, "y": 70, "name": "LED 1", "pin": 21},
        {"x": 71, "y": 141, "name": "LED 2", "pin": 22}
    ],
    "buttons": [
        {"x": 242, "y": 146, "name": "Button 1", "pin": 11},
        {"x": 200, "y": 217, "name": "Button 2", "pin": 12},
    ]
}

circuit = TkCircuit(configuration)


@circuit.run
def main():
    # now just write the code you would use on a real Raspberry Pi

    from gpiozero import LED, Button
    import paho.mqtt.client as mqtt

    def button1_pressed():
        led1.toggle()

    def button2_pressed():
        mqttc.publish("xeno/zone1", "OFF", 0, False)

    led1 = LED(21)

    button1 = Button(11)
    button1.when_pressed = button1_pressed

    button2 = Button(12)
    button2.when_pressed = button2_pressed

    # The callback for when the client receives a CONNACK response from the server.
    def on_connect(client, userdata, flags, rc):
        print("Connected with result code " + str(rc))

        # Subscribing in on_connect() means that if we lose the connection and
        # reconnect then subscriptions will be renewed.
        mqttc.publish("xeno/service", "C2 works", 0, True)
        mqttc.subscribe("xeno/zone1")
        mqttc.subscribe("xeno/zone2")

    # The callback for when a PUBLISH message is received from the server.
    def on_message(client, userdata, msg):
        print(msg.topic + " " + str(msg.payload))
        if msg.topic in ("xeno/zone1", "xeno/zone2") and str(msg.payload).find("OFF") != -1:
            led1.off()

    mqttc = mqtt.Client("copernicus-test-client-2")
    mqttc.on_message = on_message
    mqttc.on_connect = on_connect

    mqttc.connect("test.mosquitto.org", 1883, 60)

    mqttc.will_set("xeno/service", "C2 does not work", 0, True)

    mqttc.loop_forever()
