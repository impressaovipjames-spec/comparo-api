import firebase_admin
from firebase_admin import credentials
import os

def init_firebase():
    """Inicializa o SDK do Firebase Admin se ainda não estiver inicializado."""
    if not firebase_admin._apps:
        cred_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'firebase_credentials.json')
        if os.path.exists(cred_path):
            try:
                cred = credentials.Certificate(cred_path)
                firebase_admin.initialize_app(cred)
                print("Firebase Admin SDK inicializado com sucesso.")
            except Exception as e:
                print(f"Erro ao inicializar Firebase: {e}")
        else:
            print(f"AVISO: Arquivo de credenciais não encontrado em {cred_path}. Notificações Push não funcionarão.")
