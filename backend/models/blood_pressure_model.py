import numpy as np
import cv2
from tensorflow import keras
from tensorflow.keras.applications import VGG16
from tensorflow.keras import layers, Model
from tensorflow.keras.optimizers import Adam
import os

class BloodPressureCNN:
    def __init__(self, model_path=None):
        self.model = None
        # تحديث المسار ليكون نسبي من backend/
        # استخدام مسار نسبي من موقع الملف
        if model_path is None:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            self.model_path = os.path.join(current_dir, 'blood_pressure_model.h5')
        else:
            self.model_path = model_path
        
    def build_model(self, input_shape=(224, 224, 3)):
        """
        بناء نموذج باستخدام Transfer Learning مع VGG16
        VGG16 متوفر تلقائياً في TensorFlow - لا يحتاج تنزيل ملفات
        """
        # استخدام VGG16 المدرب مسبقاً (متوفر في TensorFlow)
        base_model = VGG16(
            weights='imagenet',  # أوزان مدربة - متوفرة تلقائياً
            include_top=False,   # بدون الطبقات الأخيرة
            input_shape=input_shape
        )
        
        # تجميد الطبقات الأساسية (للتدريب السريع)
        base_model.trainable = False
        
        # إضافة طبقات جديدة للتنبؤ بضغط الدم
        inputs = keras.Input(shape=input_shape)
        x = base_model(inputs, training=False)
        x = layers.GlobalAveragePooling2D()(x)
        x = layers.Dense(512, activation='relu')(x)
        x = layers.Dropout(0.5)(x)
        x = layers.Dense(256, activation='relu')(x)
        x = layers.Dropout(0.3)(x)
        outputs = layers.Dense(2, activation='linear')(x)  # systolic, diastolic
        
        model = Model(inputs, outputs)
        
        model.compile(
            optimizer=Adam(learning_rate=0.001),
            loss='mse',
            metrics=['mae']
        )
        
        return model
    
    def preprocess_image(self, image_path):
        """Preprocess image for prediction"""
        img = cv2.imread(image_path)
        if img is None:
            raise ValueError("Could not read image")
        
        # Resize to model input size
        img = cv2.resize(img, (224, 224))
        
        # Convert BGR to RGB
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        
        # Normalize
        img = img.astype(np.float32) / 255.0
        
        # Expand dimensions for batch
        img = np.expand_dims(img, axis=0)
        
        return img
    
    def predict(self, image_path):
        """التنبؤ بضغط الدم من الصورة"""
        if self.model is None:
            # محاولة تحميل النموذج المدرب
            if os.path.exists(self.model_path):
                try:
                    self.model = keras.models.load_model(self.model_path)
                    print("✅ تم تحميل النموذج المدرب بنجاح")
                except Exception as e:
                    print(f"⚠️ خطأ في تحميل النموذج: {e}")
                    print("⚠️ استخدام Transfer Learning (غير مدرب)")
                    self.model = self.build_model()
            else:
                print("⚠️ لا يوجد نموذج مدرب - استخدام Transfer Learning")
                self.model = self.build_model()
                print("⚠️ هذا نموذج غير مدرب - النتائج تجريبية")
        
        # معالجة الصورة
        processed_img = self.preprocess_image(image_path)
        
        # التنبؤ
        prediction = self.model.predict(processed_img, verbose=0)
        
        # استخراج النتائج
        systolic = float(prediction[0][0])
        diastolic = float(prediction[0][1])
        
        # التأكد من القيم المعقولة
        systolic = max(90, min(180, systolic))
        diastolic = max(60, min(120, diastolic))
        
        return {
            'systolic': round(systolic, 1),
            'diastolic': round(diastolic, 1)
        }
    
    def train(self, train_data_dir, epochs=50, batch_size=32):
        """
        تدريب النموذج على البيانات
        
        train_data_dir يجب أن يحتوي على:
        - images/ (مجلد الصور)
        - labels.csv (ملف CSV مع: image_name, systolic, diastolic)
        """
        from tensorflow.keras.preprocessing.image import ImageDataGenerator
        import pandas as pd
        
        # بناء النموذج
        print("🔨 بناء النموذج باستخدام Transfer Learning (VGG16)...")
        self.model = self.build_model()
        
        # قراءة البيانات
        labels_path = os.path.join(train_data_dir, 'labels.csv')
        if not os.path.exists(labels_path):
            raise FileNotFoundError(
                f"❌ ملف labels.csv غير موجود في: {train_data_dir}\n"
                f"📁 يجب أن يحتوي المجلد على:\n"
                f"   - images/ (مجلد الصور)\n"
                f"   - labels.csv (ملف CSV)"
            )
        
        labels_df = pd.read_csv(labels_path)
        
        # التحقق من الأعمدة
        required_cols = ['image_name', 'systolic', 'diastolic']
        for col in required_cols:
            if col not in labels_df.columns:
                raise ValueError(
                    f"❌ العمود '{col}' غير موجود في labels.csv\n"
                    f"📋 الأعمدة المطلوبة: {', '.join(required_cols)}"
                )
        
        images_dir = os.path.join(train_data_dir, 'images')
        if not os.path.exists(images_dir):
            raise FileNotFoundError(f"❌ مجلد الصور غير موجود: {images_dir}")
        
        print(f"✅ تم العثور على {len(labels_df)} صورة في labels.csv")
        
        # معالجة البيانات
        datagen = ImageDataGenerator(
            rescale=1./255,
            validation_split=0.2,
            rotation_range=20,
            width_shift_range=0.2,
            height_shift_range=0.2,
            horizontal_flip=True
        )
        
        # Generator للتدريب
        train_generator = datagen.flow_from_dataframe(
            labels_df,
            directory=images_dir,
            x_col='image_name',
            y_col=['systolic', 'diastolic'],
            target_size=(224, 224),
            batch_size=batch_size,
            class_mode='raw',
            subset='training'
        )
        
        # Generator للتحقق
        validation_generator = datagen.flow_from_dataframe(
            labels_df,
            directory=images_dir,
            x_col='image_name',
            y_col=['systolic', 'diastolic'],
            target_size=(224, 224),
            batch_size=batch_size,
            class_mode='raw',
            subset='validation'
        )
        
        print(f"📊 بيانات التدريب: {train_generator.samples} صورة")
        print(f"📊 بيانات التحقق: {validation_generator.samples} صورة")
        
        # التدريب
        print("\n🚀 بدء التدريب...")
        print("⏳ هذا قد يستغرق بعض الوقت...\n")
        
        history = self.model.fit(
            train_generator,
            epochs=epochs,
            validation_data=validation_generator,
            verbose=1
        )
        
        # حفظ النموذج
        os.makedirs(os.path.dirname(self.model_path), exist_ok=True)
        self.model.save(self.model_path)
        print(f"\n✅ تم حفظ النموذج في: {self.model_path}")
        
        return history

