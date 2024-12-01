from pathlib import Path
import sys
from fastapi import FastAPI
from contextlib import asynccontextmanager
from config import init_db, close_db
from routes import user_routes, chat_routes
import uvicorn
from dotenv import load_dotenv
import os

load_dotenv()
service_url = os.getenv("Service_URL")
host = service_url.split("://")[1].split(":")[0]
port = int(service_url.split(":")[-1])

project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield
    await close_db()

app = FastAPI(
    title="Service",
    lifespan=lifespan,
)

app.post("/users/register")(user_routes.register_user)
app.post("/users/login")(user_routes.login_user)
app.post("/chat/sessions")(chat_routes.create_session)
app.post("/chat/send")(chat_routes.send_message)
app.get("/chat/sessions/{user_id}")(chat_routes.user_sessions)
app.websocket("/ws/{user_id}/{session_id}")(chat_routes.websocket_endpoint)

if __name__ == "__main__":
    uvicorn.run(
        "main:app", 
        host=host, 
        port=port,
        reload=True
    )