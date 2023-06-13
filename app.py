"""
https://www.twilio.com/blog/asynchronous-http-requests-in-python-with-aiohttp
https://stackoverflow.com/questions/72815312/request-a-lot-of-urls-with-asyncio
"""
import uvicorn
import aiohttp
import asyncio
from fastapi import FastAPI
from src.config import (logger,
                        service_port,
                        service_host,
                        urls_for_searching)
from src.data_types import SearchData

app = FastAPI(title="Expert-Bot-Dispatcher")


async def searching(session, url, data):
    async with session.post(url, json=data) as resp:
        response = await resp.json()
        return response


@app.post("/api/search")
async def search(data: SearchData):
    """searching etalon by  incoming text"""
    results = []
    send_data = {"pubid": data.pubid, "text": data.text}
    conn = aiohttp.TCPConnector(limit=100)
    timeout_seconds = 0.5
    session_timeout = aiohttp.ClientTimeout(sock_connect=timeout_seconds, sock_read=timeout_seconds)
    logger.info("Input text for searching {} with pubid {}".format(data.text, data.pubid))
    async with aiohttp.ClientSession(connector=conn, timeout=session_timeout) as session:
        tasks = []
        for url in urls_for_searching:
            tasks.append(asyncio.ensure_future(searching(session, url, send_data)))
        try:
            taking_responses = await asyncio.gather(*tasks)
        except:
            return {"templateId": 0, "templateText": ""}
    for response in taking_responses:
        results.append(response)
    logger.info("Searching results are {}".format(str(results)))
    if results:
        for d in results:
            if d["templateId"] != 0:
                return {"templateId": d["templateId"], "templateText": d["templateText"]}
        return {"templateId": 0, "templateText": ""}
    else:
        return {"templateId": 0, "templateText": ""}


if __name__ == "__main__":
    uvicorn.run(app, host=service_host, port=service_port)
