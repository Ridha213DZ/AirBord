# AirBord

[![Tests](https://img.shields.io/badge/tests-323%20passed-brightgreen.svg)](tests/)
[![Python](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/)
[![GUI](https://img.shields.io/badge/GUI-PySide6%20(Qt)-orange.svg)](https://pypi.org/project/PySide6/)
[![Computer Vision](https://img.shields.io/badge/Vision-OpenCV%20%7C%20MediaPipe-red.svg)](https://opencv.org/)
[![Architecture](https://img.shields.io/badge/Architecture-Clean%20%2F%20DDD-informational.svg)]()

**AirBord** is an advanced interactive air-drawing desktop whiteboard application. It enables users to draw in the air using hand gestures captured via a webcam, paired with real-time biometric face identification to automatically manage individual user profiles and persistent drawing canvases.

---

## 🌟 Key Features

- 🖐️ **Real-Time Air Drawing:** Draw seamlessly in the air using hand gestures (e.g., `Closed Fist` to draw, `Open Palm` to navigate or hover).
- 📍 **Visual Hand Cursor:** Real-time on-canvas cursor feedback showing exact hand position across the canvas and interactive zones.
- 👤 **Biometric User Profiles:** Automatic user detection and identification using YuNet face detection and SFace biometric embeddings.
- 📄 **Multi-Page Workspaces:** Personal multi-page sketchbooks for each user with persistent JSON storage.
- 🎯 **Interaction Zones:** Smart screen segmentation for tool selection, color rings, eraser toggles, and undo/redo operations.
- 📐 **Clean Architecture & TDD:** Strictly decoupled layers (Core, Storage, Vision, Application, UI) backed by **323 automated unit and integration tests**.

---

## 🏗️ Architecture Overview

The project adheres to Clean Architecture and Domain-Driven Design (DDD) principles:

```
Camera Stream
     │
     ▼
┌─────────────────────────────────────────────────────────┐
│                     Vision Layer                        │
│  - YuNet Face Detector & SFace Face Recognition         │
│  - MediaPipe Hand Tracking & Gesture Classifier         │
└────────────────────────────┬────────────────────────────┘
                             │ HandGestureEvent / FaceEmbedding
                             ▼
┌─────────────────────────────────────────────────────────┐
│                  Application Layer                      │
│  - HandGestureController & FaceProfileService           │
│  - Coordinate Mappers (Normalized -> Screen -> Canvas)  │
│  - Interaction Zone Detector & Action Handlers          │
│  - DrawingService & ProfileService                      │
└────────────────────────────┬────────────────────────────┘
                             │
            ┌────────────────┴────────────────┐
            ▼                                 ▼
┌───────────────────────┐         ┌───────────────────────┐
│       Core Layer      │         │     Storage Layer     │
│ - Point, Stroke, Page │         │ - ProfileRepository   │
│ - Profile, FaceData   │         │ - JsonProfileStore    │
│ - Enums & Gestures    │         │ - ProfileSerializer   │
└───────────────────────┘         └───────────────────────┘
            │
            ▼
┌─────────────────────────────────────────────────────────┐
│                        UI Layer                         │
│  - DrawingCanvas (Real-Time Hand Cursor & Rendering)    │
│  - CameraPreview & Detection Overlays                   │
│  - CameraPreviewWindow & Main Integration Window        │
└─────────────────────────────────────────────────────────┘
```

---

## 🛠️ Tech Stack

- **Language:** Python 3.12+
- **GUI Framework:** PySide6 (Qt for Python 6.11+)
- **Computer Vision & AI:**
  - `opencv-python` / `opencv-contrib-python` (YuNet ONNX Face Detection, SFace)
  - `mediapipe` (Hand Landmark Detection & Gesture Recognition)
  - `numpy`
- **Testing Suite:** `pytest` (323 automated unit and contract tests)

---

## 📂 Project Structure

```text
AirBord/
├── app/
│   ├── core/           # Domain models (Point, Stroke, Page, Profile, Enums)
│   ├── storage/        # Persistence layer & JSON repository implementation
│   ├── vision/         # Face & Hand tracking pipelines (YuNet, MediaPipe)
│   ├── application/    # Business services, coordinate mappers & controllers
│   └── ui/             # PySide6 components (DrawingCanvas, CameraPreview)
├── models/             # Pretrained ONNX models (YuNet face detection)
├── tests/              # Comprehensive test suite (Core, Storage, Vision, UI)
├── PROJECT_STATUS.md   # Detailed architecture & progress report
└── README.md
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.12+
- Webcam

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Ridha213DZ/AirBord.git
   cd AirBord
   ```

2. **Set up the virtual environment:**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

### Running Tests

Execute the full automated test suite:
```bash
pytest
```
*Current test suite status: `323 passed`.*

---

## 🗺️ Current Status & Roadmap

- [x] **Core Domain & Models:** Points, Strokes, Pages, Profiles, Gesture Events.
- [x] **Persistence:** JSON Profile Repository with contract test coverage.
- [x] **Vision Pipelines:** YuNet face detection & MediaPipe gesture recognition.
- [x] **Interaction Logic:** Normalized-to-canvas coordinate mapping and gesture actions.
- [x] **Canvas Cursor:** Real-time visual hand cursor on `DrawingCanvas`.
- [ ] **In-Progress Stroke:** Real-time air-drawing stroke rendering on canvas.
- [ ] **Unified MainWindow:** Integrated Picture-in-Picture camera preview and whiteboard.
- [ ] **HUD Overlays:** Visual on-screen buttons for color wheel, tools, and page navigation.

---
---

# AirBord (النسخة العربية)

[![الاختبارات](https://img.shields.io/badge/%D8%A7%D9%84%D8%A7%D8%AE%D8%AA%D8%A8%D8%A7%D8%B1%D8%A7%D8%AA-323%20%D9%86%D8%A7%D8%AC%D8%AD-brightgreen.svg)](tests/)
[![بايثون](https://img.shields.io/badge/%D8%A8%D8%A7%D9%8A%D8%AB%D9%88%D9%86-3.12-blue.svg)](https://www.python.org/)
[![الواجهة الرسومية](https://img.shields.io/badge/%D8%A7%D9%84%D9%88%D8%A7%D8%AC%D9%87%D8%A9-PySide6%20(Qt)-orange.svg)](https://pypi.org/project/PySide6/)
[![الرؤية الحاسوبية](https://img.shields.io/badge/%D8%A7%D9%84%D8%B1%D8%A4%D9%8A%D8%A9-OpenCV%20%7C%20MediaPipe-red.svg)](https://opencv.org/)
[![المعمارية](https://img.shields.io/badge/%D8%A7%D9%84%D9%85%D8%B9%D9%85%D8%A7%D8%B1%D9%8A%D8%A9-%D9%86%D8%B8%D9%8A%D9%81%D8%A9%20%2F%20DDD-informational.svg)]()

**AirBord** هو تطبيق مكتبي تفاعلي متقدم للرسم في الهواء كسبورة بيضاء ذكية. يتيح التطبيق للمستخدمين الرسم والتفاعل في الهواء بحركات اليد عبر كاميرا الويب، مدعوماً بنظام تعرّف بيومتري فوري على الوجوه لإدارة الملفات الشخصية للمستخدمين وصفحات رسمهم المستقلة وحفظها تلقائياً.

---

## 🌟 أبرز الميزات

- 🖐️ **الرسم في الهواء آنياً:** الرسم بسلاسة باستخدام إيماءات اليد (مثل `قبضة اليد المغلقة FIST` للرسم، و`راحة اليد المفتوحة OPEN` للتنقل أو تحريك المؤشر).
- 📍 **مؤشر يد بصري فوري:** مؤشر مرئي على لوحة الكانفاس يعرض موضع اليد بدقة فوق اللوحة والمناطق التفاعلية.
- 👤 **ملفات مستخدمين بيومترية:** كشف وتحديد هوية المستخدم تلقائياً باستخدام نموذج YuNet السريع ونموذج SFace لاستخراج بصمة الوجه.
- 📄 **مساحات عمل متعددة الصفحات:** كراسات رسم متعددة الصفحات لكل مستخدم مع تخزين واسترجاع دائم بتنسيق JSON.
- 🎯 **مناطق التفاعل الذكية:** تقسيم تفاعلي للشاشة (عجلة اختيار الألوان، الممحاة، أدوات الرسم، والتراجع/التقدم).
- 📐 **معمارية برمجية نظيفة وتطوير موجه بالاختبارات (TDD):** فصل تام للمسؤوليات بين الطبقات مدعوماً بـ **323 اختباراً مؤتمتاً ناجحاً**.

---

## 🏗️ البنية المعمارية للنظام

يعتمد المشروع على مبادئ الهندسة النظيفة (Clean Architecture) والتصميم الموجه بالنطاق (DDD):

- **طبقة النواة (Core):** نماذج البيانات الأساسية (`Point`, `Stroke`, `Page`, `Profile`, `HandGestureEvent`).
- **طبقة التخزين (Storage):** نمط المستودع (`ProfileRepository`) والتسلسل لملفات JSON.
- **طبقة الرؤية الحاسوبية (Vision):** كاشف الوجوه (YuNet)، مشفر بصمات الوجوه (SFace)، ومتتبع اليد وتصنيف الإيماءات (MediaPipe).
- **طبقة التطبيق والخدمات (Application):** خدمات الرسم والملفات، ومحولات الإحداثيات من الأبعاد النسبية إلى بكسلات الشاشة والكانفاس، ومتحكم الإيماءات (`HandGestureController`).
- **طبقة الواجهة الرسومية (UI):** لوحة الرسم التفاعلية (`DrawingCanvas`) مع دعم المؤشر، ونافذة الكاميرا التوضيحية (`CameraPreview`).

---

## 🛠️ الحزمة البرمجية والتقنيات

- **لغة البرمجة:** Python 3.12+
- **إطار الواجهة الرسومية:** PySide6 (Qt for Python 6.11+)
- **الرؤية الحاسوبية والذكاء الاصطناعي:**
  - `opencv-python` و `opencv-contrib-python` (نموذج YuNet ONNX ونموذج SFace)
  - `mediapipe` (تتبع مفاصل اليد وتصنيف الإيماءات)
  - `numpy`
- **إطار الاختبار المؤتمت:** `pytest` (323 اختباراً ناجحاً بنسبة 100%)

---

## 🚀 البدء والتثبيت

### المتطلبات الأساسية
- بايثون 3.12 أو أحدث.
- كاميرا ويب (Webcam).

### خطوات التثبيت

1. **استنساخ المستودع:**
   ```bash
   git clone https://github.com/Ridha213DZ/AirBord.git
   cd AirBord
   ```

2. **إنشاء وتفعيل البيئة الافتراضية:**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. **تثبيت الحزم المطلوبة:**
   ```bash
   pip install -r requirements.txt
   ```

### تشغيل الاختبارات
لتشغيل حزمة الاختبارات المؤتمتة والتأكد من سلامة النظام:
```bash
pytest
```
*(النتيجة الحالية: 323 passed).*

---

## 🗺️ الوضع الحالي وخارطة الطريق

- [x] **طبقة النواة والنماذج:** النقاط، الخطوط، الصفحات، الملفات الشخصية، وأحداث الإيماءات.
- [x] **نظام التخزين والاستمرارية:** مستودع JSON مع اختبارات العقود التامة.
- [x] **خطوط الرؤية الحاسوبية:** كشف الوجوه بـ YuNet وتتبع اليد بـ MediaPipe.
- [x] **منطق التفاعل ورسم الخرائط:** تحويل إحداثيات اليد وحساب مناطق الشاشة.
- [x] **مؤشر اليد على الكانفاس:** عرض موضع مؤشر اليد بصرياً ولحظياً على لوحة الرسم.
- [ ] **السكتة الجارية (In-Progress Stroke):** إظهار الخط أثناء رسمه في الهواء آنياً دون انتظار انتهاء الإيماءة.
- [ ] **النافذة الرئيسية الموحدة (MainWindow):** دمج الكانفاس وكاميرا المعاينة المصغرة (PiP) في نافذة واحدة.
- [ ] **الواجهة التفاعلية العلوية (HUD):** رسم أزرار التفاعل على الشاشة (عجلة الألوان، الأدوات، والتنقل بين الصفحات).