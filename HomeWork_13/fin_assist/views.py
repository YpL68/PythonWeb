from django.shortcuts import render, redirect
from . models import FinCategory
from django.contrib import messages


def main(request):
    return render(request, 'fin_assist/index.html', {})


def pay_categories(request):
    if request.method == 'POST':
        filter_str = request.POST["filter_str"]
    else:
        filter_str = ""

    if filter_str:
        categories = FinCategory.objects.filter(name__icontains=filter_str).order_by("name")
    else:
        categories = FinCategory.objects.all().order_by("name")

    return render(request, 'fin_assist/pay_categories.html',
                  context={"filter_str": filter_str, "categories": categories})


def edit_pay_categories(request, cat_id):
    if request.method == 'POST':
        try:
            if cat_id == 0:
                cat = FinCategory(
                    name=request.POST['cat_name'],
                    description=request.POST['cat_desc']
                )
                cat.save()
            else:
                cat = FinCategory.objects.get(pk=cat_id)
                print(cat.name)
                cat.name = request.POST['cat_name']
                cat.description = request.POST['cat_desc']
                cat.save()

            messages.add_message(request, messages.SUCCESS, "Operation was successful", "success")
        except Exception as err:
            messages.add_message(request, messages.ERROR, f"Operation was aborted: {str(err)}", "danger")
    return redirect('/categories/')


def delete_pay_categories(request, cat_id):
    try:
        cat = FinCategory.objects.get(pk=cat_id)
        cat.delete()
        messages.add_message(request, messages.SUCCESS, "Operation was successful", "success")
    except Exception as err:
        messages.add_message(request, messages.ERROR, f"Operation was aborted: {str(err)}", "danger")
    return redirect('/categories/')
