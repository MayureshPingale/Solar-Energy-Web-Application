from django.shortcuts import render , redirect
from django.http import HttpResponseRedirect,HttpResponse
from django.urls import reverse
from .models import UserProfile, Solaranalysis
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from .analysis import prediction,current_analysis,future_prediction,weekly,current_time_generation,total_energy_generation
from datetime import date
import ast

def index(request):
    return render(request,'homepage.html')


def register(request):
    if request.method == "POST":
        us1 = request.POST['username']
        ps1 = request.POST['password']
        coun = request.POST['city']
        print(us1,ps1,coun)
        user1 = UserProfile.objects.create(username=us1, password=ps1,
                                           city=coun)
        user1.save()
        new_solar_analysis = Solaranalysis.objects.create(customer=user1,current_day_production="",
                                                          current_day_usage="", weekly_day_production="[]",
                                                          weekly_day_usage="[]")
        new_solar_analysis.save()
        u1 = User.objects.create_user(username=us1,password=ps1)
        u1.save()

        u = authenticate(username=us1, password=ps1)

        if u is not None:
            login(request,u)
            return HttpResponseRedirect(reverse('input_option'))
        else:
            return HttpResponse("Some error has occurred")
    else:
        return render(request,'usercreation.html')


def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        print(password)
        try:
            customer= UserProfile.objects.get(username=username)
            print(customer.username)
            print(customer.password)
            if customer.username == username and customer.password == password:
                u = authenticate(username=request.POST['username'], password=request.POST['password'])
                login(request,u)
                return HttpResponseRedirect(reverse('input_option'))
            else:
                return HttpResponse("Wrong password")
        except:
                return HttpResponse("Username does not exist")
    else:
        return render(request,'loginpage.html')


def input_option(request):
    if request.method == "POST":
        if "curr" in request.POST:
            return HttpResponseRedirect(reverse('current_day_analysis'))
        elif "future" in request.POST:
            return HttpResponseRedirect(reverse('future_analysis'))
        elif "Weekly" in request.POST:
            return HttpResponseRedirect(reverse("weekly_analysis"))
    else:
        solar_user = Solaranalysis.objects.get(customer__username=request.user)
        print(solar_user.current_day_production)
        return render(request,"inputbutton.html")


def input_date(request):
    if not request.user.is_authenticated:
        return HttpResponse("Please login")
    elif request.method == "POST":
        date = request.POST['date_for_ghi']

        ans = prediction(date)
        args = {
                'ans':ans
        }
        return render(request,"table.html",args)

    else:
        return render(request,'datepicker.html')


def logout_view(request):
    logout(request)
    return render(request, 'homepage.html')


def current_day_analysis(request):
    solar_user = Solaranalysis.objects.get(customer__username=request.user)
    ans = solar_user.current_day_production
    ans = ast.literal_eval(ans)
    curr = current_time_generation(ans)
    total = total_energy_generation(ans)
    print(curr)
    print(ans)
    current_usage = 40/100 * curr
    dat = date.today()
    args = {
        'date': dat,
        'curr': curr,
        'ans': ans,
        'total': total,
        'current_usage': round(current_usage,2)
    }
    return render(request, 'current_day_analysis.html',args)


def future_analysis(request):
    if request.method == "POST":
        date1 = request.POST['date_for_ghi']
        customer = UserProfile.objects.get(username = request.user)
        ans, total, peak_hours = future_prediction(date1,customer.city)

        args = {
                'date': str(date1),
                'ans': ans,
                'total': total,
                'peak_hours': peak_hours
        }

        return render(request, 'future_analysis.html',args)
    else:
        return render(request, 'datepicker.html')


def weekly_analysis(request):
    ans, energy_left, total, prev_monday = weekly()
    print(ans)
    args = {
        'date': prev_monday,
        'ans': ans,
        'energy_left': energy_left,
        'total': total
    }
    return render(request, 'weekly.html', args)


def update_database(request):
    object_all_customer =  UserProfile.objects.all()

    for i in object_all_customer:
        solar_user = Solaranalysis.objects.get(customer__username=i.username)
        ans, curr, total = current_analysis(i.city)
        str_ans = str(ans)
        solar_user.current_day_production = str_ans
        weekly_production = solar_user.weekly_day_production
        weekly_production = ast.literal_eval(weekly_production)
        weekly_production.append(total)
        str_weekly_production = str(weekly_production)
        solar_user.weekly_day_production = str_weekly_production
        solar_user.save()

    return HttpResponse("Database updated")


def current_day_hourly_analysis(request):
    solar_user = Solaranalysis.objects.get(customer__username=request.user)
    ans = solar_user.current_day_production
    ans = ast.literal_eval(ans)
    args = {
        'ans': ans
    }
    return render(request,'table.html',args)


def future_hourly(request, date1):
    customer = UserProfile.objects.get(username=request.user)
    ans, total, peak_hours = future_prediction(date1, customer.city)
    args = {
        'ans': ans,
        'date':date1
    }
    return render(request, 'table.html', args)
