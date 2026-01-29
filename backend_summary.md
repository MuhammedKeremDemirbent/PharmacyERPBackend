# Pharmacy ERP - Backend Özeti

Bu dosya, Frontend projesine başlarken referans olması için oluşturulmuştur.

## 🚀 API Uç Noktaları (Endpoints)

Base URL: `http://localhost:8000/api/`

| Bölüm | Metod | URL | Açıklama |
|---|---|---|---|
| **Inventory** | GET / POST | `/inventory/medicines/` | İlaçları listele / Yeni ilaç ekle |
| **Patients** | GET / POST | `/patients/` | Hastaları listele / Yeni hasta ekle |
| **Procurement** | GET / POST | `/procurement/` | Tedarikçileri listele / Yeni tedarikçi ekle |

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
    "name": "Ahmet Yılmaz",
    "phone": "5551234567",
    "address": "İstanbul..."
}
```

### 3. Procurement (Tedarikçi)
```json
{
    "id": 1,
    "name": "Selçuk Ecza Deposu",
    "phone": "2121234567",
    "address": "İstanbul..."
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
- **Ayarlar:** `core/celery.py` içinde ve Redis Broker ile çalışır.

### 3. SMTP (E-Posta)
- **Mod:** Console Backend (Geliştirme Amaçlı)
- **Durum:** Mailler tarayıcı yerine terminal çıktısı olarak görünür. `docker-compose logs` ile okunabilir.

## 🛠️ Kurulum Notları
Backend sunucusu şu komutla çalıştırılır:
`docker-compose up -d`

Sunucu `http://localhost:8000` adresinde çalışır.
