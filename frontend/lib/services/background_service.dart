import 'package:workmanager/workmanager.dart';
import 'api_service.dart';
import 'package:shared_preferences/shared_preferences.dart';

@pragma('vm:entry-point')
void callbackDispatcher() {
  Workmanager().executeTask((task, inputData) async {
    print("Background Task executando: $task");
    
    try {
      final prefs = await SharedPreferences.getInstance();
      // Em um cenário real, pegaríamos o deviceId real aqui
      final String deviceId = "dummy_device_id"; 
      
      final apiService = ApiService();
      final result = await apiService.buscarAlertasDisparados(deviceId);
      
      if (result['results'] != null && (result['results'] as List).isNotEmpty) {
        print("Alertas disparados encontrados! Verificando notificações locais...");
        // Aqui dispararíamos uma notificação local se necessário
      }
    } catch (e) {
      print("Erro na tarefa de background: $e");
    }

    return Future.value(true);
  });
}

class BackgroundService {
  static Future<void> initBackgroundService() async {
    await Workmanager().initialize(
      callbackDispatcher,
      isInDebugMode: true // Remover em produção
    );

    await Workmanager().registerPeriodicTask(
      "1",
      "verificarAlertasPeriodico",
      frequency: const Duration(minutes: 15),
    );
  }
}
