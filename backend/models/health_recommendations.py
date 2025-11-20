class HealthRecommendationsAI:
    """AI model for health recommendations based on blood pressure"""
    
    def __init__(self):
        self.recommendations_db = {
            'normal': [
                'ممتاز! ضغط الدم في المعدل الطبيعي',
                'استمر في الحفاظ على نمط حياة صحي',
                'مارس الرياضة بانتظام',
                'تناول نظام غذائي متوازن',
                'احصل على قسط كافٍ من النوم (7-8 ساعات)',
            ],
            'elevated': [
                'ضغط الدم مرتفع قليلاً - راقب حالتك',
                'قلل من تناول الملح في الطعام',
                'مارس التمارين الرياضية 30 دقيقة يومياً',
                'تجنب التدخين والكحول',
                'حاول تقليل التوتر والضغط النفسي',
                'راقب ضغط الدم بانتظام',
            ],
            'high_stage1': [
                'ضغط الدم مرتفع - استشر الطبيب',
                'قلل من تناول الأطعمة المالحة',
                'مارس الرياضة بانتظام',
                'حافظ على وزن صحي',
                'تجنب التدخين تماماً',
                'قلل من الكافيين',
                'احصل على قسط كافٍ من النوم',
                'راقب ضغط الدم يومياً',
            ],
            'high_stage2': [
                'ضغط الدم مرتفع جداً - استشر الطبيب فوراً',
                'اتبع تعليمات الطبيب بدقة',
                'تناول الأدوية الموصوفة بانتظام',
                'قلل من الملح بشكل كبير',
                'مارس رياضة خفيفة بعد استشارة الطبيب',
                'تجنب التوتر والضغط النفسي',
                'راقب ضغط الدم عدة مرات يومياً',
                'احصل على رعاية طبية فورية إذا كان الضغط مرتفعاً جداً',
            ],
            'crisis': [
                'حالة طوارئ - اتصل بالطوارئ فوراً!',
                'لا تنتظر - احصل على رعاية طبية فورية',
                'اجلس وارتاح ولا تبذل أي جهد',
                'اتصل برقم الطوارئ 911',
            ],
        }
    
    def get_recommendations(self, systolic, diastolic):
        """Get AI-powered health recommendations based on blood pressure"""
        category = self._categorize_bp(systolic, diastolic)
        recommendations = self.recommendations_db.get(category, [])
        
        # Add personalized recommendations based on values
        personalized = self._get_personalized_recommendations(systolic, diastolic)
        
        return {
            'category': category,
            'recommendations': recommendations + personalized,
            'severity': self._get_severity(category),
        }
    
    def _categorize_bp(self, systolic, diastolic):
        """Categorize blood pressure reading"""
        if systolic < 120 and diastolic < 80:
            return 'normal'
        elif systolic < 130 and diastolic < 80:
            return 'elevated'
        elif systolic < 140 or diastolic < 90:
            return 'high_stage1'
        elif systolic < 180 or diastolic < 120:
            return 'high_stage2'
        else:
            return 'crisis'
    
    def _get_severity(self, category):
        """Get severity level"""
        severity_map = {
            'normal': 'low',
            'elevated': 'moderate',
            'high_stage1': 'high',
            'high_stage2': 'very_high',
            'crisis': 'critical',
        }
        return severity_map.get(category, 'unknown')
    
    def _get_personalized_recommendations(self, systolic, diastolic):
        """Get personalized recommendations based on specific values"""
        recommendations = []
        
        # Systolic-specific recommendations
        if systolic > 140:
            recommendations.append('الضغط الانقباضي مرتفع - راجع الطبيب قريباً')
        
        if diastolic > 90:
            recommendations.append('الضغط الانبساطي مرتفع - يحتاج متابعة')
        
        # Combined recommendations
        if systolic > 160 or diastolic > 100:
            recommendations.append('يُنصح بقياس ضغط الدم عدة مرات يومياً')
            recommendations.append('تجنب الأنشطة الشاقة')
        
        # Lifestyle recommendations based on severity
        if systolic > 140 or diastolic > 90:
            recommendations.append('قلل من الأطعمة المصنعة')
            recommendations.append('تناول المزيد من الخضروات والفواكه')
            recommendations.append('اشرب الماء بكميات كافية (8 أكواب يومياً)')
        
        return recommendations

