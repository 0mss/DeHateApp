from dotenv import load_dotenv
import os

# Carrega .env localmente (ignorado no Railway, mas útil no dev)
load_dotenv()

### YouTube Configs

SCOPES = [
    "https://www.googleapis.com/auth/youtube",
    "https://www.googleapis.com/auth/youtube.force-ssl"
]

REDIRECT_URI = os.getenv("REDIRECT_URI")

# JSON do client OAuth como string (Railway)
GOOGLE_CLIENT_SECRET_JSON = os.getenv("GOOGLE_CLIENT_SECRET_JSON")

user_credentials = None


### Gemini Configs

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
LLM_MODEL = "gemini-1.5-flash"


### FrontEnd Configs

FRONTEND_URL = os.getenv("FRONTEND_URL")
