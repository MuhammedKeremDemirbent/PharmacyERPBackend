# Pharmacy ERP - Backend Özeti

Bu dosya, Frontend projesine başlarken referans olması için oluşturulmuştur.

## 🚀 API Uç Noktaları (Endpoints)

Base URL: `http://localhost:8000/api/`

| Bölüm | Metod | URL | Açıklama |
|---|---|---|---|
| **Inventory** | GET / POST | `/inventory/medicines/` | İlaçları listele / Yeni ilaç ekle |
| **Patients** | GET / POST | `/patients/` | Hastaları listele / Yeni hasta ekle |
| **Procurement** | GET / POST | `/procurement/` | Tedarikçileri listele / Yeni tedarikçi ekle |
| **Sales (POS)** | POST | `/sales/checkout/` | Satışı tamamla ve stoktan düş |

## 📦 Veri Modelleri (JSON Yapısı)

### 1. Medicine (İlaç)
```json
{
    "id": 1,
    "name": "Parol",
    "expiry_date": "2025-12-01",
    "price": "50.00",
    "form_type": "tablet",
    "how_many": 100
}
```

### 2. Patient (Hasta)
```json
{
    "id": 1,
    "first_name": "Ahmet",
    "last_name": "Yılmaz",
    "phone_number": "5551234567",
    "address": "İstanbul..."
}
```

### 3. Procurement (Tedarikçi)
```json
{
    "id": 1,
    "name": "Selçuk Ecza Deposu",
    "phone_number_proc": "2121234567",
    "email": "info@selcukecza.com",
    "address_proc": "İstanbul..."
}
```

### 4. Sales (Satış İşlemi)
**Frontend'den Gönderilecek (POST Payload):**
```json
{
  "items": [
    { "product_id": 1, "quantity": 2 },
    { "product_id": 5, "quantity": 1 }
  ]
}
```

**Backend Cevabı (Success):**
```json
{
  "message": "Satış Başarılı!",
  "sale_id": 15,
  "total": 150.00
}
```

## ⚙️ Gelişmiş Özellikler (Advanced Features)

### 1. Redis & Cache
- **Sistem:** Redis (Port: 6379)
- **Amaç:** Sık erişilen verileri önbelleğe alarak performansı artırma.
- **Kullanım:** `django-redis` entegrasyonu hazır.

### 2. Celery (Arka Plan Görevleri)
- **Sistem:** Celery Worker + Celery Beat
- **Amaç:** Zamanlanmış (Cron job) ve uzun süren işlemleri arka planda yapma.
- **Ayarlar:** `core/celery.py` içinde ve `inventory/tasks.py` içinde görevler tanımlı.
- **Worker (İşçi):** `celery_worker` konteyneri
- **Beat (Zamanlayıcı):** `celery_beat` konteyneri

### 3. SMTP (E-Posta)
- **Mod:** Mailpit (Simülasyon)
- **Arayüz:** `http://localhost:8025` adresinden gönderilen mailleri görebilirsiniz.

## 🛠️ Kurulum Notları
Backend sunucusu şu komutla çalıştırılır:
`docker-compose up -d`

Sunucu `http://localhost:8000` adresinde çalışır.
