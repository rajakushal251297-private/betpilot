from celery import shared_task
from .views import update_user_balance
import datetime
from .models import ColorGameTimeAdd



@shared_task
def my_task():
    currenttime = datetime.datetime.now()
    if ColorGameTimeAdd.objects.all().exists():
        color_obj=ColorGameTimeAdd.objects.get()
        color_obj.start_time=currenttime
        color_obj.save()
    else:
        ColorGameTimeAdd.objects.create(start_time=currenttime).save()
        color_obj=ColorGameTimeAdd.objects.get()
        
        with open("my_task.txt",'w') as f:
            f.write(f"currenttime : {color_obj}")
    
    update_user_balance()
    print("This task runs every 2 minutes!")
