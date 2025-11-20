import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../services/auth_service.dart';
import '../services/api_service.dart';

class HistoryScreen extends StatefulWidget {
  const HistoryScreen({super.key});

  @override
  State<HistoryScreen> createState() => _HistoryScreenState();
}

class _HistoryScreenState extends State<HistoryScreen> {
  List<Map<String, dynamic>> _history = [];
  bool _isLoading = true;

  @override
  void initState() {
    super.initState();
    _loadHistory();
  }

  Future<void> _loadHistory() async {
    setState(() => _isLoading = true);

    try {
      final authService = Provider.of<AuthService>(context, listen: false);
      final apiService = Provider.of<ApiService>(context, listen: false);

      if (authService.token != null) {
        final history = await apiService.getHistory(authService.token!);
        setState(() {
          _history = history;
          _isLoading = false;
        });
      }
    } catch (e) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text('خطأ في جلب السجل: $e'),
            backgroundColor: Colors.red,
          ),
        );
      }
      setState(() => _isLoading = false);
    }
  }

  Color _getStatusColor(double systolic, double diastolic) {
    if (systolic < 120 && diastolic < 80) {
      return Colors.green;
    } else if (systolic < 130 && diastolic < 80) {
      return Colors.orange;
    } else {
      return Colors.red;
    }
  }

  String _getStatusText(double systolic, double diastolic) {
    if (systolic < 120 && diastolic < 80) {
      return 'طبيعي';
    } else if (systolic < 130 && diastolic < 80) {
      return 'مرتفع قليلاً';
    } else {
      return 'مرتفع';
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('سجل القياسات'),
      ),
      body: _isLoading
          ? const Center(child: CircularProgressIndicator())
          : _history.isEmpty
              ? Center(
                  child: Column(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      Icon(
                        Icons.history,
                        size: 64,
                        color: Colors.grey[400],
                      ),
                      const SizedBox(height: 16),
                      Text(
                        'لا توجد قياسات سابقة',
                        style: TextStyle(color: Colors.grey[600]),
                      ),
                    ],
                  ),
                )
              : RefreshIndicator(
                  onRefresh: _loadHistory,
                  child: ListView.builder(
                    padding: const EdgeInsets.all(16),
                    itemCount: _history.length,
                    itemBuilder: (context, index) {
                      final measurement = _history[index];
                      final systolic = measurement['systolic']?.toDouble() ?? 0.0;
                      final diastolic = measurement['diastolic']?.toDouble() ?? 0.0;
                      final date = measurement['created_at'] ?? '';
                      final statusColor = _getStatusColor(systolic, diastolic);
                      final statusText = _getStatusText(systolic, diastolic);

                      return Card(
                        margin: const EdgeInsets.only(bottom: 12),
                        elevation: 2,
                        shape: RoundedRectangleBorder(
                          borderRadius: BorderRadius.circular(12),
                        ),
                        child: ListTile(
                          contentPadding: const EdgeInsets.all(16),
                          leading: CircleAvatar(
                            backgroundColor: statusColor.withOpacity(0.2),
                            child: Icon(
                              Icons.favorite,
                              color: statusColor,
                            ),
                          ),
                          title: Text(
                            '$systolic / $diastolic mmHg',
                            style: const TextStyle(
                              fontSize: 20,
                              fontWeight: FontWeight.bold,
                            ),
                          ),
                          subtitle: Column(
                            crossAxisAlignment: CrossAxisAlignment.start,
                            children: [
                              const SizedBox(height: 8),
                              Text('الحالة: $statusText'),
                              if (date.isNotEmpty) Text('التاريخ: $date'),
                            ],
                          ),
                          trailing: Icon(
                            Icons.arrow_forward_ios,
                            size: 16,
                            color: Colors.grey[600],
                          ),
                        ),
                      );
                    },
                  ),
                ),
    );
  }
}

