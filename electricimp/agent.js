server.log("Agent Started");

device.on("newdata", function(s) {
    local request = http.post("http://pythonscript.richiezeng.com:8000",
        { "Content-Type": "application/x-www-form-urlencoded"},
        http.urlencode(s));
    local response = request.sendsync();
    server.log("Request sent, got "+response.statuscode);
    //server.log("Response contains: "+response.body);
});
