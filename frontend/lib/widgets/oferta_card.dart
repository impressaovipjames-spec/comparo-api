import 'package:flutter/material.dart';
import 'package:url_launcher/url_launcher.dart';
import 'badge_analise_preco.dart';

class OfertaCard extends StatelessWidget {
  final Map<String, dynamic> offer;
  final bool isBestOffer;

  const OfertaCard({
    super.key,
    required this.offer,
    this.isBestOffer = false,
  });

  Future<void> _abrirLink(String? url) async {
    if (url == null || url.isEmpty) return;
    
    // Tracking no Backend (Sprint 14)
    final String baseUrl = "http://localhost:8000/click"; // TODO: Usar variável global
    final String trackingUrl = "$baseUrl?produto=${Uri.encodeComponent(offer['titulo'])}&loja=${Uri.encodeComponent(offer['loja'])}&link=${Uri.encodeComponent(url)}";
    
    final uri = Uri.parse(trackingUrl);
    if (await canLaunchUrl(uri)) {
      await launchUrl(uri, mode: LaunchMode.externalApplication);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Card(
      margin: const EdgeInsets.only(bottom: 16),
      elevation: isBestOffer ? 6 : 2,
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(15),
        side: isBestOffer 
            ? const BorderSide(color: Colors.orange, width: 2) 
            : BorderSide.none,
      ),
      child: Stack(
        children: [
          Padding(
            padding: const EdgeInsets.all(16.0),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                if (isBestOffer) const SizedBox(height: 10),
                Text(
                  offer['titulo'],
                  style: const TextStyle(
                    fontSize: 18,
                    fontWeight: FontWeight.bold,
                  ),
                  maxLines: 2,
                  overflow: TextOverflow.ellipsis,
                ),
                const SizedBox(height: 8),
                Row(
                  children: [
                    const Icon(Icons.store, size: 16, color: Colors.indigo),
                    const SizedBox(width: 4),
                    Text(
                      offer['loja'],
                      style: const TextStyle(
                        color: Colors.indigo,
                        fontWeight: FontWeight.w600,
                      ),
                    ),
                    const Spacer(),
                    _buildReputationBadge(offer['reputacao']),
                  ],
                ),
                const Divider(height: 32),
                Row(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  children: [
                    Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(
                          "Preço: R\$ ${offer['preco_produto'].toStringAsFixed(2)}",
                          style: const TextStyle(color: Colors.grey),
                        ),
                        Text(
                          "Frete: ${offer['frete'] == 0 ? 'GRÁTIS' : 'R\$ ' + offer['frete'].toStringAsFixed(2)}",
                          style: TextStyle(
                            color: offer['frete'] == 0 ? Colors.green : Colors.grey,
                            fontWeight: offer['frete'] == 0 ? FontWeight.bold : FontWeight.normal,
                          ),
                        ),
                        Text(
                          "Prazo: ${offer['prazo_dias']} dias",
                          style: const TextStyle(color: Colors.grey),
                        ),
                      ],
                    ),
                    Column(
                      crossAxisAlignment: CrossAxisAlignment.end,
                      children: [
                        const Text(
                          "TOTAL REAL",
                          style: TextStyle(fontSize: 10, color: Colors.grey, letterSpacing: 1),
                        ),
                        Text(
                          "R\$ ${offer['total_real'].toStringAsFixed(2)}",
                          style: const TextStyle(
                            fontSize: 24,
                            fontWeight: FontWeight.bold,
                            color: Colors.green,
                          ),
                        ),
                        if (offer['analise_preco'] != null)
                          Padding(
                            padding: const EdgeInsets.only(top: 8.0),
                            child: BadgeAnalisePreco(
                              analise: offer['analise_preco'],
                              productQuery: offer['titulo'],
                              loja: offer['loja'],
                            ),
                          ),
                      ],
                    ),
                  ],
                ),
                const SizedBox(height: 20),
                SizedBox(
                  width: double.infinity,
                  height: 45,
                  child: ElevatedButton(
                    onPressed: () => _abrirLink(offer['link_compra']),
                    style: ElevatedButton.styleFrom(
                      backgroundColor: isBestOffer ? Colors.orange : Colors.indigo,
                      foregroundColor: Colors.white,
                      shape: RoundedRectangleBorder(
                        borderRadius: BorderRadius.circular(10),
                      ),
                    ),
                    child: const Text(
                      'IR COMPRAR',
                      style: TextStyle(fontWeight: FontWeight.bold),
                    ),
                  ),
                ),
              ],
            ),
          ),
          if (isBestOffer)
            Positioned(
              top: 0,
              right: 20,
              child: Container(
                padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
                decoration: const BoxDecoration(
                  color: Colors.orange,
                  borderRadius: BorderRadius.only(
                    bottomLeft: Radius.circular(10),
                    bottomRight: Radius.circular(10),
                  ),
                ),
                child: const Text(
                  'MELHOR OFERTA',
                  style: TextStyle(
                    color: Colors.white,
                    fontWeight: FontWeight.bold,
                    fontSize: 12,
                  ),
                ),
              ),
            ),
        ],
      ),
    );
  }

  Widget _buildReputationBadge(dynamic reputation) {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 2),
      decoration: BoxDecoration(
        color: Colors.amber.shade100,
        borderRadius: BorderRadius.circular(5),
      ),
      child: Row(
        children: [
          const Icon(Icons.star, size: 14, color: Colors.orange),
          const SizedBox(width: 4),
          Text(
            reputation.toString(),
            style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 12),
          ),
        ],
      ),
    );
  }
}
