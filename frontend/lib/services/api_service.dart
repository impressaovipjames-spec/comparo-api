import 'dart:convert';
import 'package:http/http.dart' as http;

class ApiService {
  // Em Produção: https://api.comparo.app
  // Em Desenvolvimento: http://localhost:8000
  static const String baseUrl = "https://comparo-api-y1r8.onrender.com";

  Future<Map<String, dynamic>> buscarProduto(String query, String cep) async {
    final url = Uri.parse('$baseUrl/buscar');
    try {
      final response = await http.post(
        url,
        headers: {'Content-Type': 'application/json'},
        body: json.encode({'query': query, 'cep': cep}),
      );
      if (response.statusCode == 200) {
        return json.decode(response.body);
      } else {
        throw Exception('Falha ao buscar produto: ${response.statusCode}');
      }
    } catch (e) {
      throw Exception('Erro de conexão: $e');
    }
  }

  Future<Map<String, dynamic>> checkHealth() async {
    final url = Uri.parse('$baseUrl/health');
    try {
      final response = await http.get(url);
      if (response.statusCode == 200) {
        return json.decode(response.body);
      } else {
        throw Exception('API indisponível: ${response.statusCode}');
      }
    } catch (e) {
      throw Exception('Erro de conexão: $e');
    }
  }

  Future<Map<String, dynamic>> buscarAlertasDisparados(String deviceId) async {
    final url = Uri.parse('$baseUrl/alertas/$deviceId');
    try {
      final response = await http.get(url);
      if (response.statusCode == 200) {
        return json.decode(response.body);
      } else {
        throw Exception('Falha ao buscar alertas: ${response.statusCode}');
      }
    } catch (e) {
      throw Exception('Erro de conexão: $e');
    }
  }

  Future<Map<String, dynamic>> buscarHistoricoPreco(String query, String loja, {int dias = 30}) async {
    final url = Uri.parse('$baseUrl/historico-preco?query=$query&loja=$loja&dias=$dias');
    try {
      final response = await http.get(url);
      if (response.statusCode == 200) {
        return json.decode(response.body);
      } else {
        throw Exception('Falha ao buscar histórico: ${response.statusCode}');
      }
    } catch (e) {
      throw Exception('Erro de conexão: $e');
    }
  }
}
