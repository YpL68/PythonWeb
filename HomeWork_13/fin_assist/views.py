from django.shortcuts import render


def main(request):
    return render(request, 'fin_assist/index.html', {})


def pay_categories(request):
    return render(request, 'fin_assist/pay_categories.html', context={})
