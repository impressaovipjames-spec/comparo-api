import 'package:flutter/material.dart';
import '../screens/historico_preco_screen.dart';

class BadgeAnalisePreco extends StatelessWidget {
  final Map<String, dynamic> analise;
  final String productQuery;
  final String loja;

  const BadgeAnalisePreco({
    super.key, 
    required this.analise,
    required this.productQuery,
    required this.loja,
  });

  @override
  Widget build(BuildContext context) {
    final String status = analise['status'] ?? 'SEM_HISTORICO';
    final String label = analise['badge_ui'] ?? 'Sem dados';
    final String colorStr = analise['badge_cor'] ?? 'grey';

    return GestureDetector(
      onTap: () => _mostrarDetalhes(context),
      child: Container(
        padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 6),
        decoration: BoxDecoration(
          color: _getCor(colorStr).withOpacity(0.1),
          borderRadius: BorderRadius.circular(20),
          border: Border.all(color: _getCor(colorStr), width: 1),
        ),
        child: Row(
          mainAxisSize: MainAxisSize.min,
          children: [
            Icon(_getIcon(status), size: 16, color: _getCor(colorStr)),
            const SizedBox(width: 6),
            Text(
              label,
              style: TextStyle(
                color: _getCor(colorStr),
                fontSize: 12,
                fontWeight: FontWeight.bold,
              ),
            ),
          ],
        ),
      ),
    );
  }

  Color _getCor(String colorStr) {
    switch (colorStr) {
      case 'red': return Colors.red;
      case 'green': return Colors.green;
      case 'amber': return Colors.orange;
      case 'purple': return Colors.purple;
      case 'blue': return Colors.blue;
      default: return Colors.grey;
    }
  }

  IconData _getIcon(String status) {
    switch (status) {
      case 'MENOR_HISTORICO': return Icons.verified_user;
      case 'DESCONTO_REAL': return Icons.verified;
      case 'INFLADO': return Icons.warning_amber_rounded;
      case 'ESTAVEL': return Icons.trending_flat;
      default: return Icons.help_outline;
    }
  }

  void _mostrarDetalhes(BuildContext context) {
    showModalBottomSheet(
      context: context,
      shape: const RoundedRectangleBorder(
        borderRadius: BorderRadius.vertical(top: Radius.circular(20)),
      ),
      builder: (context) {
        return Padding(
          padding: const EdgeInsets.all(24.0),
          child: Column(
            mainAxisSize: MainAxisSize.min,
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Row(
                children: [
                  Icon(_getIcon(analise['status']), color: _getCor(analise['badge_cor']), size: 28),
                  const SizedBox(width: 12),
                  Text(
                    analise['badge_ui'],
                    style: const TextStyle(fontSize: 20, fontWeight: FontWeight.bold),
                  ),
                ],
              ),
              const SizedBox(height: 20),
              _buildInfoRow("Variação Médica", "${analise['variacao_percentual']}%"),
              _buildInfoRow("Preço Médio (30 dias)", "R\$ ${analise['preco_medio_30d']}"),
              _buildInfoRow("Menor Preço (30 dias)", "R\$ ${analise['preco_minimo_30d']}"),
              if (analise['data_comercial'] != null) ...[
                const SizedBox(height: 16),
                Container(
                  padding: const EdgeInsets.all(12),
                  decoration: BoxDecoration(
                    color: Colors.amber.shade50,
                    borderRadius: BorderRadius.circular(10),
                    border: Border.all(color: Colors.amber.shade200),
                  ),
                  child: Row(
                    children: [
                      const Icon(Icons.event, color: Colors.orange),
                      const SizedBox(width: 8),
                      Expanded(
                        child: Text(
                          "Atenção: Estamos próximos de uma data comercial. O app está monitorando variações de preço.",
                          style: TextStyle(color: Colors.orange.shade900, fontSize: 13),
                        ),
                      ),
                    ],
                  ),
                ),
              ],
              const SizedBox(height: 24),
              const Text(
                "Nossa análise é baseada nos snapshots diários de preços dos últimos 30 dias para esta loja específica.",
                style: TextStyle(color: Colors.grey, fontSize: 12, fontStyle: FontStyle.italic),
              ),
              const SizedBox(height: 16),
              SizedBox(
                width: double.infinity,
                child: ElevatedButton.icon(
                  onPressed: () {
                    Navigator.pop(context); // Fecha o modal
                    Navigator.push(
                      context,
                      MaterialPageRoute(
                        builder: (context) => HistoricoPrecoScreen(
                          query: productQuery,
                          loja: loja,
                        ),
                      ),
                    );
                  },
                  icon: const Icon(Icons.show_chart),
                  label: const Text("VER HISTÓRICO COMPLETO"),
                  style: ElevatedButton.styleFrom(
                    backgroundColor: Colors.indigo,
                    foregroundColor: Colors.white,
                    padding: const EdgeInsets.symmetric(vertical: 12),
                  ),
                ),
              ),
            ],
          ),
        );
      },
    );
  }

  Widget _buildInfoRow(String label, String value) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 4),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: [
          Text(label, style: const TextStyle(color: Colors.grey)),
          Text(value, style: const TextStyle(fontWeight: FontWeight.bold)),
        ],
      ),
    );
  }
}
