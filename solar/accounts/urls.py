from django.urls import path,include
from . import views

urlpatterns = [
    path('register/',views.register,name="register"),
    path('login_user/', views.login_view, name="login"),
    path('',views.index,name='index'),
    path('input/',views.input_option,name='input_option'),
    path('logout_user/',views.logout_view,name="logout"),
    path('current_day_analysis/',views.current_day_analysis,name="current_day_analysis"),
    path('future_analysis/',views.future_analysis,name="future_analysis"),
    path('weekly_analysis/',views.weekly_analysis,name="weekly_analysis"),
    path('input_date/',views.input_date,name="input_date"),
    path('update_database/',views.update_database,name="update_database"),
    path('current_hourly/', views.current_day_hourly_analysis,name="current_hourly"),
    path('future_hourly/<str:date1>/', views.future_hourly, name="future_hourly")

]

