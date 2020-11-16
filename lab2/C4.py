from VirtualCopernicusNG.tkgpio import TkCircuit

# initialize the circuit inside the
configuration = {
    "name": "C4",
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
    ],
    "buzzers": [
        {"x": 277, "y": 9, "name": "Buzzer", "pin": 16, "frequency": 440},
    ]
}
circuit = TkCircuit(configuration)

@circuit.run
def main():
    apartment = "a13"
    room = "lobby"
    device = "lamp"
    ID = 1

    # sockets initialization
    import socket
    MCAST_GRP = '236.0.0.0'
    MCAST_PORT = 3456

    sock_sender = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock_sender.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)
    socket_msg = "a13;*;*;*;off"


    # Raspberry Pi
    from gpiozero import LED, Button
    from time import sleep

    led1 = LED(21)  # lobby lamp

    def button1_pressed():
        led1.toggle()

    def button2_pressed():
        led1.off()
        sock_sender.sendto(socket_msg.encode('utf-8'), (MCAST_GRP, MCAST_PORT))

    button1 = Button(11)
    button1.when_pressed = button1_pressed

    button2 = Button(12)
    button2.when_pressed = button2_pressed

    while True:
        sleep(0.1)

