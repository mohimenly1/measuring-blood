import 'dart:convert';
import 'dart:io';
import 'package:http/http.dart' as http;

class ApiService {
  // TODO: Update with your backend URL
  static const String baseUrl = 'http://172.20.10.2:8000/api';

  Future<Map<String, dynamic>> login(String email, String password) async {
    try {
      final response = await http.post(
        Uri.parse('$baseUrl/auth/login'),
        headers: {'Content-Type': 'application/x-www-form-urlencoded'},
        body: 'username=$email&password=$password',
      );

      if (response.statusCode == 200) {
        final data = jsonDecode(response.body) as Map<String, dynamic>;
        // تحويل الاستجابة إلى التنسيق المتوقع
        return {
          'access_token': data['access_token'],
          'token_type': data['token_type'] ?? 'bearer',
          'user': data['user'],
        };
      } else {
        final errorBody = response.body;
        throw Exception('فشل تسجيل الدخول: $errorBody');
      }
    } catch (e) {
      if (e is Exception) {
        rethrow;
      }
      throw Exception('خطأ في الاتصال: $e');
    }
  }

  Future<Map<String, dynamic>> register(
    String name,
    String email,
    String password,
  ) async {
    try {
      final response = await http.post(
        Uri.parse('$baseUrl/auth/register'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({'name': name, 'email': email, 'password': password}),
      );

      if (response.statusCode == 200 || response.statusCode == 201) {
        final data = jsonDecode(response.body) as Map<String, dynamic>;
        // تحويل الاستجابة إلى التنسيق المتوقع
        return {
          'access_token': data['access_token'],
          'token_type': data['token_type'] ?? 'bearer',
          'user': data['user'],
        };
      } else {
        final errorBody = response.body;
        // محاولة استخراج رسالة الخطأ من الاستجابة
        try {
          final errorData = jsonDecode(errorBody) as Map<String, dynamic>;
          final detail = errorData['detail'] as String?;
          throw Exception(detail ?? 'فشل التسجيل');
        } catch (_) {
          throw Exception('فشل التسجيل: $errorBody');
        }
      }
    } catch (e) {
      if (e is Exception) {
        rethrow;
      }
      throw Exception('خطأ في الاتصال: $e');
    }
  }

  Future<Map<String, dynamic>> measureBloodPressure(
    String token,
    File imageFile,
  ) async {
    try {
      // التحقق من أن الـ token موجود وصحيح
      final cleanToken = token.trim();
      if (cleanToken.isEmpty) {
        throw Exception('الـ token غير موجود - يرجى تسجيل الدخول');
      }

      // Debug logging
      print('🔑 [DEBUG] Token length: ${cleanToken.length}');
      print(
        '🔑 [DEBUG] Token preview: ${cleanToken.substring(0, cleanToken.length > 30 ? 30 : cleanToken.length)}...',
      );

      var request = http.MultipartRequest(
        'POST',
        Uri.parse('$baseUrl/measure'),
      );

      // إضافة الـ token في headers (بدون Content-Type لأن MultipartRequest يضيفه تلقائياً)
      request.headers['Authorization'] = 'Bearer $cleanToken';

      // Debug logging للـ headers
      print('📤 [DEBUG] Request headers: ${request.headers}');

      // إضافة الصورة
      request.files.add(
        await http.MultipartFile.fromPath('image', imageFile.path),
      );

      var streamedResponse = await request.send();
      var response = await http.Response.fromStream(streamedResponse);

      // Debug logging للاستجابة
      print('📥 [DEBUG] Response status: ${response.statusCode}');
      print('📥 [DEBUG] Response body: ${response.body}');

      if (response.statusCode == 200) {
        return jsonDecode(response.body) as Map<String, dynamic>;
      } else if (response.statusCode == 401) {
        print('❌ [ERROR] 401 Unauthorized - Token may be invalid or expired');
        throw Exception('غير مصرح لك - يرجى تسجيل الدخول مرة أخرى');
      } else {
        // محاولة استخراج رسالة الخطأ
        try {
          final errorData = jsonDecode(response.body) as Map<String, dynamic>;
          final detail = errorData['detail'] as String?;
          throw Exception(detail ?? 'فشل القياس');
        } catch (_) {
          throw Exception('فشل القياس: ${response.body}');
        }
      }
    } catch (e) {
      if (e is Exception) {
        rethrow;
      }
      throw Exception('خطأ في القياس: $e');
    }
  }

  Future<List<Map<String, dynamic>>> getHistory(String token) async {
    try {
      // التحقق من أن الـ token موجود وصحيح
      final cleanToken = token.trim();
      if (cleanToken.isEmpty) {
        throw Exception('الـ token غير موجود - يرجى تسجيل الدخول');
      }

      final response = await http.get(
        Uri.parse('$baseUrl/history'),
        headers: {
          'Authorization': 'Bearer $cleanToken',
          'Content-Type': 'application/json',
        },
      );

      if (response.statusCode == 200) {
        var data = jsonDecode(response.body) as Map<String, dynamic>;
        return List<Map<String, dynamic>>.from(data['history'] ?? []);
      } else if (response.statusCode == 401) {
        throw Exception('غير مصرح لك - يرجى تسجيل الدخول مرة أخرى');
      } else {
        // محاولة استخراج رسالة الخطأ
        try {
          final errorData = jsonDecode(response.body) as Map<String, dynamic>;
          final detail = errorData['detail'] as String?;
          throw Exception(detail ?? 'فشل جلب السجل');
        } catch (_) {
          throw Exception('فشل جلب السجل: ${response.body}');
        }
      }
    } catch (e) {
      if (e is Exception) {
        rethrow;
      }
      throw Exception('خطأ في جلب السجل: $e');
    }
  }

  Future<Map<String, dynamic>> getHealthRecommendations(
    String token,
    double systolic,
    double diastolic,
  ) async {
    try {
      final response = await http.post(
        Uri.parse('$baseUrl/recommendations'),
        headers: {
          'Authorization': 'Bearer $token',
          'Content-Type': 'application/json',
        },
        body: jsonEncode({'systolic': systolic, 'diastolic': diastolic}),
      );

      if (response.statusCode == 200) {
        return jsonDecode(response.body);
      } else {
        throw Exception('فشل جلب التوصيات: ${response.body}');
      }
    } catch (e) {
      throw Exception('خطأ في جلب التوصيات: $e');
    }
  }

  Future<Map<String, dynamic>> saveTrainingData(
    String token,
    File imageFile,
    double systolic,
    double diastolic,
  ) async {
    try {
      final cleanToken = token.trim();
      if (cleanToken.isEmpty) {
        throw Exception('الـ token غير موجود - يرجى تسجيل الدخول');
      }

      var request = http.MultipartRequest(
        'POST',
        Uri.parse('$baseUrl/training-data'),
      );

      request.headers['Authorization'] = 'Bearer $cleanToken';
      request.files.add(
        await http.MultipartFile.fromPath('image', imageFile.path),
      );
      request.fields['systolic'] = systolic.toString();
      request.fields['diastolic'] = diastolic.toString();

      var streamedResponse = await request.send();
      var response = await http.Response.fromStream(streamedResponse);

      if (response.statusCode == 200) {
        return jsonDecode(response.body) as Map<String, dynamic>;
      } else {
        try {
          final errorData = jsonDecode(response.body) as Map<String, dynamic>;
          final detail = errorData['detail'] as String?;
          throw Exception(detail ?? 'فشل حفظ بيانات التدريب');
        } catch (_) {
          throw Exception('فشل حفظ بيانات التدريب: ${response.body}');
        }
      }
    } catch (e) {
      if (e is Exception) {
        rethrow;
      }
      throw Exception('خطأ في حفظ بيانات التدريب: $e');
    }
  }

  Future<Map<String, dynamic>> getTrainingStats(String token) async {
    try {
      final cleanToken = token.trim();
      if (cleanToken.isEmpty) {
        throw Exception('الـ token غير موجود');
      }

      final response = await http.get(
        Uri.parse('$baseUrl/training-data/stats'),
        headers: {
          'Authorization': 'Bearer $cleanToken',
          'Content-Type': 'application/json',
        },
      );

      if (response.statusCode == 200) {
        return jsonDecode(response.body) as Map<String, dynamic>;
      } else {
        throw Exception('فشل جلب الإحصائيات: ${response.body}');
      }
    } catch (e) {
      if (e is Exception) {
        rethrow;
      }
      throw Exception('خطأ في جلب الإحصائيات: $e');
    }
  }
}
