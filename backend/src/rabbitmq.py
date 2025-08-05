from fastapi import HTTPException
from faststream.rabbit.fastapi import RabbitRouter
from faststream.rabbit import RabbitBroker
import asyncio
from src.schemas import CallData
from src.database import db_dependency
from src.redis import redis_client, store_in_redis
from src.hand_download import download_and_store_file
from src.control_page import add_received_file, get_hand_mode, get_accept_files

router = RabbitRouter("amqp://guest:guest@rabbitmq:5672/")
broker = RabbitBroker("amqp://guest:guest@rabbitmq:5672/")

async def connect_to_rabbitmq():
    retries = 5
    delay = 5
    for attempt in range(retries):
        try:
            await broker.connect()
            return True
        except Exception as e:
            if attempt < retries - 1:
                await asyncio.sleep(delay)
                delay *= 2
    return False

@router.post("/receive_call_data/")
async def add_data_in_rabbit(data: CallData):
    try:
        q_data = data.model_dump()
        await router.broker.publish(
            q_data,
            queue="calls",
        )
        return {"status": "success", "data": q_data}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@broker.subscriber("calls")
async def receive_call_data(data: CallData):
    if not get_accept_files():
        raise

    try:
        url = data.fileUrl + "/download"
        if get_hand_mode():
            success = await download_and_store_file(url, data.callId, data.agentId, data.event_time)
        else:
            success = await store_in_redis(url, data.callId, data.agentId, data.event_time, redis_client)
        filename = data.fileUrl.split("/")[-1]

        file_info = {
            "filename": filename,
            "timestamp": data.event_time.split()[1],
            "agent_id": data.agentId,
            "download_status": "✅" if success else "❌"
        }
        add_received_file(file_info)

        return {
            "status": "success",
            "received_data": data.model_dump()
        }
    except Exception as e:
        raise