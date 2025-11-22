from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dishka.integrations.fastapi import setup_dishka

from src.api.complaints import router as complaints_router
from src.api.ws import router as ws_router
from src.api.tickets_front import router as tickets_front_router
from src.di.container import container
from src.db.session import engine
from src.db.base import Base


@asynccontextmanager
async def lifespan(app: FastAPI):
    # ✅ код старта
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    # можно тут же подгрузить справочники, категории, сервисы и т.п.

    yield

    # ✅ код остановки (опционально)
    await engine.dispose()


app = FastAPI(
    title="Lobachevsky Portal",
    lifespan=lifespan,
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # под фронт поправишь
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

setup_dishka(container, app)

app.include_router(complaints_router)
app.include_router(ws_router)
app.include_router(tickets_front_router)
