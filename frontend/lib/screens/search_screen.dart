import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';
import '../services/api_service.dart';
import 'results_screen.dart';

class SearchScreen extends StatefulWidget {
  const SearchScreen({super.key});

  @override
  State<SearchScreen> createState() => _SearchScreenState();
}

class _SearchScreenState extends State<SearchScreen> {
  final TextEditingController _productController = TextEditingController();
  final TextEditingController _cepController = TextEditingController();
  final ApiService _apiService = ApiService();
  bool _isLoading = false;
  List<String> _history = [];

  @override
  void initState() {
    super.initState();
    _loadHistory();
  }

  Future<void> _loadHistory() async {
    final prefs = await SharedPreferences.getInstance();
    setState(() {
      _history = prefs.getStringList('search_history') ?? [];
    });
  }

  Future<void> _saveToHistory(String query) async {
    if (query.isEmpty) return;
    final prefs = await SharedPreferences.getInstance();
    List<String> currentHistory = prefs.getStringList('search_history') ?? [];
    
    currentHistory.remove(query);
    currentHistory.insert(0, query);
    
    if (currentHistory.length > 10) {
      currentHistory = currentHistory.sublist(0, 10);
    }
    
    await prefs.setStringList('search_history', currentHistory);
    setState(() {
      _history = currentHistory;
    });
  }

  String? _validateCep(String value) {
    String cleanCep = value.replaceAll('-', '').trim();
    if (cleanCep.length != 8 || int.tryParse(cleanCep) == null) {
      return "CEP inválido (8 dígitos)";
    }
    return null;
  }

  void _buscar() async {
    final String product = _productController.text;
    final String rawCep = _cepController.text;
    final String? cepError = _validateCep(rawCep);

    if (product.isEmpty || rawCep.isEmpty) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Preencha os campos para buscar')),
      );
      return;
    }

    if (cepError != null) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text(cepError), backgroundColor: Colors.red),
      );
      return;
    }

    String cleanCep = rawCep.replaceAll('-', '').trim();

    setState(() => _isLoading = true);

    try {
      final result = await _apiService.buscarProduto(product, cleanCep);
      await _saveToHistory(product);
      
      if (!mounted) return;
      
      Navigator.push(
        context,
        MaterialPageRoute(
          builder: (context) => ResultsScreen(
            offers: result['results'],
            query: product,
          ),
        ),
      );
    } catch (e) {
      if (!mounted) return;
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text("Erro: $e")),
      );
    } finally {
      if (mounted) setState(() => _isLoading = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('COMPARÔ'),
        centerTitle: true,
        backgroundColor: Colors.indigo,
        foregroundColor: Colors.white,
      ),
      body: SingleChildScrollView(
        child: Padding(
          padding: const EdgeInsets.all(20.0),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              const Text(
                'O que você deseja comprar?',
                style: TextStyle(fontSize: 22, fontWeight: FontWeight.bold),
              ),
              const SizedBox(height: 20),
              TextField(
                controller: _productController,
                decoration: InputDecoration(
                  labelText: 'Produto (ex: iPhone 15)',
                  border: OutlineInputBorder(borderRadius: BorderRadius.circular(10)),
                  prefixIcon: const Icon(Icons.search),
                ),
              ),
              const SizedBox(height: 15),
              TextField(
                controller: _cepController,
                decoration: InputDecoration(
                  labelText: 'Seu CEP',
                  border: OutlineInputBorder(borderRadius: BorderRadius.circular(10)),
                  prefixIcon: const Icon(Icons.location_on),
                  hintText: '00000-000',
                ),
                keyboardType: TextInputType.number,
              ),
              const SizedBox(height: 25),
              SizedBox(
                width: double.infinity,
                height: 55,
                child: ElevatedButton(
                  onPressed: _isLoading ? null : _buscar,
                  style: ElevatedButton.styleFrom(
                    backgroundColor: Colors.indigo,
                    foregroundColor: Colors.white,
                    shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(10)),
                  ),
                  child: _isLoading
                      ? const CircularProgressIndicator(color: Colors.white)
                      : const Text('BUSCAR MELHORES OFERTAS', style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold)),
                ),
              ),
              if (_history.isNotEmpty) ...[
                const SizedBox(height: 40),
                const Text('Buscas recentes', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
                const SizedBox(height: 10),
                Wrap(
                  spacing: 10,
                  children: _history.map((q) => ActionChip(
                    label: Text(q),
                    onPressed: () => _productController.text = q,
                  )).toList(),
                ),
              ],
            ],
          ),
        ),
      ),
    );
  }
}
