from fastapi import FastAPI
import send_request
from dotenv import load_dotenv
import uvicorn
import os

load_dotenv()
service_url = os.getenv("Connector_URL")
host = service_url.split("://")[1].split(":")[0]
port = int(service_url.split(":")[-1])

app = FastAPI(
    title="Connector",
    debug=True
)

app.post("/chat/send", response_model=str)(send_request.get_response)

if __name__ == "__main__":
    uvicorn.run(app, host=host, port=port)