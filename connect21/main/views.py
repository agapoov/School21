from django.shortcuts import render


def home_page(request):
    return render(request, 'main/home.html')


def page_not_found(request, exception):
    return render(request, '404.html', status=404)


def about(request):
    return render(request, 'main/about.html')
