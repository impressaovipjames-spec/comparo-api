from .supabase_client import get_supabase
from .models.alerta import AlertaCreate
from typing import List, Dict

class AlertService:
    @staticmethod
    def criar_alerta(alerta: AlertaCreate) -> Dict:
        supabase = get_supabase()
        data = alerta.model_dump()
        # Converte UUID para string se necessário ou deixa o Supabase lidar
        response = supabase.table("alertas").insert(data).execute()
        return response.data[0] if response.data else {}

    @staticmethod
    def listar_alertas(device_id: str) -> List[Dict]:
        supabase = get_supabase()
        response = supabase.table("alertas") \
            .select("*") \
            .eq("device_id", device_id) \
            .eq("status", "ativo") \
            .execute()
        return response.data

    @staticmethod
    def excluir_alerta(alerta_id: str) -> bool:
        supabase = get_supabase()
        response = supabase.table("alertas") \
            .delete() \
            .eq("id", alerta_id) \
            .execute()
        return len(response.data) > 0
