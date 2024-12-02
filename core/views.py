from django.shortcuts import render, redirect
from django.http import HttpResponse , JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
import datetime ,time
from .models import BallColorGame, UserAmount, UserHistory, PreviousHistory, ColorGameTotalProfitStatistics,NumberGameLastWinTwenty, NumberGameTwenty, NumberGametwentyRecords, NumberGameDeclarations, NumberGameFifty , NumberGameFiftyLastWin,NumberGameFiftyRecords, NumberGameFiftyDeclarations, AccountDetails, DepositDetails, NumberGameTwentyProfit, NumberGameFiftyProfit, ColorGameTimeAdd
import decimal
# from .utils import time_until_next_cron_job
import random
from .check_time import check_task_time


from django.http import JsonResponse
from core.utils import remaining_time
def time_remaining_view(request):
    return JsonResponse({'remaining_time': remaining_time()})

@login_required(login_url='userlogin')
def home(request):
    balance=get_user_balance(request)
    return render(request, 'core/home.html',{"balance": balance})


@csrf_exempt
def userlogin(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        username = str(request.POST.get('username'))
        password = str(request.POST.get('password'))
        user = authenticate(request,username=username,password=password)
        if user is not None:
            login(request, user)
            print('User login successful')
            # return redirect('home')
            return JsonResponse({'status': 'success'})
        
        else:
            return JsonResponse({'status': 'Invalid username or password'})
    return render(request, 'core/userlogin.html')


@csrf_exempt
def register(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()
        confirm_password = request.POST.get('confirm_password', '').strip()

        # Check if passwords match
        if password != confirm_password:
            return JsonResponse({'status': 'error', 'message': 'Passwords do not match'})

        # Check if username already exists
        if User.objects.filter(username=username).exists():
            return JsonResponse({'status': 'error', 'message': 'Username already exists'})

        # Create and save the user
        user = User.objects.create(username=username)
        user.set_password(password)  # Hash the password
        user.save()

        # Authenticate and log in the user
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({'status': 'success', 'message': 'Registration successful'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Invalid username or password'})
    
    return render(request, 'core/registration.html')
        

@csrf_exempt
@login_required(login_url='userlogin')
def colorcontest(request):
    return render(request, 'core/colorcontest.html')


@csrf_exempt
@login_required(login_url='userlogin')
def colorgame(request):
    previous_history = get_previous_winrecord()
    allwinrecord_lst= get_win_record(request)
    
    balance=get_user_balance(request)
    ball_color_game_data=get_ball_color_game_data(request)
    time_remaining= check_task_time()
    print('➡ time_remaining:', time_remaining)
    if request.method == 'POST':
        ballcolor = request.POST.get('ballcolor')
        betamount = decimal.Decimal(request.POST.get('betamount'))
        if (balance - betamount)<0:
            return JsonResponse({'status': 'Insufficient balance'})
        bettime = get_time()
        BallColorGame.objects.create(user=request.user, ball_color=ballcolor, bet_amount=betamount, bet_time=bettime).save()        
        ball_color_game_data = get_ball_color_game_data(request)
        current_balance=0
        if UserAmount.objects.filter(user=request.user).exists():
            useramountobj= UserAmount.objects.get(user=request.user)
            useramountobj.balance -= betamount
            useramountobj.save()
            current_balance = useramountobj.balance
        
        return JsonResponse({'status': 'success',"ballcolorgamedata":ball_color_game_data,"currentbalance":current_balance})
    return render(request, 'core/colorgame.html',{"ballcolorgamedata":ball_color_game_data,"time_remaining":time_remaining,"balance":balance,"allwinrecord_lst":allwinrecord_lst,"previous_history":previous_history})


@csrf_exempt
@login_required(login_url='userlogin')
def contest(request):
    return render(request, 'core/contest.html')


@csrf_exempt
@login_required(login_url='userlogin')
def deposit(request):
    status=''
    if DepositDetails.objects.filter(user=request.user).exists():
        deposit_obj = DepositDetails.objects.get(user=request.user)
        status = deposit_obj.status
    balance=get_user_balance(request)
    if request.method == 'POST':
        utr_number = request.POST.get('utr_number')
        if utr_number.strip() != '':
            if DepositDetails.objects.filter(ref_number=utr_number).exists():
                return JsonResponse({'status':'UTR Number already exists'})
            if DepositDetails.objects.filter(user=request.user).exists():
                deposit_obj = DepositDetails.objects.get(user=request.user)
                deposit_obj.amount = ""
                deposit_obj.ref_number = utr_number
                deposit_obj.status = "Deposit request pending.."
                deposit_obj.save()
            else:
                DepositDetails.objects.create(user=request.user,amount="",ref_number=utr_number,status="Deposit request pending..").save()
                
            return JsonResponse({'status':'success'})
        else:
            return JsonResponse({'status':'Invalid UTR Number'})
    return render(request, 'core/deposit.html',{"balance":balance,"status":status})

@login_required(login_url='userlogin')
def invite(request):
    return render(request, 'core/invite.html')


@csrf_exempt
@login_required(login_url='userlogin')
def luckynamecontest(request):
    return render(request, 'core/luckynamecontest.html')


@csrf_exempt
@login_required(login_url='userlogin')
def mycontest(request):
    return render(request, 'core/mycontest.html')


@csrf_exempt
@login_required(login_url='userlogin')
def numberguess(request):
    update_number_game_result_data()
    remaining_balance= get_user_balance(request)
    lst=[]
    number_last_win_lst= []
    if NumberGameTwenty.objects.filter(user=request.user).exists():
        obj= NumberGameTwenty.objects.filter(user=request.user)
        for i in obj:
            lst.append((i.created_at,i.number))
    if NumberGameLastWinTwenty.objects.all().exists():
        for obj in NumberGameLastWinTwenty.objects.all():
            number_last_win_lst.append((obj.time,obj.number))     
    if request.method == 'POST':
        if remaining_balance >=20:
            guessnumber = int(request.POST.get('selectednumber'))
            NumberGameTwenty.objects.create(user= request.user, number = guessnumber, created_at = datetime.datetime.now().strftime("%I:%M %p"))
            cal_all_amounts(guessnumber)
            user_amount_obj=UserAmount.objects.get(user=request.user)
            user_amount_obj.balance -= 20
            user_amount_obj.save()
            new_lst=[]
            obj= NumberGameTwenty.objects.filter(user=request.user)
            for i in obj:
                new_lst.append((i.created_at,i.number))
            new_lst.reverse()
            remaining_balance= get_user_balance(request)
            return JsonResponse({'status':"true",'guessnumber':guessnumber,"remaining_balance":remaining_balance,"my_history":new_lst})
        else:
            return JsonResponse({'status':"false","message":'Insufficient balance',"remaining_balance":remaining_balance})
    number_last_win_lst.reverse()
    return render(request, 'core/numberguess.html',{"remaining_balance":remaining_balance,"lst_balance":lst,"number_last_win_lst":number_last_win_lst})

@csrf_exempt
@login_required(login_url='userlogin')
def numberguessfifty(request):
    update_number_game_result_data_fifty()
    remaining_balance= get_user_balance(request)
    lst=[]
    number_last_win_lst= []
    if NumberGameFifty.objects.filter(user=request.user).exists():
        obj= NumberGameFifty.objects.filter(user=request.user)
        for i in obj:
            lst.append((i.created_at,i.number))
    if NumberGameFiftyLastWin.objects.all().exists():
        for obj in NumberGameFiftyLastWin.objects.all():
            number_last_win_lst.append((obj.time,obj.number))     
    if request.method == 'POST':
        if remaining_balance >=50:
            guessnumber = int(request.POST.get('selectednumber'))
            NumberGameFifty.objects.create(user= request.user, number = guessnumber, created_at = datetime.datetime.now().strftime("%I:%M %p"))
            cal_all_amounts_fifty(guessnumber)
            user_amount_obj=UserAmount.objects.get(user=request.user)
            user_amount_obj.balance -= 50
            user_amount_obj.save()
            new_lst=[]
            obj= NumberGameFifty.objects.filter(user=request.user)
            for i in obj:
                new_lst.append((i.created_at,i.number))
            new_lst.reverse()
            remaining_balance= get_user_balance(request)
            return JsonResponse({'status':"true",'guessnumber':guessnumber,"remaining_balance":remaining_balance,"my_history":new_lst})
        else:
            return JsonResponse({'status':"false","message":'Insufficient balance',"remaining_balance":remaining_balance})
    number_last_win_lst.reverse()
    return render(request, 'core/numberguessfifty.html',{"remaining_balance":remaining_balance,"lst_balance":lst,"number_last_win_lst":number_last_win_lst})


@csrf_exempt
@login_required(login_url='userlogin')
def userprofile(request):
    remaining_balance= get_user_balance(request)
    return render(request, 'core/userprofile.html',{"remaining_balance":remaining_balance})


@csrf_exempt
@login_required(login_url='userlogin')
def withdraw(request):
    message= None
    if AccountDetails.objects.filter(user=request.user).exists():
        account_obj = AccountDetails.objects.get(user=request.user)
        message= f"Amount {account_obj.amount} is  {account_obj.message}"
    balance = get_user_balance(request)
    if request.method == 'POST':
        withdraw_amount = int(request.POST.get('amount'))
        ac_number = request.POST.get('acnumber')
        ifsc_code = request.POST.get('ifsccode')
        useramountobj= UserAmount.objects.get(user=request.user)
        if useramountobj.balance >= withdraw_amount and withdraw_amount >= 200:
            if AccountDetails.objects.filter(user=request.user).exists():
                account_obj = AccountDetails.objects.get(user=request.user)
                account_obj.amount = withdraw_amount
                account_obj.account_number = ac_number
                account_obj.ifsc_code = ifsc_code
                account_obj.message = "pending ..."
                account_obj.status = False
                account_obj.save()
                
            else:
                AccountDetails.objects.create(user=request.user, amount=withdraw_amount, account_number=ac_number, ifsc_code=ifsc_code, message="pending...", status=False)
            useramountobj.balance -= withdraw_amount
            useramountobj.save()
            balance = get_user_balance(request)
        if AccountDetails.objects.filter(user=request.user).exists():
            account_obj = AccountDetails.objects.get(user=request.user)
            message= f"Amount {account_obj.amount} is  {account_obj.message}"
        
    return render(request, 'core/withdraw.html',{"balance":balance,"message":message})


@csrf_exempt
@login_required(login_url='userlogin')
def userlogout(request):
    logout(request)
    return redirect('userlogin')




@login_required(login_url='userlogin')
def updatedata(request):
    # update_user_balance()
    current_balance=0
    if UserAmount.objects.filter(user=request.user).exists():
        useramountobj= UserAmount.objects.get(user=request.user)
        current_balance = useramountobj.balance
    ball_color_game_data = get_ball_color_game_data(request)
    allwinrecord_lst= get_win_record(request)
    previous_history = get_previous_winrecord()
    return JsonResponse({"status": "success","currentbalance":current_balance,"ballcolorgamedata":ball_color_game_data,"allwinrecord_lst":allwinrecord_lst,"previous_history":previous_history})


# // helper functions 

def get_time():
    current_time = datetime.datetime.now().time()
    current_time = current_time.strftime("%I:%M %p")
    return current_time

def get_ball_color_game_data(request):
    ballcolorgameobjs=BallColorGame.objects.filter(user=request.user)
    ball_color_game_data = []
    for ballcolorgameobj in ballcolorgameobjs:
        ball_color = ballcolorgameobj.ball_color
        bet_amount = ballcolorgameobj.bet_amount
        bet_time = ballcolorgameobj.bet_time
        ball_color_game_data.append((bet_time, ball_color, bet_amount))
    return ball_color_game_data

def get_delete_ball_color_game_data():
    BallColorGame.objects.all().delete()
    
    
def get_ball_color_game_result():
    blue_ball_total_amount =0
    green_ball_total_amount =0
    purple_ball_total_amount =0
    for i in BallColorGame.objects.all():
        if i.ball_color == "blue":
            blue_ball_total_amount +=i.bet_amount
        elif i.ball_color == "green":
            green_ball_total_amount +=i.bet_amount
        else:
            purple_ball_total_amount +=i.bet_amount
            
    dict_data = {
            "blue": round(decimal.Decimal(blue_ball_total_amount)*decimal.Decimal(1.9),2),
            "green": round(decimal.Decimal(green_ball_total_amount)*decimal.Decimal(1.9),2),
            "purple": round(decimal.Decimal(purple_ball_total_amount)*decimal.Decimal(5),2)
            }
    total_amount = blue_ball_total_amount + green_ball_total_amount + purple_ball_total_amount
    sorted_items = sorted(dict_data.items(), key=lambda kv: (kv[1], kv[0]))
    profit = total_amount - sorted_items[0][1]
    return sorted_items[0][0], sorted_items, total_amount ,profit
    
    
    
def get_user_balance(request):
    if UserAmount.objects.filter(user=request.user).exists():
        user_amount_obj=UserAmount.objects.get(user=request.user)
        return user_amount_obj.balance
    return 0


    
def update_user_balance():
    if BallColorGame.objects.all().exists():
        profit= get_ball_color_game_result()[3]
        color= get_ball_color_game_result()[0]
        user_lst=[]
        for userobj in BallColorGame.objects.all():
            user_lst.append(userobj.user)
        for user in set(user_lst):
            for lose_color_amount in get_loss_color_amount(user,color):
                losecolor,amount=lose_color_amount
                UserHistory.objects.create(user=user,bet_color=losecolor, bet_amount=-amount).save()
                # BallColorGame.objects.filter(user=currentuser.user).delete()
        # for user in set(user_lst):
            total_amount =0
            for item in BallColorGame.objects.filter(user=user,ball_color=color):
                total_amount +=item.bet_amount
            if UserAmount.objects.filter(user=user).exists():
                current_balance = UserAmount.objects.get(user=user)
                if color == 'purple':
                    winamount = decimal.Decimal(total_amount)*5
                    if winamount > 0:
                        if BallColorGame.objects.filter(user=user,ball_color=color).exists():
                            UserHistory.objects.create(user=user,bet_color=color, bet_amount=+winamount).save()
                    current_balance.balance += winamount
                else :
                    winamount = round(decimal.Decimal(total_amount)*decimal.Decimal(1.9),2)
                    if winamount > 0:
                        if BallColorGame.objects.filter(user=user,ball_color=color).exists():
                            UserHistory.objects.create(user=user,bet_color=color, bet_amount=+winamount).save()
                    current_balance.balance += winamount
                current_balance.save()
                # if BallColorGame.objects.filter(user=user).exists():
        PreviousHistory.objects.create(bet_color=color).save()                
        color_game_total_profit(profit)     
        get_delete_ball_color_game_data()
        return JsonResponse({"success": True})
    else:
        color = random.choice(["blue", "green", "purple"])
        PreviousHistory.objects.create(bet_color=color).save()


# def cron_status_view(request):
#     cron_expression = '*/2 * * * *'  # Example cron job running every 2 minutes
#     remaining_time = time_until_next_cron_job(cron_expression)

#     # Format the remaining time for response
#     remaining_minutes, remaining_seconds = divmod(remaining_time.total_seconds(), 60)
#     remaining_time_formatted = f"0{int(remaining_minutes)}:{int(remaining_seconds)}"

#     return {
#         'next_run_in':int(remaining_time.total_seconds()),'displaytime':remaining_time_formatted
#     }
    
    
def get_loss_color_amount(currentuser,win_color):
    color_amount=[]
    all_colors= {"green","blue","purple"}
    loss_colors= all_colors - {win_color}
    print('➡ loss_colors:', loss_colors)
    for color in loss_colors:
        ballcolorobj= BallColorGame.objects.filter(user=currentuser,ball_color=color)
        for i in ballcolorobj:
            color_amount.append((color,i.bet_amount))
    # win_obj= BallColorGame.objects.filter(user=currentuser,ball_color=win_color)
    # for wincolor in win_obj:
    #     color_amount.append((wincolor.ball_color,wincolor.bet_amount))
    return color_amount

def get_win_record(request):
    allwinrecord_lst=[]
    if UserHistory.objects.filter(user=request.user).exists():
        for useramountobj in UserHistory.objects.filter(user=request.user):
            allwinrecord_lst.append((useramountobj.created_at,useramountobj.bet_color,useramountobj.bet_amount))
        
    allwinrecord_lst.reverse()
    return allwinrecord_lst

def get_previous_winrecord():
    previous_winrecord_lst=[]
    if PreviousHistory.objects.all().exists():
        for previoushistoryobj in PreviousHistory.objects.all():
            previous_winrecord_lst.append((previoushistoryobj.created_at,previoushistoryobj.bet_color))
    previous_winrecord_lst.reverse()
    return previous_winrecord_lst

def color_game_total_profit(profit):
    if UserAmount.objects.all().exists():
        total_remaining = 0
        for i in UserAmount.objects.all():
            total_remaining += i.balance 
        obj=ColorGameTotalProfitStatistics.objects.get()
        obj.profit +=profit
        obj.remaining_amount = total_remaining
        obj.save()
        
        
        
def cal_all_amounts(sel_number):

    if NumberGametwentyRecords.objects.filter(sel_number=sel_number).exists():
        obj = NumberGametwentyRecords.objects.get(sel_number=sel_number)
        obj.amount += 20
        obj.save()
    else:
        NumberGametwentyRecords.objects.create(sel_number=sel_number, amount=20).save()
        
        
        
# //////////////////////////////// Number Game Logic //////////////////////////////


def update_number_game_result_data():
    if NumberGameDeclarations.objects.all().exists():
        obj = NumberGameDeclarations.objects.all().first()        

        if obj.declaration:
            for numobj in NumberGameTwenty.objects.all():
                if numobj.number == obj.number:
                    winuser = numobj.user
                    o= UserAmount.objects.get(user=winuser)
                    o.balance += 160
                    o.save()
            NumberGameLastWinTwenty.objects.create(number = obj.number,time = datetime.datetime.now().date()).save()
            obj.declaration= False
            obj.save()
            total_amount=0
            win_num_amount=0
            for i in NumberGametwentyRecords.objects.all():
                total_amount += i.amount
            if NumberGametwentyRecords.objects.filter(sel_number=obj.number).exists():
                win_num_amount=NumberGametwentyRecords.objects.get(sel_number=obj.number).amount
                
            print('➡ win_num_amount:', win_num_amount)
            total_profit = total_amount - win_num_amount*8
            print('➡ total_profit:', total_profit)
            NumberGameTwentyProfit.objects.create(profit=total_profit)
            if NumberGameTwenty.objects.all().exists():
                NumberGameTwenty.objects.all().delete()
                NumberGametwentyRecords.objects.all().delete()
                
                

def update_number_game_result_data_fifty():
    if NumberGameFiftyDeclarations.objects.all().exists():
        obj = NumberGameFiftyDeclarations.objects.all().first()        

        if obj.declaration:
            for numobj in NumberGameFifty.objects.all():
                if numobj.number == obj.number:
                    winuser = numobj.user
                    o= UserAmount.objects.get(user=winuser)
                    o.balance += 400
                    o.save()
            NumberGameFiftyLastWin.objects.create(number = obj.number,time = datetime.datetime.now().date()).save()
            obj.declaration= False
            obj.save()
            total_amount=0
            win_num_amount= 0
            for i in NumberGameFiftyRecords.objects.all():
                total_amount += i.amount
            if NumberGameFiftyRecords.objects.filter(sel_number=obj.number).exists():
                win_num_amount=NumberGameFiftyRecords.objects.get(sel_number=obj.number).amount
            total_profit = total_amount - win_num_amount*8
            print('➡ total_profit:', total_profit)
            NumberGameFiftyProfit.objects.create(profit=total_profit)
            if NumberGameFifty.objects.all().exists():
                NumberGameFifty.objects.all().delete()
                NumberGameFiftyRecords.objects.all().delete()
                
def cal_all_amounts_fifty(sel_number):

    if NumberGameFiftyRecords.objects.filter(sel_number=sel_number).exists():
        obj = NumberGameFiftyRecords.objects.get(sel_number=sel_number)
        obj.amount += 20
        obj.save()
    else:
        NumberGameFiftyRecords.objects.create(sel_number=sel_number, amount=20).save()
                    