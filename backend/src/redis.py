import json
from redis import Redis
from httpx import AsyncClient
from io import BytesIO
from src.duration import duration
from src.api_params import get_auto_params

redis_client = Redis(host='redis', port=6379, db=0)

    
async def store_in_redis(url: str, call_id: str, agent_id: str, call_date: str, redis_client) ->bool:
    try:
        async with AsyncClient() as client:
            response = await client.get(url)
            response.raise_for_status()
            file_duration = duration(response.content)

            agent_img = await client.get(f'https://robohash.org/{agent_id}')
            file_data = {
                "content": response.content.decode('latin1'),
                "img": agent_img.content.decode('latin1'),
            }
            redis_client.set(call_id, json.dumps(file_data))
            await send_and_clean_redis(redis_client, call_id, call_date, agent_id, file_duration)

            return True
    except Exception as e:
        print(f"Store in Redis failed: {e}")
        return False

async def send_and_clean_redis(redis_client, call_id: str, date: str, agent: str, dur: str):
    try:
        data = redis_client.get(call_id)
        file_data = json.loads(data)
        url = "https://cxmonline.ru/service/responder"
        ai_url = "https://httpbin.org/post"
        params = get_auto_params()
        data = {
            "LoginName": "autoopt-call-robot",
            "Password": "123",
            "QuestionID": params["QuestionID"],#(redis_client.hget("auto_params", "QuestionID") or b"").decode(),
            "ButtonAlias": params["ButtonAlias"],#(redis_client.hget("auto_params", "ButtonAlias") or b"").decode(),
            "DateLocal": date,
            "DateUTC": date,
            "HubComputerName": params["HubComputerName"],#(redis_client.hget("auto_params", "HubComputerName") or b"").decode(),
            "POS": params["POS"],#(redis_client.hget("auto_params", "POS") or b"").decode(),
            "ButtonPanel": agent,
            "UserText": params["UserText"],#(redis_client.hget("auto_params", "UserText") or b"").decode(),
            'Attr[1][Alias]': 'Call Duration',
            'Attr[1][Description]': '',
            'Attr[1][DataType]': 'text',
            'Attr[1][Value]': dur
        }

        file_content = file_data["content"].encode('latin1')
        agent_img = file_data["img"].encode('latin1')
        files = {
            "AttachedSoundFile": (call_id, BytesIO(file_content),"audio/mpeg"),
            "AttachedPictureFile": (agent, BytesIO(agent_img),"image/png")
        }
        headers = {
            "User-Agent": "EPM-Agent",
            "RequestType": "SendMessage"
        }

        async with AsyncClient(timeout=30.0) as client:
            response = await client.post(url, data=data, files=files, headers=headers)
            airesponse = await client.post(ai_url, data=data, files=files, headers=headers)
            if response.status_code == 200 and response.text.split()[1] == "000" and airesponse.status_code == 200:
                print(f"Successfully sent file {call_id}")
                redis_client.delete(call_id)
                return True
            else:
                print(f"Failed to send data for record {call_id}, status: {response.status_code}")
                return False

    except Exception as e:
        print(f"Error processing Redis record {call_id}: {e}")
        return False
