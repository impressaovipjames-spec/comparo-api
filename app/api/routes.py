from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import RedirectResponse
from typing import List, Optional
import json
import os
from datetime import datetime, timedelta

from core.supabase_client import get_supabase
from core.cache import get_cache
from core.models.busca import BuscaRequest
from core.models.oferta import Oferta
from core.models.alerta import AlertaCreate, AlertaRead
from core.search_service import buscar_produto
from core.alert_service import AlertService
from core.notification_service import NotificationService

router = APIRouter()

@router.post("/buscar")
async def buscar(request: BuscaRequest):
    try:
        results = await buscar_produto(request.query, request.cep)
        return {
            "query": request.query,
            "cep": request.cep,
            "results": results
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/alertas")
async def criar_alerta(alerta: AlertaCreate):
    try:
        novo_alerta = AlertService.criar_alerta(alerta)
        return {"status": "sucesso", "alerta": novo_alerta}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/alertas/{device_id}")
async def listar_alertas(device_id: str):
    try:
        alertas = AlertService.listar_alertas(device_id)
        return {"status": "sucesso", "results": alertas}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/alertas/{alerta_id}")
async def excluir_alerta(alerta_id: str):
    try:
        sucesso = AlertService.excluir_alerta(alerta_id)
        if not sucesso:
            raise HTTPException(status_code=404, detail="Alerta não encontrado")
        return {"status": "sucesso", "message": "Alerta excluído"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/test-push")
async def test_push(request: dict):
    fcm_token = request.get("fcm_token")
    if not fcm_token:
        raise HTTPException(status_code=400, detail="fcm_token é obrigatório")
    
    response = NotificationService.enviar_push_teste(fcm_token)
    if response:
        return {"status": "sucesso", "message": "Push de teste enviado", "message_id": response}
    else:
        raise HTTPException(status_code=500, detail="Erro ao enviar push. Verifique se as credenciais do Firebase estão configuradas.")

@router.get("/historico-preco")
async def get_historico(query: str, loja: str, dias: int = 30):
    """
    Retorna o histórico de preços de um produto em uma loja específica.
    """
    try:
        supabase = get_supabase()
        data_limite = (datetime.now() - timedelta(days=dias)).date().isoformat()
        
        response = supabase.table("price_history") \
            .select("*") \
            .eq("produto_query", query) \
            .eq("loja", loja) \
            .gte("coletado_em", data_limite) \
            .order("coletado_em", ascending=True) \
            .execute()
            
        return {
            "status": "sucesso",
            "query": query,
            "loja": loja,
            "results": response.data
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/click")
async def track_click(produto: str, loja: str, link: str, device_id: Optional[str] = None):
    """
    Registra o clique no banco de dados e redireciona para a loja.
    """
    try:
        supabase = get_supabase()
        supabase.table("click_tracking").insert({
            "produto": produto,
            "loja": loja,
            "device_id": device_id
        }).execute()
        
        return RedirectResponse(url=link)
    except Exception as e:
        print(f"Erro ao registrar clique: {e}")
        # Redireciona mesmo em caso de erro no tracking para não quebrar a experiência
        return RedirectResponse(url=link)
