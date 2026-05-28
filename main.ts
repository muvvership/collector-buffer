function sendBufferedReadings () {
    if (node2Dirty) {
        node2Sent = node2Message
        serial.writeLine(node2Message)
        basic.pause(50)
    }
    if (node3Dirty) {
        node3Sent = node3Message
        serial.writeLine(node3Message)
        basic.pause(50)
    }
    if (node5Dirty) {
        node5Sent = node5Message
        serial.writeLine(node5Message)
        basic.pause(50)
    }
    if (node7Dirty) {
        node7Sent = node7Message
        serial.writeLine(node7Message)
        basic.pause(50)
    }
    serial.writeLine("DONE")
    basic.showLeds(`
        . . . . .
        . . . . .
        . . # . .
        . . . . .
        . . . . .
        `)
    basic.pause(50)
    basic.clearScreen()
}
function bufferReading (receivedString: string) {
    parts = receivedString.split(",")
    if (parts.length >= 4) {
        if (parts[0] == "2") {
            node2Message = receivedString
            node2Dirty = true
            basic.showLeds(`
                # . . . .
                . . . . .
                . . . . .
                . . . . .
                . . . . .
                `)
        } else if (parts[0] == "3") {
            node3Message = receivedString
            node3Dirty = true
            basic.showLeds(`
                . . . . #
                . . . . .
                . . . . .
                . . . . .
                . . . . .
                `)
        } else if (parts[0] == "5") {
            node5Message = receivedString
            node5Dirty = true
            basic.showLeds(`
                . . . . .
                . . . . .
                . . . . .
                . . . . .
                . . . . #
                `)
        } else if (parts[0] == "7") {
            node7Message = receivedString
            basic.showLeds(`
                . . . . .
                . . . . .
                . . . . .
                . . . . .
                # . . . .
                `)
            node7Dirty = true
        }
        basic.pause(50)
        basic.clearScreen()
    }
}
input.onButtonPressed(Button.A, function () {
    wiggle = burstTick % 5
    for (let i = 0; i <= beds.length - 1; i++) {
        id = beds[i]
        tC = Math.round((tempBase[i] + wiggle * 0.1) * 10) / 10
        h = humBase[i] + wiggle
        s = soilBase[i] + wiggle
        bufferReading("" + id + "," + tC + "," + h + "," + s)
    }
    burstTick = burstTick + 1
    basic.showIcon(IconNames.SmallDiamond)
    basic.pause(50)
    basic.clearScreen()
})
radio.onReceivedString(function (receivedString) {
    bufferReading(receivedString)
})
function clearAcknowledged (nodeText: string) {
    if (nodeText == "2") {
        if (node2Message == node2Sent) {
            node2Dirty = false
            node2Sent = ""
        }
    } else if (nodeText == "3") {
        if (node3Message == node3Sent) {
            node3Dirty = false
            node3Sent = ""
        }
    } else if (nodeText == "5") {
        if (node5Message == node5Sent) {
            node5Dirty = false
            node5Sent = ""
        }
    } else if (nodeText == "7") {
        if (node7Message == node7Sent) {
            node7Dirty = false
            node7Sent = ""
        }
    }
}
serial.onDataReceived(serial.delimiters(Delimiters.NewLine), function () {
    incomingCommand = serial.readLine()
    if (incomingCommand == "REQ") {
        sendBufferedReadings()
    } else {
        commandParts = incomingCommand.split(",")
        if (commandParts.length >= 2) {
            if (commandParts[0] == "ACK") {
                clearAcknowledged(commandParts[1])
                basic.showLeds(`
                    . . . . .
                    . . . . .
                    . . # . .
                    . . . . .
                    . . . . .
                    `)
                basic.pause(50)
                basic.clearScreen()
            }
        }
    }
})
let commandParts: string[] = []
let incomingCommand = ""
let s = 0
let h = 0
let tC = 0
let id = 0
let burstTick = 0
let wiggle = 0
let parts: string[] = []
let node7Message = ""
let node7Sent = ""
let node7Dirty = false
let node5Message = ""
let node5Sent = ""
let node5Dirty = false
let node3Message = ""
let node3Sent = ""
let node3Dirty = false
let node2Message = ""
let node2Sent = ""
let node2Dirty = false
let soilBase: number[] = []
let humBase: number[] = []
let tempBase: number[] = []
let beds: number[] = []
radio.setGroup(99)
led.setBrightness(10)
serial.redirect(
SerialPin.P1,
SerialPin.P0,
BaudRate.BaudRate115200
)
// Debug: press A to seed one canned reading per canonical node
// (2, 3, 5, 7). The ESP32 will pull these on its next wake cycle.
beds = [
2,
3,
5,
7
]
tempBase = [
23.5,
22.8,
24.1,
21.4
]
humBase = [
65,
61,
58,
70
]
soilBase = [
42,
45,
39,
48
]
