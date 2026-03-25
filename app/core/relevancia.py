def validar_relevancia(titulo: str, query: str) -> bool:
    """
    Valida se o produto encontrado é realmente o que o usuário buscou.
    Foca em tokens críticos (modelos numéricos) e bloqueia variantes indesejadas.
    """
    titulo_l = titulo.lower()
    query_l = query.lower()

    # 1. Identificar tokens críticos (ex: 5500, 4060, 1tb)
    # São tokens que contêm números e são fundamentais para o modelo
    tokens_criticos = [t for t in query_l.split() if any(c.isdigit() for c in t)]

    for token in tokens_criticos:
        if token not in titulo_l:
            return False

    # 2. Bloquear variantes não solicitadas (ex: se buscou 5500, não mostrar 5500x3d)
    # Lista de modificadores que alteram drasticamente o produto/preço
    modificadores = ["x3d", "xt", "ti", "super", "ultra", "max", "plus", "pro", "mini"]

    for mod in modificadores:
        # Se o modificador está no título MAS não estava na busca do usuário, é irrelevante
        if mod in titulo_l and mod not in query_l:
            return False

    return True
