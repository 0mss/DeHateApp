from dotenv import load_dotenv
import os

# Importando variáveis de ambiente
load_dotenv()


### YouTube Configs
# Arquivo de credenciais
CLIENT_SECRETS_FILE = "client_secret.json"

# Escopos necessários
SCOPES = [
    "https://www.googleapis.com/auth/youtube",
    "https://www.googleapis.com/auth/youtube.force-ssl"
]

# Callback uri
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
