#!/usr/bin/env python3
"""
سكريبت للتحقق من بيانات التدريب في قاعدة البيانات
"""
import sys
import os

backend_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, backend_dir)

from database import SessionLocal, TrainingData
from sqlalchemy import func

def check_training_data():
    """التحقق من بيانات التدريب"""
    db = SessionLocal()
    
    try:
        # إحصائيات عامة
        total = db.query(TrainingData).count()
        verified = db.query(TrainingData).filter(
            TrainingData.is_verified == 1
        ).count()
        pending = db.query(TrainingData).filter(
            TrainingData.is_verified == 0
        ).count()
        
        print("=" * 60)
        print("📊 إحصائيات بيانات التدريب")
        print("=" * 60)
        print(f"إجمالي البيانات: {total}")
        print(f"✅ بيانات محققة: {verified}")
        print(f"⏳ بيانات قيد الانتظار: {pending}")
        print()
        
        if verified == 0:
            print("⚠️  لا توجد بيانات محققة للتدريب")
            print("💡 اجمع بيانات من المستخدمين أولاً")
            return
        
        # إحصائيات القياسات
        stats = db.query(
            func.avg(TrainingData.systolic).label('avg_systolic'),
            func.avg(TrainingData.diastolic).label('avg_diastolic'),
            func.min(TrainingData.systolic).label('min_systolic'),
            func.max(TrainingData.systolic).label('max_systolic'),
            func.min(TrainingData.diastolic).label('min_diastolic'),
            func.max(TrainingData.diastolic).label('max_diastolic'),
        ).filter(
            TrainingData.is_verified == 1
        ).first()
        
        print("📈 إحصائيات القياسات:")
        print(f"   متوسط الانقباضي: {stats.avg_systolic:.1f} mmHg")
        print(f"   متوسط الانبساطي: {stats.avg_diastolic:.1f} mmHg")
        print(f"   نطاق الانقباضي: {stats.min_systolic:.1f} - {stats.max_systolic:.1f} mmHg")
        print(f"   نطاق الانبساطي: {stats.min_diastolic:.1f} - {stats.max_diastolic:.1f} mmHg")
        print()
        
        # حالة الجاهزية
        minimum_required = 50
        if verified >= minimum_required:
            print(f"✅ جاهز للتدريب! ({verified} صورة)")
            print("💡 يمكنك الآن تشغيل:")
            print("   1. python export_training_data.py")
            print("   2. python train_model.py")
        else:
            needed = minimum_required - verified
            print(f"⏳ تحتاج {needed} صورة أخرى للتدريب")
            print(f"   (الحد الأدنى: {minimum_required} صورة)")
            print("💡 استمر في جمع البيانات من المستخدمين")
        
        print("=" * 60)
        
    except Exception as e:
        print(f"❌ خطأ: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    check_training_data()

