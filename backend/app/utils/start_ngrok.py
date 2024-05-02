import os
import sys

from pyngrok import ngrok
from pydantic_settings import BaseSettings
from fastapi.logger import logger

def start():
    class Settings(BaseSettings):
        # ... The rest of our FastAPI settings

        BASE_URL: str = "http://localhost:8001"
        USE_NGROK: bool = os.environ.get("USE_NGROK", "False") == "True"


    settings = Settings()


    def init_webhooks(base_url):
        # Update inbound traffic via APIs to use the public-facing ngrok URL
        pass


    if settings.USE_NGROK and os.environ.get("NGROK_AUTHTOKEN"):
        # pyngrok should only ever be installed or initialized in a dev environment when this flag is set
        

        # Get the dev server port (defaults to 8000 for Uvicorn, can be overridden with `--port`
        # when starting the server
        port = sys.argv[sys.argv.index("--port") + 1] if "--port" in sys.argv else "8001"

        # Open a ngrok tunnel to the dev server
        public_url = ngrok.connect(port).public_url
        logger.info(f"ngrok tunnel \"{public_url}\" -> \"http://127.0.0.1:{port}\"")

        # Update any base URLs or webhooks to use the public ngrok URL
        settings.BASE_URL = public_url
        init_webhooks(public_url)



