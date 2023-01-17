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
            "id": "dc8ecbb811810d45",
            "type": "http response",
            "z": "ca4e03938b0d6d91",
            "name": "",
            "statusCode": "",
            "headers": {},
            "x": 410,
            "y": 360,
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
            "x": 260,
            "y": 320,
            "wires": [
                [
                    "dc8ecbb811810d45",
                    "9a504a31f7daa089"
                ]
            ]
        },
        {
            "id": "9a504a31f7daa089",
            "type": "function",
            "z": "ca4e03938b0d6d91",
            "name": "get_row_data",
            "func": "const MAC = msg.payload.mac;\nconst TIMESTAMP = msg.payload.fields.received_timestamp;\nconst TEMPERATURE = msg.payload.fields.samples[0]/100;\n\nmsg.payload = {\n    \"mac\" : MAC,\n    \"timestamp\": TIMESTAMP,\n    \"temperature\": TEMPERATURE\n};\nreturn msg;",
            "outputs": 1,
            "noerr": 0,
            "initialize": "",
            "finalize": "",
            "libs": [],
            "x": 440,
            "y": 280,
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
            "x": 630,
            "y": 280,
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
            "filename": "/Users/rdelaf/documents/inria/dust_temp/offices_temp_data.csv",
            "filenameType": "str",
            "appendNewline": false,
            "createDir": true,
            "overwriteFile": "false",
            "encoding": "none",
            "x": 840,
            "y": 340,
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
            "x": 820,
            "y": 240,
            "wires": []
        }
    ]
    ```