import 'package:flutter/material.dart';
import 'package:fl_chart/fl_chart.dart';
import 'package:intl/intl.dart';
import '../services/api_service.dart';

class HistoricoPrecoScreen extends StatefulWidget {
  final String query;
  final String loja;

  const HistoricoPrecoScreen({super.key, required this.query, required this.loja});

  @override
  State<HistoricoPrecoScreen> createState() => _HistoricoPrecoScreenState();
}

class _HistoricoPrecoScreenState extends State<HistoricoPrecoScreen> {
  final ApiService _apiService = ApiService();
  List<dynamic> _historyData = [];
  bool _isLoading = true;
  double _minPrice = 0;
  double _maxPrice = 0;
  double _avgPrice = 0;

  @override
  void initState() {
    super.initState();
    _fetchHistory();
  }

  Future<void> _fetchHistory() async {
    try {
      final data = await _apiService.buscarHistoricoPreco(widget.query, widget.loja);
      if (mounted) {
        setState(() {
          _historyData = data['results'] ?? [];
          if (_historyData.isNotEmpty) {
            final prices = _historyData.map((e) => (e['preco_total'] as num).toDouble()).toList();
            _minPrice = prices.reduce((a, b) => a < b ? a : b);
            _maxPrice = prices.reduce((a, b) => a > b ? a : b);
            _avgPrice = prices.reduce((a, b) => a + b) / prices.length;
          }
          _isLoading = false;
        });
      }
    } catch (e) {
      if (mounted) {
        setState(() => _isLoading = false);
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('Erro ao carregar histórico: $e')),
        );
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Histórico de Preço'),
        backgroundColor: Colors.indigo,
        foregroundColor: Colors.white,
      ),
      body: _isLoading
          ? const Center(child: CircularProgressIndicator())
          : _historyData.isEmpty
              ? const Center(child: Text('Nenhum dado histórico encontrado.'))
              : SingleChildScrollView(
                  padding: const EdgeInsets.all(16.0),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(
                        widget.query,
                        style: const TextStyle(fontSize: 22, fontWeight: FontWeight.bold),
                      ),
                      Text(
                        widget.loja,
                        style: const TextStyle(fontSize: 16, color: Colors.indigo),
                      ),
                      const SizedBox(height: 30),
                      _buildChart(),
                      const SizedBox(height: 40),
                      _buildSummaryCard(),
                    ],
                  ),
                ),
    );
  }

  Widget _buildChart() {
    return SizedBox(
      height: 300,
      width: double.infinity,
      child: LineChart(
        LineChartData(
          gridData: const FlGridData(show: true, drawVerticalLine: false),
          titlesData: FlTitlesData(
            leftTitles: const AxisTitles(sideTitles: SideTitles(showTitles: false)),
            topTitles: const AxisTitles(sideTitles: SideTitles(showTitles: false)),
            rightTitles: const AxisTitles(
              sideTitles: SideTitles(showTitles: true, reservedSize: 45),
            ),
            bottomTitles: AxisTitles(
              sideTitles: SideTitles(
                showTitles: true,
                getTitlesWidget: (value, meta) {
                  if (value.toInt() >= 0 && value.toInt() < _historyData.length) {
                    if (value.toInt() % 5 == 0 || value.toInt() == _historyData.length - 1) {
                      final dateStr = _historyData[value.toInt()]['coletado_em'];
                      final date = DateTime.parse(dateStr);
                      return Padding(
                        padding: const EdgeInsets.only(top: 8.0),
                        child: Text(DateFormat('dd/MM').format(date), style: const TextStyle(fontSize: 10)),
                      );
                    }
                  }
                  return const Text('');
                },
              ),
            ),
          ),
          borderData: FlBorderData(show: true, border: Border.all(color: Colors.grey.shade300)),
          minY: _minPrice * 0.95,
          maxY: _maxPrice * 1.05,
          lineBarsData: [
            LineChartBarData(
              spots: _historyData.asMap().entries.map((e) {
                return FlSpot(e.key.toDouble(), (e.value['preco_total'] as num).toDouble());
              }).toList(),
              isCurved: true,
              color: Colors.indigo,
              barWidth: 3,
              isStrokeCapRound: true,
              dotData: const FlDotData(show: false),
              belowBarData: BarAreaData(
                show: true,
                color: Colors.indigo.withOpacity(0.1),
              ),
            ),
            // Linha de Média
            LineChartBarData(
              spots: [
                FlSpot(0, _avgPrice),
                FlSpot((_historyData.length - 1).toDouble(), _avgPrice),
              ],
              isCurved: false,
              color: Colors.orange.withOpacity(0.5),
              barWidth: 1,
              dashArray: [5, 5],
              dotData: const FlDotData(show: false),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildSummaryCard() {
    return Card(
      elevation: 0,
      color: Colors.grey.shade100,
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(15)),
      child: Padding(
        padding: const EdgeInsets.all(20.0),
        child: Column(
          children: [
            _buildSummaryRow("Média do período", "R\$ ${_avgPrice.toStringAsFixed(2)}", Colors.black),
            const Divider(),
            _buildSummaryRow("Menor preço", "R\$ ${_minPrice.toStringAsFixed(2)}", Colors.green),
            const Divider(),
            _buildSummaryRow("Maior preço", "R\$ ${_maxPrice.toStringAsFixed(2)}", Colors.red),
          ],
        ),
      ),
    );
  }

  Widget _buildSummaryRow(String label, String value, Color color) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 8),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: [
          Text(label, style: const TextStyle(fontSize: 16)),
          Text(value, style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold, color: color)),
        ],
      ),
    );
  }
}
