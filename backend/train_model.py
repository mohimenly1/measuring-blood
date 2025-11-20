#!/usr/bin/env python3
"""
سكريبت لتدريب نموذج قياس ضغط الدم
"""
import sys
import os

# إضافة مسار backend إلى Python path
backend_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, backend_dir)

from models.blood_pressure_model import BloodPressureCNN

def main():
    print("=" * 60)
    print("🎯 تدريب نموذج قياس ضغط الدم")
    print("=" * 60)
    
    # مسار مجلد البيانات
    train_data_dir = os.path.join(backend_dir, 'data', 'train')
    
    # التحقق من وجود البيانات
    if not os.path.exists(train_data_dir):
        print(f"\n❌ مجلد البيانات غير موجود: {train_data_dir}")
        print("\n📁 يجب أن يحتوي المجلد على:")
        print("   - images/ (مجلد الصور)")
        print("   - labels.csv (ملف CSV مع: image_name, systolic, diastolic)")
        print("\n💡 مثال على labels.csv:")
        print("   image_name,systolic,diastolic")
        print("   image001.jpg,120,80")
        print("   image002.jpg,130,85")
        print("\n📝 أنشئ المجلد وملف CSV ثم حاول مرة أخرى")
        return
    
    labels_path = os.path.join(train_data_dir, 'labels.csv')
    images_dir = os.path.join(train_data_dir, 'images')
    
    if not os.path.exists(labels_path):
        print(f"\n❌ ملف labels.csv غير موجود في: {train_data_dir}")
        return
    
    if not os.path.exists(images_dir):
        print(f"\n❌ مجلد images غير موجود في: {train_data_dir}")
        return
    
    # إنشاء النموذج
    model = BloodPressureCNN()
    
    try:
        # التدريب
        print(f"\n📂 مجلد البيانات: {train_data_dir}")
        history = model.train(
            train_data_dir=train_data_dir,
            epochs=50,  # يمكنك تغيير هذا
            batch_size=32
        )
        
        print("\n" + "=" * 60)
        print("✅ تم التدريب بنجاح!")
        print(f"📊 النموذج محفوظ في: {model.model_path}")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ خطأ أثناء التدريب: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
