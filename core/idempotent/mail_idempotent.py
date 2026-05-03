from functools import wraps
from django.core.cache import cache

#receipt.py için yaptık
def mail_idempotent(expire=30):
    """
    Mail Task Idempotency Decorator
    Celery tasklarının aynı ID ile tekrar çalışmasını engeller.
    
    expire: Cache süresi (saniye) - Varsayılan 24 saat (1 gün)
    Mailin tekrar gitmemesi için id'yi 1 gün tutmak yeterlidir.
    """
    def decorator(task_func):
        @wraps(task_func)
        def _wrapped_task(self, unique_id, *args, **kwargs):
            
            task_name = task_func.__name__
            cache_key = f"mail_sent_{task_name}_{unique_id}"
            
            # 1. Daha önce atılmış mı?
            if cache.get(cache_key):
                print(f" IDEMPOTENCY: {task_name} maili {unique_id} ID'si için ZATEN ATILMIŞ. Pas geçiliyor.")
                return f"Mail already sent for {unique_id}"

            # 2. Maili At (Task'ı çalıştır)
            result = task_func(self, unique_id, *args, **kwargs)
            
            # 3. Başarılıysa Kaydet
            # Task hata verirse buraya gelmez, dolayısıyla cache'e yazılmaz. (Retry olur)
            cache.set(cache_key, True, timeout=expire)
            print(f"✅ IDEMPOTENCY: {task_name} maili {unique_id} için işaretlendi.")
            
            return result
            
        return _wrapped_task
    return decorator
