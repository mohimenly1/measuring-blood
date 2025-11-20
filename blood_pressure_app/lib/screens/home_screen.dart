import 'dart:io';
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:camera/camera.dart';
import 'package:image_picker/image_picker.dart';
import '../services/auth_service.dart';
import '../services/api_service.dart';
import 'camera_screen.dart';
import 'history_screen.dart';

class HomeScreen extends StatefulWidget {
  const HomeScreen({super.key});

  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  final ImagePicker _picker = ImagePicker();
  bool _isLoading = false;
  File? _lastProcessedImage;

  Future<void> _takePicture() async {
    try {
      final cameras = await availableCameras();
      if (!mounted) return;
      
      // التحقق من وجود كاميرات متاحة
      if (cameras.isEmpty) {
        if (mounted) {
          ScaffoldMessenger.of(context).showSnackBar(
            const SnackBar(
              content: Text('لا توجد كاميرات متاحة على هذا الجهاز'),
              backgroundColor: Colors.red,
            ),
          );
        }
        return;
      }
      
      final result = await Navigator.push(
        context,
        MaterialPageRoute(
          builder: (context) => CameraScreen(cameras: cameras),
        ),
      );

      if (result != null && result is File) {
        _processImage(result);
      }
    } catch (e) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text('خطأ في فتح الكاميرا: $e'),
            backgroundColor: Colors.red,
          ),
        );
      }
    }
  }

  Future<void> _pickImageFromGallery() async {
    try {
      final XFile? image = await _picker.pickImage(source: ImageSource.gallery);
      if (image != null) {
        _processImage(File(image.path));
      }
    } catch (e) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text('خطأ في اختيار الصورة: $e'),
            backgroundColor: Colors.red,
          ),
        );
      }
    }
  }

  Future<void> _processImage(File imageFile) async {
    setState(() => _isLoading = true);
    _lastProcessedImage = imageFile; // حفظ الصورة لاستخدامها لاحقاً

    try {
      final authService = Provider.of<AuthService>(context, listen: false);
      final apiService = Provider.of<ApiService>(context, listen: false);

      if (authService.token == null || authService.token!.isEmpty) {
        throw Exception('غير مصرح لك - يرجى تسجيل الدخول');
      }

      final result = await apiService.measureBloodPressure(
        authService.token!,
        imageFile,
      );

      if (mounted) {
        _showResults(result);
      }
    } catch (e) {
      if (mounted) {
        String errorMessage = e.toString().replaceAll('Exception: ', '');
        
        // إذا كان الخطأ 401، قم بتسجيل الخروج
        if (errorMessage.contains('غير مصرح لك') || 
            errorMessage.contains('401') ||
            errorMessage.contains('Unauthorized')) {
          await Provider.of<AuthService>(context, listen: false).logout();
          if (mounted) {
            ScaffoldMessenger.of(context).showSnackBar(
              const SnackBar(
                content: Text('انتهت صلاحية الجلسة - يرجى تسجيل الدخول مرة أخرى'),
                backgroundColor: Colors.orange,
                duration: Duration(seconds: 3),
              ),
            );
          }
        } else {
          ScaffoldMessenger.of(context).showSnackBar(
            SnackBar(
              content: Text(errorMessage),
              backgroundColor: Colors.red,
              duration: const Duration(seconds: 3),
            ),
          );
        }
      }
    } finally {
      if (mounted) {
        setState(() => _isLoading = false);
      }
    }
  }

  void _showResults(Map<String, dynamic> result) {
    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        title: const Text('نتائج القياس'),
        content: SingleChildScrollView(
          child: Column(
            mainAxisSize: MainAxisSize.min,
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              // تحذير مهم
              Container(
                padding: const EdgeInsets.all(12),
                decoration: BoxDecoration(
                  color: Colors.orange.shade50,
                  borderRadius: BorderRadius.circular(8),
                  border: Border.all(color: Colors.orange.shade300),
                ),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Row(
                      children: [
                        Icon(Icons.warning_amber_rounded, 
                             color: Colors.orange.shade700, size: 20),
                        const SizedBox(width: 8),
                        const Text(
                          'تحذير مهم',
                          style: TextStyle(
                            fontWeight: FontWeight.bold,
                            color: Colors.orange,
                          ),
                        ),
                      ],
                    ),
                    const SizedBox(height: 8),
                    const Text(
                      'هذه النتائج تجريبية ولا يمكن الاعتماد عليها لأغراض طبية. '
                      'ننصح بمراجعة الطبيب للحصول على قياسات دقيقة باستخدام أجهزة معتمدة.',
                      style: TextStyle(fontSize: 12),
                    ),
                  ],
                ),
              ),
              const SizedBox(height: 16),
              Text('الضغط الانقباضي: ${result['systolic']} mmHg'),
              Text('الضغط الانبساطي: ${result['diastolic']} mmHg'),
              const SizedBox(height: 16),
              if (result['recommendations'] != null) ...[
                const Text(
                  'التوصيات الصحية:',
                  style: TextStyle(fontWeight: FontWeight.bold),
                ),
                const SizedBox(height: 8),
                ...(result['recommendations'] as List)
                    .map((rec) => Padding(
                          padding: const EdgeInsets.only(bottom: 4),
                          child: Text('• $rec'),
                        ))
                    .toList(),
              ],
              const SizedBox(height: 16),
              const Divider(),
              const SizedBox(height: 8),
              const Text(
                '💡 ساعدنا في تحسين النموذج',
                style: TextStyle(
                  fontWeight: FontWeight.bold,
                  fontSize: 14,
                ),
              ),
              const SizedBox(height: 8),
              const Text(
                'إذا قمت بقياس ضغط دمك بجهاز طبي، يمكنك إدخال القياس الحقيقي لمساعدتنا في تدريب النموذج.',
                style: TextStyle(fontSize: 12),
              ),
            ],
          ),
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(context),
            child: const Text('تخطي'),
          ),
          ElevatedButton(
            onPressed: () {
              Navigator.pop(context);
              _showTrainingDataDialog(result);
            },
            style: ElevatedButton.styleFrom(
              backgroundColor: Theme.of(context).colorScheme.primary,
            ),
            child: const Text('إدخال القياس الحقيقي'),
          ),
        ],
      ),
    );
  }

  void _showTrainingDataDialog(Map<String, dynamic> result) {
    final systolicController = TextEditingController(
      text: result['systolic'].toString(),
    );
    final diastolicController = TextEditingController(
      text: result['diastolic'].toString(),
    );

    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        title: const Text('إدخال القياس الحقيقي'),
        content: SingleChildScrollView(
          child: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              const Text(
                'أدخل قياس ضغط الدم الحقيقي من جهاز طبي معتمد:',
                style: TextStyle(fontSize: 14),
              ),
              const SizedBox(height: 16),
              TextField(
                controller: systolicController,
                keyboardType: TextInputType.number,
                decoration: const InputDecoration(
                  labelText: 'الضغط الانقباضي (mmHg)',
                  border: OutlineInputBorder(),
                ),
                textDirection: TextDirection.ltr,
              ),
              const SizedBox(height: 12),
              TextField(
                controller: diastolicController,
                keyboardType: TextInputType.number,
                decoration: const InputDecoration(
                  labelText: 'الضغط الانبساطي (mmHg)',
                  border: OutlineInputBorder(),
                ),
                textDirection: TextDirection.ltr,
              ),
            ],
          ),
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(context),
            child: const Text('إلغاء'),
          ),
          ElevatedButton(
            onPressed: () async {
              final systolic = double.tryParse(systolicController.text);
              final diastolic = double.tryParse(diastolicController.text);

              if (systolic == null || diastolic == null) {
                ScaffoldMessenger.of(context).showSnackBar(
                  const SnackBar(
                    content: Text('الرجاء إدخال قيم صحيحة'),
                    backgroundColor: Colors.red,
                  ),
                );
                return;
              }

              if (systolic < 70 || systolic > 200 || diastolic < 40 || diastolic > 130) {
                ScaffoldMessenger.of(context).showSnackBar(
                  const SnackBar(
                    content: Text('القيم غير معقولة - تحقق من القياسات'),
                    backgroundColor: Colors.orange,
                  ),
                );
                return;
              }

              Navigator.pop(context);
              await _saveTrainingData(systolic, diastolic);
            },
            style: ElevatedButton.styleFrom(
              backgroundColor: Theme.of(context).colorScheme.primary,
            ),
            child: const Text('حفظ'),
          ),
        ],
      ),
    );
  }

  Future<void> _saveTrainingData(double systolic, double diastolic) async {
    if (_lastProcessedImage == null) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(
          content: Text('لا توجد صورة لحفظها'),
          backgroundColor: Colors.red,
        ),
      );
      return;
    }

    setState(() => _isLoading = true);

    try {
      final authService = Provider.of<AuthService>(context, listen: false);
      final apiService = Provider.of<ApiService>(context, listen: false);

      if (authService.token == null || authService.token!.isEmpty) {
        throw Exception('غير مصرح لك');
      }

      final response = await apiService.saveTrainingData(
        authService.token!,
        _lastProcessedImage!,
        systolic,
        diastolic,
      );

      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text(
              '✅ ${response['message']}\n'
              'إجمالي بيانات التدريب: ${response['total_training_data']}',
            ),
            backgroundColor: Colors.green,
            duration: const Duration(seconds: 3),
          ),
        );
      }
    } catch (e) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text('خطأ في حفظ البيانات: $e'),
            backgroundColor: Colors.red,
          ),
        );
      }
    } finally {
      if (mounted) {
        setState(() => _isLoading = false);
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('قياس ضغط الدم الذكي'),
        actions: [
          IconButton(
            icon: const Icon(Icons.history),
            onPressed: () {
              Navigator.push(
                context,
                MaterialPageRoute(builder: (context) => const HistoryScreen()),
              );
            },
          ),
          IconButton(
            icon: const Icon(Icons.logout),
            onPressed: () async {
              await Provider.of<AuthService>(context, listen: false).logout();
            },
          ),
        ],
      ),
      body: _isLoading
          ? const Center(child: CircularProgressIndicator())
          : Container(
              decoration: BoxDecoration(
                gradient: LinearGradient(
                  begin: Alignment.topCenter,
                  end: Alignment.bottomCenter,
                  colors: [
                    Theme.of(context).colorScheme.surface,
                    Colors.white,
                  ],
                ),
              ),
              child: SafeArea(
                child: Padding(
                  padding: const EdgeInsets.all(24.0),
                  child: Column(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      Icon(
                        Icons.favorite,
                        size: 120,
                        color: Theme.of(context).colorScheme.primary,
                      ),
                      const SizedBox(height: 24),
                      Text(
                        'مرحباً ${Provider.of<AuthService>(context).userName ?? "المستخدم"}',
                        style: Theme.of(context).textTheme.headlineSmall?.copyWith(
                              fontWeight: FontWeight.bold,
                            ),
                        textAlign: TextAlign.center,
                      ),
                      const SizedBox(height: 8),
                      Text(
                        'اضغط على الكاميرا لقياس ضغط الدم',
                        style: Theme.of(context).textTheme.bodyLarge?.copyWith(
                              color: Colors.grey[600],
                            ),
                        textAlign: TextAlign.center,
                      ),
                      const SizedBox(height: 48),
                      Row(
                        mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                        children: [
                          _buildActionButton(
                            context,
                            icon: Icons.camera_alt,
                            label: 'الكاميرا',
                            onTap: _takePicture,
                            color: Theme.of(context).colorScheme.primary,
                          ),
                          _buildActionButton(
                            context,
                            icon: Icons.photo_library,
                            label: 'المعرض',
                            onTap: _pickImageFromGallery,
                            color: Theme.of(context).colorScheme.secondary,
                          ),
                        ],
                      ),
                      const SizedBox(height: 32),
                      Card(
                        elevation: 4,
                        shape: RoundedRectangleBorder(
                          borderRadius: BorderRadius.circular(16),
                        ),
                        child: Padding(
                          padding: const EdgeInsets.all(16.0),
                          child: Column(
                            children: [
                              Icon(
                                Icons.info_outline,
                                color: Theme.of(context).colorScheme.secondary,
                              ),
                              const SizedBox(height: 8),
                              Text(
                                'تعليمات الاستخدام',
                                style: Theme.of(context)
                                    .textTheme
                                    .titleMedium
                                    ?.copyWith(fontWeight: FontWeight.bold),
                              ),
                              const SizedBox(height: 8),
                              const Text(
                                '1. ضع إصبعك على الكاميرا\n'
                                '2. انتظر حتى يتم تحليل الصورة\n'
                                '3. احصل على النتائج والتوصيات',
                                textAlign: TextAlign.center,
                                style: TextStyle(fontSize: 14),
                              ),
                              const SizedBox(height: 12),
                              Container(
                                padding: const EdgeInsets.all(8),
                                decoration: BoxDecoration(
                                  color: Colors.orange.shade50,
                                  borderRadius: BorderRadius.circular(8),
                                ),
                                child: const Text(
                                  '⚠️ النتائج تجريبية - استشر الطبيب للقياسات الدقيقة',
                                  textAlign: TextAlign.center,
                                  style: TextStyle(
                                    fontSize: 11,
                                    color: Colors.orange,
                                    fontWeight: FontWeight.bold,
                                  ),
                                ),
                              ),
                            ],
                          ),
                        ),
                      ),
                    ],
                  ),
                ),
              ),
            ),
    );
  }

  Widget _buildActionButton(
    BuildContext context, {
    required IconData icon,
    required String label,
    required VoidCallback onTap,
    required Color color,
  }) {
    return InkWell(
      onTap: onTap,
      borderRadius: BorderRadius.circular(20),
      child: Container(
        width: 140,
        height: 140,
        decoration: BoxDecoration(
          color: color.withOpacity(0.1),
          borderRadius: BorderRadius.circular(20),
          border: Border.all(color: color, width: 2),
        ),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Icon(icon, size: 48, color: color),
            const SizedBox(height: 8),
            Text(
              label,
              style: TextStyle(
                fontSize: 16,
                fontWeight: FontWeight.bold,
                color: color,
              ),
            ),
          ],
        ),
      ),
    );
  }
}

