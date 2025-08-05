from fastapi import APIRouter
from collections import deque

accept_files = False
hand_mode = False
received_files = deque()
router = APIRouter()

@router.get("/control_data")
async def get_control_data():
    global accept_files, received_files, hand_mode
    return {
        "accept_files": accept_files,
        "hand_mode": hand_mode,
        "received_files": list(received_files)[::-1],
    }

@router.post("/toggle_accept/")
async def toggle_accept():
    global accept_files
    accept_files = not accept_files
    return {"status": "success", "accept_files": accept_files}

@router.post("/toggle_hand_mode")
async def toggle_hand_mode():
    global hand_mode
    hand_mode = not hand_mode
    return {"status": "success", "hand_mode": hand_mode}

def add_received_file(file):
    if len(received_files) >=5:
        received_files.popleft()
        received_files.append(file)
        return
    received_files.append(file)
    return

def get_hand_mode():
    return hand_mode

def get_accept_files():
    return accept_files