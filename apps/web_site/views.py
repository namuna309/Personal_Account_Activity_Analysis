from django.shortcuts import render

# Create your views here.

def combine_charts(request):
    return render(request, 'web_site/combine_charts.html')