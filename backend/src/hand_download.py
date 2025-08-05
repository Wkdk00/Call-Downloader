from httpx import AsyncClient
from src.models import Files
from src.database import SessionLocal

async def download_and_store_file(url: str, call_id: str, agent_id: str, event_time: str) -> bool:
    db = SessionLocal()
    try:
        async with AsyncClient() as client:
            response = await client.get(url)
            response.raise_for_status()


        file_record = Files(
            fileId=call_id,
            filedata=response.content,
            date=event_time,
            agentId=agent_id
        )
        db.add(file_record)
        db.commit()
        return True
    except Exception as e:
        print(f"Download and store failed: {e}")
        db.rollback()
        return False
    finally:
        db.close()