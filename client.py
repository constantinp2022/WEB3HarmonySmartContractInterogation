

#GLOBAL VARIABLES
WS_API_HARMONY_ADDRESS="https://ws.explorer-v2-api.hmny.io"
contractAddress="0x3C2B8Be99c50593081EAA2A724F0B8285F5aba8f" #USDT

import socketio
import json

# standard Python
sio = socketio.Client()
# sio = socketio.Client(logger=True, engineio_logger=True) #For more logs


# Callback for getTopFiveHolders
def processCallBackTopFiveHolders(data):
    # print('processCallBack called')
    jsonReceived = json.loads(data['payload'])
    # print(jsonReceived)

    for i in range(len(jsonReceived)):
        print (str(i + 1) + " holder address: " + str(jsonReceived[i]["ownerAddress"]))
        print (str(i + 1) + " holder balance: " + str(jsonReceived[i]["balance"]))
    


    sio.disconnect()


def getTopFiveHolders(contractAddressInput):
    my_sid = sio.sid
    # print('my sid is', my_sid)
    method = 'getERC20TokenHolders'
    contractAddressLowerCase = contractAddressInput.lower()
    params = [contractAddressLowerCase, 5, 0] #Just top 5 Holders
    sio.emit(method, params, callback=processCallBackTopFiveHolders)

def processCallContractsByField(data):
    # print('processCallContractsByField called')
    jsonReceived = json.loads(data['payload'])
    # print(jsonReceived)
    print("Creator address: " + str(jsonReceived["creatorAddress"]))


def getCreatorAddress(contractAddressInput):
    my_sid = sio.sid
    # print('my sid is', my_sid)
    method = 'getContractsByField'
    contractAddressLowerCase = contractAddressInput.lower()
    params = [0, "address", contractAddressLowerCase] #First is the shard
    sio.emit(method, params, callback=processCallContractsByField)

def processCallAllInformationERC20(data):
    # print('processCallContractsByField called')
    # print(data)
    jsonReceived = json.loads(data['payload'])
    # print(jsonReceived) 

    contractAddressLowerCase = contractAddress.lower()
    for i in range(len(jsonReceived)):
        if jsonReceived[i]['address'] == contractAddressLowerCase:
            print("Name: " + str(jsonReceived[i]["name"]))
            print("Symbol: " + str(jsonReceived[i]["symbol"]))
            print("Decimals: " + str(jsonReceived[i]["decimals"]))
            print("Total Supply: " + str(jsonReceived[i]["totalSupply"]))
            print("Circulating Supply: " + str(jsonReceived[i]["circulatingSupply"]))
            print("Holders: " + str(jsonReceived[i]["holders"]))
            print("Transaction Count: " + str(jsonReceived[i]["transactionCount"]))
            print("Last Update bock number: " + str(jsonReceived[i]["lastUpdateBlockNumber"]))




def getAllInformationERC20():
    my_sid = sio.sid
    # print('my sid is', my_sid)
    method = 'getAllERC20'
    params = [] #No args
    sio.emit(method, params, callback=processCallAllInformationERC20)


sio.connect(WS_API_HARMONY_ADDRESS, transports=["websocket"])
getTopFiveHolders(contractAddress)
getCreatorAddress(contractAddress)
getAllInformationERC20()
sio.wait()
sio.disconnect()