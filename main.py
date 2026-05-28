def sendBufferedReadings():
    global node2Sent, node3Sent, node5Sent, node7Sent
    if node2Dirty:
        node2Sent = node2Message
        serial.write_line(node2Message)
        basic.pause(50)
    if node3Dirty:
        node3Sent = node3Message
        serial.write_line(node3Message)
        basic.pause(50)
    if node5Dirty:
        node5Sent = node5Message
        serial.write_line(node5Message)
        basic.pause(50)
    if node7Dirty:
        node7Sent = node7Message
        serial.write_line(node7Message)
        basic.pause(50)
    serial.write_line("DONE")
    basic.show_leds("""
        . . . . .
        . . . . .
        . . # . .
        . . . . .
        . . . . .
        """)
    basic.pause(50)
    basic.clear_screen()
def bufferReading(receivedString: str):
    global parts, node2Message, node2Dirty, node3Message, node3Dirty, node5Message, node5Dirty, node7Message, node7Dirty
    parts = receivedString.split(",")
    if len(parts) >= 4:
        if parts[0] == "2":
            node2Message = receivedString
            node2Dirty = True
            basic.show_leds("""
                # . . . .
                . . . . .
                . . . . .
                . . . . .
                . . . . .
                """)
        elif parts[0] == "3":
            node3Message = receivedString
            node3Dirty = True
            basic.show_leds("""
                . . . . #
                . . . . .
                . . . . .
                . . . . .
                . . . . .
                """)
        elif parts[0] == "5":
            node5Message = receivedString
            node5Dirty = True
            basic.show_leds("""
                . . . . .
                . . . . .
                . . . . .
                . . . . .
                . . . . #
                """)
        elif parts[0] == "7":
            node7Message = receivedString
            basic.show_leds("""
                . . . . .
                . . . . .
                . . . . .
                . . . . .
                # . . . .
                """)
            node7Dirty = True
        basic.pause(50)
        basic.clear_screen()

def on_button_pressed_a():
    global wiggle, id2, tC, h, s, burstTick
    wiggle = burstTick % 5
    i = 0
    while i <= len(beds) - 1:
        id2 = beds[i]
        tC = Math.round((tempBase[i] + wiggle * 0.1) * 10) / 10
        h = humBase[i] + wiggle
        s = soilBase[i] + wiggle
        bufferReading("" + str(id2) + "," + str(tC) + "," + str(h) + "," + str(s))
        i += 1
    burstTick = burstTick + 1
    basic.show_icon(IconNames.SMALL_DIAMOND)
    basic.pause(50)
    basic.clear_screen()
input.on_button_pressed(Button.A, on_button_pressed_a)

def on_received_string(receivedString2):
    bufferReading(receivedString2)
radio.on_received_string(on_received_string)

def clearAcknowledged(nodeText: str):
    global node2Dirty, node2Sent, node3Dirty, node3Sent, node5Dirty, node5Sent, node7Dirty, node7Sent
    if nodeText == "2":
        if node2Message == node2Sent:
            node2Dirty = False
            node2Sent = ""
    elif nodeText == "3":
        if node3Message == node3Sent:
            node3Dirty = False
            node3Sent = ""
    elif nodeText == "5":
        if node5Message == node5Sent:
            node5Dirty = False
            node5Sent = ""
    elif nodeText == "7":
        if node7Message == node7Sent:
            node7Dirty = False
            node7Sent = ""

def on_data_received():
    global incomingCommand, commandParts
    incomingCommand = serial.read_line()
    if incomingCommand == "REQ":
        sendBufferedReadings()
    else:
        commandParts = incomingCommand.split(",")
        if len(commandParts) >= 2:
            if commandParts[0] == "ACK":
                clearAcknowledged(commandParts[1])
                basic.show_leds("""
                    . . . . .
                    . . . . .
                    . . # . .
                    . . . . .
                    . . . . .
                    """)
                basic.pause(50)
                basic.clear_screen()
serial.on_data_received(serial.delimiters(Delimiters.NEW_LINE), on_data_received)

commandParts: List[str] = []
incomingCommand = ""
s = 0
h = 0
tC = 0
id2 = 0
burstTick = 0
wiggle = 0
parts: List[str] = []
node7Message = ""
node7Sent = ""
node7Dirty = False
node5Message = ""
node5Sent = ""
node5Dirty = False
node3Message = ""
node3Sent = ""
node3Dirty = False
node2Message = ""
node2Sent = ""
node2Dirty = False
soilBase: List[number] = []
humBase: List[number] = []
tempBase: List[number] = []
beds: List[number] = []
radio.set_group(99)
led.set_brightness(10)
# Debug: press A to seed one canned reading per canonical node
# (2, 3, 5, 7). The ESP32 will pull these on its next wake cycle.
beds = [2, 3, 5, 7]
tempBase = [23.5, 22.8, 24.1, 21.4]
humBase = [65, 61, 58, 70]
soilBase = [42, 45, 39, 48]