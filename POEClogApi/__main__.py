import os

import uvicorn

HOST = os.getenv("HOST") or "0.0.0.0"
PORT = os.getenv("PORT") or 5000


if __name__ == "__main__":
    uvicorn.run("POEClogApi.api:app", host=HOST, port=PORT, log_level="info")
