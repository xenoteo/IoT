from VirtualCopernicusNG.tkgpio import TkCircuit

# initialize the circuit inside the
configuration = {
    "name": "C1",
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
    # sockets initialization
    import struct
    import socket
    MCAST_GRP = '236.0.0.0'
    MCAST_PORT = 3456

    sock_receiver = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock_receiver.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock_receiver.bind(('', MCAST_PORT))
    mreq = struct.pack("4sl", socket.inet_aton(MCAST_GRP), socket.INADDR_ANY)
    sock_receiver.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

    sock_sender = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock_sender.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)
    socket_msg = "a13;kitchen;lamp;1;change"


    # Raspberry Pi
    from gpiozero import LED, Button
    from time import sleep

    led1 = LED(21)  # living room lamp

    def button1_pressed():
        led1.toggle()

    def button2_pressed():
        sock_sender.sendto(socket_msg.encode('utf-8'), (MCAST_GRP, MCAST_PORT))

    button1 = Button(11)
    button1.when_pressed = button1_pressed

    button2 = Button(12)
    button2.when_pressed = button2_pressed


    # receiving the commands
    apartment = "a13"
    room = "living room"
    device = "lamp"
    ID = 1

    def handle_led_command(led, instruction):
        if instruction == "on":
            led.on()
        elif instruction == "off":
            led.off()
        elif instruction == "change":
            led.toggle()

    while True:
        command = sock_receiver.recv(10240)
        command = command.decode("utf-8")
        params = command.split(';')
        if params[0] == apartment and (params[1] == room or params[1] == "*") and (
                params[2] == device or params[2] == "*") and (params[3] == str(ID) or params[3] == "*"):
            handle_led_command(led1, params[4])
        sleep(0.1)

