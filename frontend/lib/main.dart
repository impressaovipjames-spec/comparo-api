import 'package:flutter/material.dart';
import 'package:firebase_core/firebase_core.dart';
import 'services/notification_service.dart';
import 'services/background_service.dart';
import 'screens/search_screen.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  
  // Inicialização do Firebase
  try {
    await Firebase.initializeApp();
    await NotificationService.initFirebaseMessaging();
  } catch (e) {
    print("Erro ao inicializar Firebase: $e");
  }

  // Inicialização do Background Service
  try {
    await BackgroundService.initBackgroundService();
  } catch (e) {
    print("Erro ao inicializar Background Service: $e");
  }

  runApp(const ComparoApp());
}

class ComparoApp extends StatelessWidget {
  const ComparoApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Comparô',
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: Colors.indigo),
        useMaterial3: true,
      ),
      debugShowCheckedModeBanner: false,
      home: const SearchScreen(),
    );
  }
}
