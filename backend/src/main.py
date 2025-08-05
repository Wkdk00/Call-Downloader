import asyncio
from fastapi import FastAPI
from src.auth import router as auth_router
from src.middleware import setup_middlewares
from src.api_params import router as params_router
from src.control_page import router as control_router
from src.rabbitmq import router as rabbit_router, broker as RabbitBroker

app = FastAPI()
app.include_router(auth_router)
app.include_router(rabbit_router)
app.include_router(params_router)
app.include_router(control_router)
setup_middlewares(app)

async def main() -> None:
    async with RabbitBroker:
        await RabbitBroker.start()
        config = uvicorn.Config(app, host="0.0.0.0", port=8000)
        server = uvicorn.Server(config)
        await server.serve()

if __name__ == "__main__":
    import uvicorn
    asyncio.run(main())