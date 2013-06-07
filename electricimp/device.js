s <- "";

function readSerial() {  
    local result = hardware.uart12.read();
    if (result == -1) {
        server.log("No data returned.");
    } else {
        if (result == 2) s="";
        else if (result ==3) {
            server.log("got "+s);
            agent.send("newdata", {"rfid" : s});
        }
        else s+=format("%c",result);
    }
}

// configure a pin pair for UART TX/RX
server.log("Starting");
imp.configure("Serial RX", [], []);
hardware.uart12.configure(9600, 8, PARITY_NONE, 1, NO_CTSRTS, readSerial);
