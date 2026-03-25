import urllib.parse

class AffiliateService:
    @staticmethod
    def gerar_link_afiliado(link_original: str, loja: str) -> str:
        """
        Recebe um link original e injeta os parâmetros de afiliado conforme a loja.
        """
        if not link_original:
            return ""

        parsed_url = urllib.parse.urlparse(link_original)
        query = urllib.parse.parse_qs(parsed_url.query)

        # Configuração de parâmetros por loja (Sprint 14)
        config = {
            "Mercado Livre": {"utm_source": "comparo"},
            "Amazon": {"tag": "comparo-20"},
            "Magalu": {"utm_source": "comparo"},
            "Shopee": {"smtt": "comparo"}
        }

        if loja in config:
            for key, value in config[loja].items():
                query[key] = [value]

        # Reconstrói a URL
        new_query = urllib.parse.urlencode(query, doseq=True)
        new_url = urllib.parse.ParseResult(
            scheme=parsed_url.scheme,
            netloc=parsed_url.netloc,
            path=parsed_url.path,
            params=parsed_url.params,
            query=new_query,
            fragment=parsed_url.fragment
        ).geturl()

        return new_url
