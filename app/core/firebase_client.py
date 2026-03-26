import firebase_admin
from firebase_admin import credentials
import os

def init_firebase():
    """Inicializa o SDK do Firebase Admin se ainda não estiver inicializado."""
    if not firebase_admin._apps:
        # 1. Tentar ler das Variáveis de Ambiente primeiro (Produção/Render)
        private_key = os.environ.get("FIREBASE_PRIVATE_KEY")
        if private_key:
            # Correção crítica para plataformas Cloud (Render/Heroku/Vercel)
            private_key = private_key.replace('\\n', '\n')
            
            cert_dict = {
                "type": os.environ.get("FIREBASE_TYPE", "service_account"),
                "project_id": os.environ.get("FIREBASE_PROJECT_ID", "comparo"),
                "private_key_id": os.environ.get("FIREBASE_PRIVATE_KEY_ID", ""),
                "private_key": private_key,
                "client_email": os.environ.get("FIREBASE_CLIENT_EMAIL", ""),
                "client_id": os.environ.get("FIREBASE_CLIENT_ID", ""),
                "auth_uri": os.environ.get("FIREBASE_AUTH_URI", "https://accounts.google.com/o/oauth2/auth"),
                "token_uri": os.environ.get("FIREBASE_TOKEN_URI", "https://oauth2.googleapis.com/token"),
                "auth_provider_x509_cert_url": os.environ.get("FIREBASE_AUTH_PROVIDER_X509_CERT_URL", "https://www.googleapis.com/oauth2/v1/certs"),
                "client_x509_cert_url": os.environ.get("FIREBASE_CLIENT_X509_CERT_URL", "")
            }
            try:
                cred = credentials.Certificate(cert_dict)
                firebase_admin.initialize_app(cred)
                print("Firebase Admin SDK inicializado com sucesso via Variáveis de Ambiente.")
                return
            except Exception as e:
                print(f"Erro ao inicializar Firebase via ENV: {e}")

        # 2. Fallback para arquivo JSON local (Desenvolvimento)
        cred_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'firebase_credentials.json')
        if os.path.exists(cred_path):
            try:
                cred = credentials.Certificate(cred_path)
                firebase_admin.initialize_app(cred)
                print("Firebase Admin SDK inicializado com sucesso via JSON local.")
            except Exception as e:
                print(f"Erro ao inicializar Firebase via JSON: {e}")
        else:
            print("AVISO: Credenciais do Firebase não encontradas (nem ENV, nem JSON). Push não funcionará.")
