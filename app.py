"""
https://www.twilio.com/blog/asynchronous-http-requests-in-python-with-aiohttp
https://stackoverflow.com/questions/72815312/request-a-lot-of-urls-with-asyncio
"""
import uvicorn
import aiohttp
import asyncio
import requests
from fastapi import FastAPI
from src.config import (logger,
                        parameters)
from src.data_types import SearchData

app = FastAPI(title="Expert-Bot-Dispatcher")


async def searching(session, url, data):
    async with session.post(url, json=data) as resp:
        response = await resp.json()
        return response


@app.post("/api/search")
async def search(data: SearchData):
    """searching etalon by  incoming text"""
    send_data = {"pubid": data.pubid, "text": data.text}
    if len(data.text.split()) >= parameters.max_text_len:
        logger.info("Input text {} has len {} more then max len {}, without  searching".format(str(data.text), 
                                                                                               str(len(data.text.split())), str(parameters.max_text_len)))
        return {"templateId": 0, "templateText": ""}
    else:
        conn = aiohttp.TCPConnector(limit=100)
        session_timeout = aiohttp.ClientTimeout(sock_connect=parameters.timeout_seconds, sock_read=parameters.timeout_seconds)
        logger.info("Input text for searching {} with pubid {}".format(data.text, data.pubid))
        async with aiohttp.ClientSession(connector=conn, timeout=session_timeout) as session:
            tasks = []
            for url in parameters.urls_for_searching:
                tasks.append(asyncio.ensure_future(searching(session, url, send_data)))
            try:
                taking_responses = await asyncio.gather(*tasks)
                print("taking_responses:", taking_responses)
            except:
                logger.exception("ClientSession is broken")
                return {"templateId": 0, "templateText": ""}
        logger.info("Searching results are {}".format(str([x for x in taking_responses])))
        for response in taking_responses:
            print(response)
            if response["templateId"] != 0:
                return {"templateId": response["templateId"], "templateText": response["templateText"]}
        
        if data.pubid in parameters.bss_pubs:
            res = requests.post(parameters.bss_bert_url, json=send_data)
            if res.json() is not None:
                return res.json()
            else:
                return {"templateId": 0, "templateText": ""}
        else:
            return {"templateId": 0, "templateText": ""}


if __name__ == "__main__":
    uvicorn.run(app, host=parameters.service_host, port=parameters.service_port)
