import datetime
from django.utils import timezone
from .models import ColorGameTimeAdd

def check_task_time():
    now = timezone.now()  # Use timezone-aware now()
    print('➡ now:', now)
    
    try:
        start_time = ColorGameTimeAdd.objects.get().start_time
        print('➡ start_time:', start_time)
        
        time_remaining = now - start_time
        return 120-int(time_remaining.total_seconds())
    
    except ColorGameTimeAdd.DoesNotExist:
        print('No ColorGameTimeAdd record found')
        return None