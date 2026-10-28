# RFID WebSocket

Connect to `/ws/rfid` and send either the text message `get_rfid` or the JSON
message `{"protocol": "get_rfid"}`. The next RFID tag is returned as
`{"protocol": "get_rfid", "tag": 123}`. Tags scanned when no read is requested
continue to use the default room-creation behavior.
