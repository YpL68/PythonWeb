from django.urls import path
from . import views

app_name = 'fin_assist'

urlpatterns = [
    path('', views.main, name='main'),
    path('categories/', views.pay_categories, name='pay_categories'),
    path('categories/edit/<int:cat_id>', views.edit_pay_categories, name='edit_pay_categories'),
    path('categories/delete/<int:cat_id>', views.delete_pay_categories, name='delete_pay_categories'),
]
