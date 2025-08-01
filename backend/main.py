from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from passlib.context import CryptContext
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from faststream.rabbit.fastapi import RabbitRouter
from faststream.rabbit import RabbitBroker
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI()
router = RabbitRouter("amqp://guest:guest@rabbitmq:5672/")
broker = RabbitBroker("amqp://guest:guest@rabbitmq:5672/")

# CORS настройки
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*","http://localhost", "http://localhost:8080"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Конфигурация
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Тестовый пользователь
fake_user = {
    "username": "admin",
    "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW"
}

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserIn(BaseModel):
    username: str
    password: str

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict):
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)

@app.post("/token")
async def login(user_data: UserIn):
    if (user_data.username != fake_user["username"] or 
        not verify_password(user_data.password, fake_user["hashed_password"])):
        raise HTTPException(status_code=400, detail="Неверные данные")
    return {"access_token": create_access_token({"sub": user_data.username}), "token_type": "bearer"}

@app.get("/protected") 
async def protected_route(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return
    except JWTError:
        raise HTTPException(status_code=401, detail="Не авторизован")
    

##########################################################################################################
from collections import deque

accept_files = False
hand_mode = False
received_files = deque()

def add_received_file(file):
    if len(received_files) >=5:
        received_files.popleft()
        received_files.append(file)
        return
    received_files.append(file)
    return

@app.get("/control_data")
async def get_control_data():
    global accept_files, received_files, hand_mode
    return {
        "accept_files": accept_files,
        "hand_mode": hand_mode,
        "received_files": list(received_files)[::-1],
    }

@app.post("/toggle_accept/")
async def toggle_accept():
    global accept_files
    accept_files = not accept_files
    return {"status": "success", "accept_files": accept_files}

@app.post("/toggle_hand_mode")
async def toggle_hand_mode():
    global hand_mode
    hand_mode = not hand_mode
    return {"status": "success", "hand_mode": hand_mode}

######################################################################

import redis

redis_client = redis.Redis(host='redis', port=6379, db=0)

class CallData(BaseModel):
    callId: str
    callDate: Optional[str] = None
    fileUrl: str
    agentId: str
    event_time: str

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
async def receive_call_data(data: CallData):#, db: db_dependency):
    global accept_files, received_files

    if not accept_files:
        raise

    try:
        url = data.fileUrl + "/download"
        if hand_mode:
            pass
            #success = await download_and_store_file(url, data.callId, data.agentId, data.event_time, db)
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
    
import httpx
import json
from io import BytesIO
    
async def store_in_redis(url: str, call_id: str, agent_id: str, call_date: str, redis_client) ->bool:
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            response.raise_for_status()
            file_duration = duration(response.content)

            agent_img = await client.get(f'https://robohash.org/{agent_id}')
            file_data = {
                "content": response.content.decode('latin1'),
                "img": agent_img.content.decode('latin1'),
                "date": call_date,
                "agent_id": agent_id,
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
        data = {
            "LoginName": "autoopt-call-robot",
            "Password": "123",
            "QuestionID": "2198",#(redis_client.hget("auto_params", "QuestionID") or b"").decode(),
            "ButtonAlias": "1",#(redis_client.hget("auto_params", "ButtonAlias") or b"").decode(),
            "DateLocal": date,
            "DateUTC": date,
            "HubComputerName": "test",#(redis_client.hget("auto_params", "HubComputerName") or b"").decode(),
            "POS": "667",#(redis_client.hget("auto_params", "POS") or b"").decode(),
            "ButtonPanel": agent,
            "UserText": (redis_client.hget("auto_params", "UserText") or b"").decode(),
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

        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(url, data=data, files=files, headers=headers)
            if response.status_code == 200 and response.text.split()[1] == "000":
                print(f"Successfully sent file {call_id}")
                redis_client.delete(call_id)
                return True
            else:
                print(f"Failed to send data for record {call_id}, status: {response.status_code}")
                return False

    except Exception as e:
        print(f"Error processing Redis record {call_id}: {e}")
        return False

from mutagen.mp3 import MP3

def duration(b_file: bytes) -> str:
    file = BytesIO(b_file)
    audio = MP3(file)
    dur = audio.info.length
    if dur < 3*60: value = "short"
    elif dur < 6*60: value = "middle"
    else: value = "long"
    file.seek(0)
    return value


app.include_router(router)

import asyncio

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

async def main() -> None:
    async with broker:
        await broker.start()
        config = uvicorn.Config(app, host="0.0.0.0", port=8000)
        server = uvicorn.Server(config)
        await server.serve()

if __name__ == "__main__":
    import uvicorn
    asyncio.run(main())