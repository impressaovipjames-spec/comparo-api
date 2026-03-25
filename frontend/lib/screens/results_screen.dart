import 'package:flutter/material.dart';

import '../widgets/oferta_card.dart';

class ResultsScreen extends StatelessWidget {
  final List<dynamic> offers;
  final String query;

  const ResultsScreen({super.key, required this.offers, required this.query});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Resultados: $query'),
        backgroundColor: Colors.indigo,
        foregroundColor: Colors.white,
        elevation: 0,
      ),
      body: Container(
        color: Colors.grey.shade100,
        child: Padding(
          padding: const EdgeInsets.symmetric(horizontal: 16.0),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              const SizedBox(height: 20),
              Text(
                'Encontramos ${offers.length} opções:',
                style: const TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
              ),
              const SizedBox(height: 16),
              Expanded(
                child: offers.isEmpty
                    ? const Center(child: Text('Nenhuma oferta encontrada.'))
                    : ListView.builder(
                        physics: const BouncingScrollPhysics(),
                        itemCount: offers.length,
                        itemBuilder: (context, index) {
                          return OfertaCard(
                            offer: offers[index],
                            isBestOffer: index == 0,
                          );
                        },
                      ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
