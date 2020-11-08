import requests
import time

import asyncio
from azure.eventhub.aio import EventHubConsumerClient
from azure.eventhub.extensions.checkpointstoreblobaio import BlobCheckpointStore

ID_JEROEN = 878864710
ID_FREDERICK = 1273923095
OFFSET = 0
LATEST_TEMP = -1

URL = "https://api.telegram.org/bot1121749211:AAFmyn4kPHJBqItW22wCmwb1p0gMJjBRcOY/"

def checkForMessages():
    print("checking")
    global OFFSET
    response = requests.post(url = (URL + "getUpdates"),params= {"offset":OFFSET})
    data = response.json()
    if (data["ok"]):
        for i in range(len(data["result"])):
            if((data["result"][i]["update_id"]) >= OFFSET):
                    OFFSET = data["result"][i]["update_id"] + 1
                    print(OFFSET)
            if(data["result"][i]["message"]["chat"]["id"] == ID_FREDERICK):
                text = data["result"][i]["message"]["text"]
                print(text)
                if ("/getTemperature" in text):
                    replyTemperature(ID_FREDERICK)
            if(data["result"][i]["message"]["chat"]["id"] == ID_JEROEN):
                print(text)
                if ("/getTemperature" in text):
                    replyTemperature(ID_FREDERICK)

    elif(not data["ok"]):
        print("Error")


def replyTemperature(chat_id):
    reply = "Temperature is {}°C".format(LATEST_TEMP)
    requests.post(url = (URL + "sendMessage"),params = {"chat_id":chat_id,"text":reply})



async def on_event(partition_context, event):
    # Print the event data.
    #print("Received the event: \"{}\" from the partition with ID: \"{}\"".format(event.body_as_str(encoding='UTF-8'), partition_context.partition_id))
    LATEST_TEMP = float(event.body_as_str(encoding='UTF-8')[15:19])
    print(LATEST_TEMP)
    # Update the checkpoint so that the program doesn't read the events
    # that it has already read when you run it next time.
    await partition_context.update_checkpoint(event)

async def main():
    # Create an Azure blob checkpoint store to store the checkpoints.
    Checkpoint_store = BlobCheckpointStore.from_connection_string("DefaultEndpointsProtocol=https;AccountName=pycomstorage;AccountKey=uZRtTT/f4Wvxoy50FJIs+AzRA3ut7arVXCIP8MLo25jJnWlAx3h7QfD0EVvgNwpcqcAqz8mHr0iJMQ3wjCm0Bw==;EndpointSuffix=core.windows.net", "temperatureblobstorage")
    # Create a consumer client for the event hub.
    client = EventHubConsumerClient.from_connection_string("Endpoint=sb://realtimetemp.servicebus.windows.net/;SharedAccessKeyName=RealTimeTemp_TempOutput_policy;SharedAccessKey=1KMNBdrnuWM0LGAz4ruFiV/OdZ9s4VZdcIIJWQmnqcM=;EntityPath=realtimetempoutput", consumer_group="$Default", eventhub_name="realtimetempoutput")
    async with client:
        # Call the receive method. Read from the beginning of the partition (starting_position: "-1")
        await client.receive(on_event=on_event,  starting_position="-1")




if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    # Run the main method.
    loop.run_until_complete(main())-