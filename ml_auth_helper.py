import httpx
import asyncio
import urllib.parse

# Configurações
APP_ID = "6744427811164510"
SECRET_KEY = "7cqvhfV1gqoISKiwIzyEUDd2vRH6ZSkt"
REDIRECT_URI = "https://comparo-api-y1r8.onrender.com/callback"

async def main():
    if APP_ID == "6744427811164510":
        print("❌ ERRO: Você esqueceu de colocar o APP_ID e SECRET_KEY dentro deste arquivo!")
        return

    auth_url = f"https://auth.mercadolivre.com.br/authorization?response_type=code&client_id={APP_ID}&redirect_uri={REDIRECT_URI}"
    
    print("="*60)
    print(" PASSO 1 - CLIQUE NESTE LINK PARA AUTORIZAR:")
    print("="*60)
    print(auth_url)
    print("="*60)
    print("\nDepois de autorizar, a página vai dar 'Not Found'. É NORMAL!")
    print("Vá na barra de endereços do navegador e copie o CÓDIGO que aparece depois de '?code='")
    print("Exemplo: https://comparo-api.../callback?code=TG-xxxxx-1234")
    print("Você deve copiar APENAS a parte TG-xxxxx-1234\n")
    
    code = input(" Cole o seu código aqui e aperte ENTER: ").strip()
    
    if not code:
        print("Código vazio!")
        return
        
    print("\nGerando tokens VIP...")
    token_url = "https://api.mercadolibre.com/oauth/token"
    payload = {
        "grant_type": "authorization_code",
        "client_id": APP_ID,
        "client_secret": SECRET_KEY,
        "code": code,
        "redirect_uri": REDIRECT_URI
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.post(token_url, data=payload)
        
    if response.status_code == 200:
        data = response.json()
        print("\n" + "="*60)
        print("✅ SUCESSO! SEUS TOKENS FORAM GERADOS:")
        print("="*60)
        print("ACCESS_TOKEN:", data.get("access_token"))
        print("-" * 60)
        print("REFRESH_TOKEN:", data.get("refresh_token"))
        print("="*60)
        print("👉 Envie o REFRESH_TOKEN no chat para o assistente!")
        with open(".env.ml_tokens", "w") as f:
            f.write(f"ML_ACCESS_TOKEN={data.get('access_token')}\n")
            f.write(f"ML_REFRESH_TOKEN={data.get('refresh_token')}\n")
    else:
        print("\n❌ Falha ao obter token. Veja o erro do Mercado Livre:")
        print(response.text)

if __name__ == "__main__":
    asyncio.run(main())
