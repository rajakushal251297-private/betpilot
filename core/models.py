from django.db import models
from django.contrib.auth.models import User


class BallColorGame(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ball_color = models.CharField(max_length=20)
    bet_amount = models.DecimalField(max_digits=10, decimal_places=2)
    bet_time = models.CharField(max_length=20)

    

class UserAmount(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=10, decimal_places=2)
    
class UserHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bet_color = models.CharField(max_length=200,default='')
    bet_amount= models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        
        # Keep only the last 10 records
        if UserHistory.objects.count() > 10:
            # Delete older records, keeping only the latest 10
            lst=UserHistory.objects.order_by('-created_at')[10:]
            for i in lst:
                UserHistory.objects.get(created_at=i.created_at).delete()
            
            # UserHistory.objects.filter(created_at=lst).delete()
class PreviousHistory(models.Model):
    bet_color= models.CharField(max_length=200,default='')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        
        # Keep only the last 10 records
        if PreviousHistory.objects.count() > 10:
            lst=PreviousHistory.objects.order_by('-created_at')[10:]
            for i in lst:
                PreviousHistory.objects.get(created_at=i.created_at).delete()   

class ColorGameTotalProfitStatistics(models.Model):
    profit = models.DecimalField(max_digits=10, decimal_places=2)
    remaining_amount = models.DecimalField(max_digits=10, decimal_places=2)
    
    
class NumberGameTwenty(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    number = models.IntegerField()
    created_at = models.CharField(max_length=200)
    

class NumberGameLastWinTwenty(models.Model):
    number = models.IntegerField()
    time = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        
        # Keep only the last 10 records
        if NumberGameLastWinTwenty.objects.count() > 10:
            lst=NumberGameLastWinTwenty.objects.order_by('-created_at')[10:]
            for i in lst:
                NumberGameLastWinTwenty.objects.get(created_at=i.created_at).delete()
    
    
class NumberGametwentyRecords(models.Model):
    sel_number = models.IntegerField()
    amount = models.IntegerField()
    
   
    
class NumberGameDeclarations(models.Model):
    number = models.IntegerField()
    declaration = models.BooleanField(default=False)
    
    
# ==================================================

class NumberGameFifty(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    number = models.IntegerField()
    created_at = models.CharField(max_length=200)
    

class NumberGameFiftyLastWin(models.Model):
    number = models.IntegerField()
    time = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        
        # Keep only the last 10 records
        if NumberGameFiftyLastWin.objects.count() > 10:
            lst=NumberGameFiftyLastWin.objects.order_by('-created_at')[10:]
            for i in lst:
                NumberGameFiftyLastWin.objects.get(created_at=i.created_at).delete()
    
    
class NumberGameFiftyRecords(models.Model):
    sel_number = models.IntegerField()
    amount = models.IntegerField()
    
   
    
class NumberGameFiftyDeclarations(models.Model):
    number = models.IntegerField()
    declaration = models.BooleanField(default=False)
    
    
    
class AccountDetails(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    amount = models.CharField(max_length=200)
    account_number = models.CharField(max_length=200)
    ifsc_code = models.CharField(max_length=200)
    message = models.CharField(max_length=200)
    status = models.BooleanField(default=False)
    
    
    
class DepositDetails(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.CharField(max_length=200)
    ref_number = models.CharField(max_length=200)
    status = models.CharField(max_length=200)
    
    
class NumberGameTwentyProfit(models.Model):
    profit= models.CharField(max_length=200)
    
    
    
class NumberGameFiftyProfit(models.Model):
    profit= models.CharField(max_length=200)
    
    
    
class ColorGameTimeAdd(models.Model):
    start_time= models.DateTimeField()