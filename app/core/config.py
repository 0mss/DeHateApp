from dotenv import load_dotenv
import os

# Carrega variáveis do .env local (opcional, útil no dev local)
load_dotenv()

### YouTube Configs

# Escopos necessários
SCOPES = [
    "https://www.googleapis.com/auth/youtube",
    "https://www.googleapis.com/auth/youtube.force-ssl"
]

# Callback URI
REDIRECT_URI = os.getenv("REDIRECT_URI")

# Variável global para armazenar credenciais do usuário
# Dispensável para aplicações com persistência
user_credentials = None


### Gemini Configs

# Chave da API
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Modelo de LLM utilizado
LLM_MODEL = "gemini-1.5-flash"


### FrontEnd Configs

FRONTEND_URL = os.getenv("FRONTEND_URL")
