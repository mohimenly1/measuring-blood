#!/usr/bin/env python3
"""
سكريبت لتصدير بيانات التدريب من قاعدة البيانات إلى CSV
"""
import sys
import os
import csv
from pathlib import Path

# إضافة مسار backend إلى Python path
backend_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, backend_dir)

from database import SessionLocal, TrainingData
from sqlalchemy import func

def export_training_data():
    """تصدير بيانات التدريب إلى CSV ومجلد الصور"""
    db = SessionLocal()
    
    try:
        # جلب جميع بيانات التدريب الم verified
        training_data = db.query(TrainingData).filter(
            TrainingData.is_verified == 1
        ).all()
        
        if not training_data:
            print("❌ لا توجد بيانات تدريب للتصدير")
            return
        
        print(f"📊 تم العثور على {len(training_data)} صورة للتدريب")
        
        # إنشاء مجلدات التصدير
        export_dir = Path(backend_dir) / 'data' / 'train'
        images_dir = export_dir / 'images'
        images_dir.mkdir(parents=True, exist_ok=True)
        
        # إنشاء CSV
        csv_path = export_dir / 'labels.csv'
        
        with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['image_name', 'systolic', 'diastolic'])
            
            for idx, data in enumerate(training_data, 1):
                # نسخ الصورة
                source_path = Path(data.image_path)
                if source_path.exists():
                    # اسم جديد للصورة
                    image_name = f"training_{data.id:05d}.jpg"
                    dest_path = images_dir / image_name
                    
                    # نسخ الصورة
                    import shutil
                    shutil.copy2(source_path, dest_path)
                    
                    # كتابة في CSV
                    writer.writerow([
                        image_name,
                        data.systolic,
                        data.diastolic
                    ])
                    
                    if idx % 10 == 0:
                        print(f"✅ تم تصدير {idx}/{len(training_data)} صورة")
                else:
                    print(f"⚠️ الصورة غير موجودة: {source_path}")
        
        print(f"\n✅ تم التصدير بنجاح!")
        print(f"📁 الصور: {images_dir}")
        print(f"📄 CSV: {csv_path}")
        print(f"\n💡 الآن يمكنك تشغيل: python train_model.py")
        
    except Exception as e:
        print(f"❌ خطأ في التصدير: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    print("=" * 60)
    print("📤 تصدير بيانات التدريب")
    print("=" * 60)
    export_training_data()

