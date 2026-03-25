-- SQL para criação da tabela de alertas no Supabase

CREATE TABLE alertas (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    device_id TEXT NOT NULL,
    fcm_token TEXT NOT NULL,
    produto_query TEXT NOT NULL,
    lojas_monitorar TEXT[] NOT NULL,
    preco_alvo DECIMAL,
    queda_percentual DECIMAL,
    preco_referencia DECIMAL NOT NULL,
    status TEXT NOT NULL DEFAULT 'ativo',
    criado_em TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
);

-- Habilitar RLS (Row Level Security) se necessário, ou configurar permissões públicas iniciais
-- ALTER TABLE alertas ENABLE ROW LEVEL SECURITY;

-- Tabela de Histórico de Preços
CREATE TABLE price_history (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    produto_query TEXT NOT NULL,
    loja TEXT NOT NULL,
    preco DECIMAL NOT NULL,
    frete DECIMAL DEFAULT 0,
    preco_total DECIMAL NOT NULL,
    coletado_em DATE DEFAULT CURRENT_DATE NOT NULL,
    produto_id_externo TEXT
);

-- Tabela de Rastreamento de Cliques (Monetização)
CREATE TABLE click_tracking (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    produto TEXT NOT NULL,
    loja TEXT NOT NULL,
    device_id TEXT,
    criado_em TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL
);

-- Índice para relatórios de conversão
CREATE INDEX idx_click_tracking_loja ON click_tracking(loja);
