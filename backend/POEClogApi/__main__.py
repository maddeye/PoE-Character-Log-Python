import os

import uvicorn


if __name__ == "__main__":
    uvicorn.run("POEClogApi.api:app", log_level="info")
