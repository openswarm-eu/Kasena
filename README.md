# Kasena

Kasena is a little project with the goal of measuring the temperatures of each office at the first floor of the building A at INRIA Paris.

## Dependencies
If you want to run the project, you should first download & install all the software mentioned in [this guide](https://dustcloud.atlassian.net/wiki/spaces/ALLDOC/pages/111458926/Lab+00.+Things+to+Install)

## How to run
To achieve our goal we will follow this steps:

1. First of all, we will connect a SmartMesh IP Manager and follow the part about the manager of this guide: 

2. Then we’ll turn on and deploy a series of SmartMesh IP Motes around the floor creating a mesh network. It’s really important to check in a serial terminal that all the motes are connected to the manager.

3. After that we’ll run instances of both JsonServer.py and node-red, to do so please follow this guide: 

4. Once all of the above are done, there’s only one thing left to do: import and deploy into node-red the flow needed to recieve measurements and store them in a .csv file. To do so, you should click the three lines icon at the top-right corner, select import and finally paste the following flow json:

    ```json
    [
    {
        "id": "ca4e03938b0d6d91",
        "type": "tab",
        "label": "Flow 1",
        "disabled": false,
        "info": "",
        "env": []
    },
    {
        "id": "dc8ecbb811810d45",
        "type": "http response",
        "z": "ca4e03938b0d6d91",
        "name": "",
        "statusCode": "",
        "headers": {},
        "x": 390,
        "y": 340,
        "wires": []
    },
    {
        "id": "412b5c41f101603b",
        "type": "http in",
        "z": "ca4e03938b0d6d91",
        "name": "",
        "url": "/oap",
        "method": "post",
        "upload": false,
        "swaggerDoc": "",
        "x": 240,
        "y": 300,
        "wires": [
            [
                "dc8ecbb811810d45",
                "f88d146bd50bd2b1",
                "9a504a31f7daa089"
            ]
        ]
    },
    {
        "id": "9a504a31f7daa089",
        "type": "function",
        "z": "ca4e03938b0d6d91",
        "name": "get_row_data",
        "func": "const MAC = msg.payload.mac;\nconst TIMESTAMP = msg.payload.fields.received_timestamp;\nconst TEMPERATURE = msg.payload.fields.samples[0]/100;\n\nconst CALIBRATION = {\n    \"00-17-0D-00-00-30-52-44\": 0.0,\n    \"00-17-0D-00-00-31-C7-B4\": 0.0,\n    \"00-17-0D-00-00-31-D1-70\": 0.0,\n    \"00-17-0D-00-00-31-D1-AC\": 0.0,\n    \"00-17-0D-00-00-31-CC-0F\": 0.0,\n    \"00-17-0D-00-00-31-D5-67\": 0.0,\n    \"00-17-0D-00-00-31-CB-E7\": 0.0,\n    \"00-17-0D-00-00-31-C1-A1\": 0.0,\n    \"00-17-0D-00-00-31-D1-D3\": 0.0,\n    \"00-17-0D-00-00-31-D1-32\": 0.0,\n    \"00-17-0D-00-00-31-D5-30\": 0.0,\n    \"00-17-0D-00-00-31-D5-01\": 0.0,\n    \"00-17-0D-00-00-31-CA-03\": 0.0,\n    \"00-17-0D-00-00-31-C1-A0\": 0.0,\n    \"00-17-0D-00-00-31-C9-E6\": 0.0,\n    \"00-17-0D-00-00-31-D5-69\": 0.0,\n    \"00-17-0D-00-00-31-C9-DA\": 0.0,\n    \"00-17-0D-00-00-31-C6-B8\": 0.0,\n    \"00-17-0D-00-00-31-D5-20\": 0.0,\n    \"00-17-0D-00-00-31-CC-59\": 0.0,\n    \"00-17-0D-00-00-31-C1-C1\": 0.0,\n    \"00-17-0D-00-00-31-C3-71\": 0.0,\n    \"00-17-0D-00-00-31-CB-E5\": 0.0,\n    \"00-17-0D-00-00-31-D4-7E\": 0.0,\n    \"00-17-0D-00-00-31-C3-37\": 0.0,\n    \"00-17-0D-00-00-31-D1-A8\": 0.0,\n    \"00-17-0D-00-00-31-C6-A1\": 0.0,\n    \"00-17-0D-00-00-31-D5-86\": 0.0,\n    \"00-17-0D-00-00-31-C7-B0\": 0.0\n};\n\nmsg.payload = {\n    \"mac\" : MAC,\n    \"timestamp\": TIMESTAMP,\n    \"temperature\": TEMPERATURE + CALIBRATION[MAC.toUpperCase()]\n};\nreturn msg;",
        "outputs": 1,
        "noerr": 0,
        "initialize": "",
        "finalize": "",
        "libs": [],
        "x": 420,
        "y": 240,
        "wires": [
            [
                "c48cbedc7b7f53b9"
            ]
        ]
    },
    {
        "id": "c48cbedc7b7f53b9",
        "type": "csv",
        "z": "ca4e03938b0d6d91",
        "name": "to_csv_row",
        "sep": ",",
        "hdrin": "",
        "hdrout": "once",
        "multi": "one",
        "ret": "\\n",
        "temp": "mac,timestamp,temperature",
        "skip": "0",
        "strings": true,
        "include_empty_strings": "",
        "include_null_values": "",
        "x": 610,
        "y": 240,
        "wires": [
            [
                "6639bb386c791289",
                "e7840572f459da94"
            ]
        ]
    },
    {
        "id": "6639bb386c791289",
        "type": "file",
        "z": "ca4e03938b0d6d91",
        "name": "append_temp_to_csv",
        "filename": "/home/pi/kasena/offices_temp_data.csv",
        "filenameType": "str",
        "appendNewline": false,
        "createDir": true,
        "overwriteFile": "false",
        "encoding": "none",
        "x": 820,
        "y": 260,
        "wires": [
            []
        ]
    },
    {
        "id": "e7840572f459da94",
        "type": "debug",
        "z": "ca4e03938b0d6d91",
        "name": "csv_row_debug",
        "active": true,
        "tosidebar": true,
        "console": false,
        "tostatus": false,
        "complete": "payload",
        "targetType": "msg",
        "statusVal": "",
        "statusType": "auto",
        "x": 800,
        "y": 220,
        "wires": []
    },
    {
        "id": "5bb803e419f0d7bf",
        "type": "http response",
        "z": "ca4e03938b0d6d91",
        "name": "",
        "statusCode": "",
        "headers": {},
        "x": 390,
        "y": 440,
        "wires": []
    },
    {
        "id": "aa5d5bafecb39c18",
        "type": "http in",
        "z": "ca4e03938b0d6d91",
        "name": "",
        "url": "/hr",
        "method": "post",
        "upload": false,
        "swaggerDoc": "",
        "x": 240,
        "y": 400,
        "wires": [
            [
                "5bb803e419f0d7bf",
                "eda97d0414adff54"
            ]
        ]
    },
    {
        "id": "9beaaa2d9cb99b44",
        "type": "http response",
        "z": "ca4e03938b0d6d91",
        "name": "",
        "statusCode": "",
        "headers": {},
        "x": 390,
        "y": 540,
        "wires": []
    },
    {
        "id": "15f39f5db85bb479",
        "type": "http in",
        "z": "ca4e03938b0d6d91",
        "name": "",
        "url": "/notifData",
        "method": "post",
        "upload": false,
        "swaggerDoc": "",
        "x": 220,
        "y": 500,
        "wires": [
            [
                "9beaaa2d9cb99b44",
                "c54ce568662e47ca"
            ]
        ]
    },
    {
        "id": "b490971b4cbe23b9",
        "type": "http response",
        "z": "ca4e03938b0d6d91",
        "name": "",
        "statusCode": "",
        "headers": {},
        "x": 390,
        "y": 640,
        "wires": []
    },
    {
        "id": "2afb3de63e4e1119",
        "type": "http in",
        "z": "ca4e03938b0d6d91",
        "name": "",
        "url": "/notifLog",
        "method": "post",
        "upload": false,
        "swaggerDoc": "",
        "x": 220,
        "y": 600,
        "wires": [
            [
                "b490971b4cbe23b9",
                "fef1c1cf11be14ee"
            ]
        ]
    },
    {
        "id": "e3028f9d1089d413",
        "type": "http response",
        "z": "ca4e03938b0d6d91",
        "name": "",
        "statusCode": "",
        "headers": {},
        "x": 390,
        "y": 740,
        "wires": []
    },
    {
        "id": "f9fbc957823cb19a",
        "type": "http in",
        "z": "ca4e03938b0d6d91",
        "name": "",
        "url": "/notifIpData",
        "method": "post",
        "upload": false,
        "swaggerDoc": "",
        "x": 210,
        "y": 700,
        "wires": [
            [
                "e3028f9d1089d413",
                "c8b9ccc8830d31ac"
            ]
        ]
    },
    {
        "id": "e2d1569f2ced618d",
        "type": "http response",
        "z": "ca4e03938b0d6d91",
        "name": "",
        "statusCode": "",
        "headers": {},
        "x": 390,
        "y": 840,
        "wires": []
    },
    {
        "id": "7f47034cdf70d011",
        "type": "http in",
        "z": "ca4e03938b0d6d91",
        "name": "",
        "url": "/notifHealthReport",
        "method": "post",
        "upload": false,
        "swaggerDoc": "",
        "x": 190,
        "y": 800,
        "wires": [
            [
                "e2d1569f2ced618d",
                "1306d91f77afeea1"
            ]
        ]
    },
    {
        "id": "5ba2a9a8cb7ff9cb",
        "type": "http response",
        "z": "ca4e03938b0d6d91",
        "name": "",
        "statusCode": "",
        "headers": {},
        "x": 390,
        "y": 940,
        "wires": []
    },
    {
        "id": "7a56a62d54c197ed",
        "type": "http in",
        "z": "ca4e03938b0d6d91",
        "name": "",
        "url": "/event",
        "method": "post",
        "upload": false,
        "swaggerDoc": "",
        "x": 230,
        "y": 900,
        "wires": [
            [
                "5ba2a9a8cb7ff9cb",
                "2e5b810ba350555d"
            ]
        ]
    },
    {
        "id": "eda97d0414adff54",
        "type": "mqtt out",
        "z": "ca4e03938b0d6d91",
        "name": "mqtt: hr",
        "topic": "Kasena@Inria-Paris/hr",
        "qos": "",
        "retain": "",
        "respTopic": "",
        "contentType": "",
        "userProps": "",
        "correl": "",
        "expiry": "",
        "broker": "c21f9dc6bce6aa9c",
        "x": 540,
        "y": 400,
        "wires": []
    },
    {
        "id": "c54ce568662e47ca",
        "type": "mqtt out",
        "z": "ca4e03938b0d6d91",
        "name": "mqtt: notifData",
        "topic": "Kasena@Inria-Paris/notifData",
        "qos": "",
        "retain": "",
        "respTopic": "",
        "contentType": "",
        "userProps": "",
        "correl": "",
        "expiry": "",
        "broker": "c21f9dc6bce6aa9c",
        "x": 560,
        "y": 500,
        "wires": []
    },
    {
        "id": "fef1c1cf11be14ee",
        "type": "mqtt out",
        "z": "ca4e03938b0d6d91",
        "name": "mqtt: notifLog",
        "topic": "Kasena@Inria-Paris/notifLog",
        "qos": "",
        "retain": "",
        "respTopic": "",
        "contentType": "",
        "userProps": "",
        "correl": "",
        "expiry": "",
        "broker": "c21f9dc6bce6aa9c",
        "x": 560,
        "y": 600,
        "wires": []
    },
    {
        "id": "c8b9ccc8830d31ac",
        "type": "mqtt out",
        "z": "ca4e03938b0d6d91",
        "name": "mqtt: notifIpData",
        "topic": "Kasena@Inria-Paris/notifIpData",
        "qos": "",
        "retain": "",
        "respTopic": "",
        "contentType": "",
        "userProps": "",
        "correl": "",
        "expiry": "",
        "broker": "c21f9dc6bce6aa9c",
        "x": 570,
        "y": 700,
        "wires": []
    },
    {
        "id": "1306d91f77afeea1",
        "type": "mqtt out",
        "z": "ca4e03938b0d6d91",
        "name": "mqtt: notifHealthReport",
        "topic": "Kasena@Inria-Paris/notifHealthReport",
        "qos": "",
        "retain": "",
        "respTopic": "",
        "contentType": "",
        "userProps": "",
        "correl": "",
        "expiry": "",
        "broker": "c21f9dc6bce6aa9c",
        "x": 590,
        "y": 800,
        "wires": []
    },
    {
        "id": "2e5b810ba350555d",
        "type": "mqtt out",
        "z": "ca4e03938b0d6d91",
        "name": "mqtt: event",
        "topic": "Kasena@Inria-Paris/event",
        "qos": "",
        "retain": "",
        "respTopic": "",
        "contentType": "",
        "userProps": "",
        "correl": "",
        "expiry": "",
        "broker": "c21f9dc6bce6aa9c",
        "x": 550,
        "y": 900,
        "wires": []
    },
    {
        "id": "f88d146bd50bd2b1",
        "type": "mqtt out",
        "z": "ca4e03938b0d6d91",
        "name": "mqtt: oap",
        "topic": "Kasena@Inria-Paris/oap",
        "qos": "",
        "retain": "",
        "respTopic": "",
        "contentType": "",
        "userProps": "",
        "correl": "",
        "expiry": "",
        "broker": "c21f9dc6bce6aa9c",
        "x": 540,
        "y": 300,
        "wires": []
    },
    {
        "id": "c21f9dc6bce6aa9c",
        "type": "mqtt-broker",
        "name": "public hivemqtt broker",
        "broker": "broker.hivemq.com",
        "port": "1883",
        "clientid": "",
        "autoConnect": true,
        "usetls": false,
        "protocolVersion": "4",
        "keepalive": "60",
        "cleansession": true,
        "birthTopic": "",
        "birthQos": "0",
        "birthPayload": "",
        "birthMsg": {},
        "closeTopic": "",
        "closeQos": "0",
        "closePayload": "",
        "closeMsg": {},
        "willTopic": "",
        "willQos": "0",
        "willPayload": "",
        "willMsg": {},
        "userProps": "",
        "sessionExpiry": ""
    }
    ]
    ```
