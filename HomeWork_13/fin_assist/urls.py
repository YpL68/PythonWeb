from django.urls import path
from . import views

app_name = 'fin_assist'

urlpatterns = [
    path('', views.main, name='main'),
    path('categories/', views.pay_categories, name='pay_categories'),
    path('categories/<int:cat_id>', views.edit_pay_categories, name='edit_pay_categories'),
]
