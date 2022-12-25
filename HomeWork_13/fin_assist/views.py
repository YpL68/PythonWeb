from django.shortcuts import render


def main(request):
    return render(request, 'fin_assist/index.html', {})


def pay_categories(request):
    return render(request, 'fin_assist/pay_categories.html', context={"filter_str": "ghjfhgfjgh"})


def edit_pay_categories(request, cat_id):
    if request.method == 'POST':
        pass
    return render(request, 'fin_assist/pay_categories.html', context={"filter_str": str(cat_id)})
