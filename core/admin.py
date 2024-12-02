from django.contrib import admin
from .models import BallColorGame, UserAmount, UserHistory, PreviousHistory, ColorGameTotalProfitStatistics, NumberGameTwenty , NumberGameLastWinTwenty,NumberGametwentyRecords, NumberGameDeclarations, NumberGameFifty , NumberGameFiftyLastWin,NumberGameFiftyRecords, NumberGameFiftyDeclarations, AccountDetails, DepositDetails, NumberGameTwentyProfit, NumberGameFiftyProfit,ColorGameTimeAdd

@admin.register(BallColorGame)
class BallColorGameAdmin(admin.ModelAdmin):
    list_display = ('user', 'ball_color', 'bet_amount', 'bet_time')

@admin.register(UserAmount)
class UserAmountAdmin(admin.ModelAdmin):
    list_display = ('user', 'balance')
    

@admin.register(UserHistory)
class UserHistoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'bet_color',"created_at","bet_amount")
    
@admin.register(PreviousHistory)
class PreviousHistoryAdmin(admin.ModelAdmin):
    list_display = ('bet_color',"created_at")
    
@admin.register(ColorGameTotalProfitStatistics)
class ColorGameTotalProfitStatisticsAdmin(admin.ModelAdmin):
    list_display = ('profit', 'remaining_amount')
    

@admin.register(NumberGameTwenty)
class NumberGameTwentyAdmin(admin.ModelAdmin):
    list_display = ('user', 'number', 'created_at')
    

@admin.register(NumberGameLastWinTwenty)
class NumberGameLastWinTwentyAdmin(admin.ModelAdmin):
    list_display = ('number', 'time')
    
    
    

@admin.register(NumberGametwentyRecords)
class NumberGametwentyRecordsAdmin(admin.ModelAdmin):
    list_display = ('sel_number','amount')
    

@admin.register(NumberGameDeclarations)
class NumberGameDeclarationsAdmin(admin.ModelAdmin):
    list_display = ('number','declaration')
    

# ///////////////////////////////////////////


@admin.register(NumberGameFifty)
class NumberGameFiftyAdmin(admin.ModelAdmin):
    list_display = ('user', 'number', 'created_at')
    

@admin.register(NumberGameFiftyLastWin)
class NumberGameFiftyLastWinAdmin(admin.ModelAdmin):
    list_display = ('number', 'time')
    
    
    

@admin.register(NumberGameFiftyRecords)
class NumberGameFiftyRecordsAdmin(admin.ModelAdmin):
    list_display = ('sel_number','amount')
    

@admin.register(NumberGameFiftyDeclarations)
class NumberGameFiftyDeclarationsAdmin(admin.ModelAdmin):
    list_display = ('number','declaration')
    


@admin.register(AccountDetails)
class AccountDetailsAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'account_number', 'ifsc_code', 'status',"message")
    
    

@admin.register(DepositDetails)
class DepositDetailsAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'ref_number', 'status')
    
    

@admin.register(NumberGameTwentyProfit)
class NumberGameTwentyProfitAdmin(admin.ModelAdmin):
    list_display = ('profit',)
    
    

@admin.register(NumberGameFiftyProfit)
class NumberGameFiftyProfitAdmin(admin.ModelAdmin):
    list_display = ('profit',)
    
    
@admin.register(ColorGameTimeAdd)
class ColorGameTimeAddAdmin(admin.ModelAdmin):
    list_display = ('start_time',)