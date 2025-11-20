import 'package:flutter/foundation.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'api_service.dart';

class AuthService extends ChangeNotifier {
  bool _isAuthenticated = false;
  String? _token;
  String? _userId;
  String? _userName;
  String? _userEmail;

  bool get isAuthenticated => _isAuthenticated;
  String? get token => _token;
  String? get userId => _userId;
  String? get userName => _userName;
  String? get userEmail => _userEmail;

  final ApiService _apiService = ApiService();

  AuthService() {
    _loadAuthState();
  }

  Future<void> _loadAuthState() async {
    final prefs = await SharedPreferences.getInstance();
    final savedToken = prefs.getString('token');
    _token = savedToken?.trim();
    _userId = prefs.getString('userId');
    _userName = prefs.getString('userName');
    _userEmail = prefs.getString('userEmail');
    _isAuthenticated = _token != null && _token!.isNotEmpty;
    notifyListeners();
  }

  Future<void> login(String email, String password) async {
    try {
      final response = await _apiService.login(email, password);
      
      final token = response['access_token'] as String?;
      final user = response['user'] as Map<String, dynamic>?;
      
      if (token == null || user == null) {
        throw Exception('استجابة غير صحيحة من السيرفر');
      }
      
      _token = token;
      _userId = user['id']?.toString() ?? '';
      _userName = user['name'] as String? ?? '';
      _userEmail = user['email'] as String? ?? '';
      _isAuthenticated = true;

      final prefs = await SharedPreferences.getInstance();
      await prefs.setString('token', _token!);
      await prefs.setString('userId', _userId!);
      await prefs.setString('userName', _userName!);
      await prefs.setString('userEmail', _userEmail!);

      notifyListeners();
    } catch (e) {
      _isAuthenticated = false;
      notifyListeners();
      rethrow;
    }
  }

  Future<void> register(String name, String email, String password) async {
    try {
      final response = await _apiService.register(name, email, password);
      
      final token = response['access_token'] as String?;
      final user = response['user'] as Map<String, dynamic>?;
      
      if (token == null || user == null) {
        throw Exception('استجابة غير صحيحة من السيرفر');
      }
      
      // تنظيف الـ token من المسافات
      _token = token.trim();
      _userId = user['id']?.toString() ?? '';
      _userName = user['name'] as String? ?? '';
      _userEmail = user['email'] as String? ?? '';
      _isAuthenticated = true;

      // Debug logging
      print('✅ [AUTH] Login successful');
      print('🔑 [AUTH] Token saved (length: ${_token!.length})');
      print('🔑 [AUTH] Token preview: ${_token!.substring(0, _token!.length > 30 ? 30 : _token!.length)}...');

      final prefs = await SharedPreferences.getInstance();
      await prefs.setString('token', _token!);
      await prefs.setString('userId', _userId!);
      await prefs.setString('userName', _userName!);
      await prefs.setString('userEmail', _userEmail!);

      notifyListeners();
    } catch (e) {
      _isAuthenticated = false;
      notifyListeners();
      rethrow;
    }
  }

  Future<void> logout() async {
    _token = null;
    _userId = null;
    _userName = null;
    _userEmail = null;
    _isAuthenticated = false;

    final prefs = await SharedPreferences.getInstance();
    await prefs.remove('token');
    await prefs.remove('userId');
    await prefs.remove('userName');
    await prefs.remove('userEmail');

    notifyListeners();
  }
}

