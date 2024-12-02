from django.urls import path
from .views import home,colorcontest,colorgame,contest,deposit,userlogin,invite,luckynamecontest,mycontest,numberguess,userprofile,withdraw, userlogout, updatedata, numberguessfifty, register


urlpatterns = [
    path('home/',home,name="home"),
    path('register/',register,name="register"),
    path('',userlogin,name="userlogin"),
    path('colorcontest/',colorcontest,name="colorcontest"),
    path('colorgame/',colorgame,name="colorgame"),
    path('contest/',contest,name="contest"),
    path('deposit/',deposit,name="deposit"),
    path('invite/',invite,name="invite"),
    path('luckynamecontest/',luckynamecontest,name="luckynamecontest"),
    path('mycontest/',mycontest,name="mycontest"),
    path('numberguess/',numberguess,name="numberguess"),
    path('numberguessfifty/',numberguessfifty,name="numberguessfifty"),
    path('userprofile/',userprofile,name="userprofile"),
    path('withdraw/',withdraw,name="withdraw"),
    path('logout/',userlogout,name="userlogout"),
    path('updatedata/',updatedata, name="updatedata")
]
