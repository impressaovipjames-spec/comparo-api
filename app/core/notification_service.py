from firebase_admin import messaging
from .firebase_client import init_firebase

# Garante que o firebase está inicializado
init_firebase()

class NotificationService:
    @staticmethod
    def enviar_alerta_preco(fcm_token: str, titulo_produto: str, preco_atual: float):
        """Envia uma notificação push via FCM sobre queda de preço."""
        mensagem = messaging.Message(
            notification=messaging.Notification(
                title="🔥 ALERTA DE PREÇO",
                body=f"O produto '{titulo_produto}' baixou para R$ {preco_atual:.2f}! Aproveite agora!",
            ),
            token=fcm_token,
            data={
                "type": "price_drop",
                "product": titulo_produto,
                "price": str(preco_atual)
            }
        )
        
        try:
            response = messaging.send(mensagem)
            print(f"Notificação enviada com sucesso: {response}")
            return response
        except Exception as e:
            print(f"Erro ao enviar notificação FCM: {e}")
            return None

    @staticmethod
    def enviar_push_teste(fcm_token: str):
        """Envia uma notificação de teste."""
        mensagem = messaging.Message(
            notification=messaging.Notification(
                title="COMPARÔ - Teste",
                body="Esta é uma notificação de teste do seu assistente de compras.",
            ),
            token=fcm_token,
        )
        try:
            return messaging.send(mensagem)
        except Exception as e:
            print(f"Erro no teste de push: {e}")
            return None
