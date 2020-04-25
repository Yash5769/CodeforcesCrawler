from django.shortcuts import render
from .forms import Handle
from django.http import HttpResponseRedirect
from . import scrape
from . import Selenium_scraper
from .models import time_table, languages
from . import graph


# Create your views here.
def home(response):
    return render(response, 'login/home.html')
    
def Input(response):
    response. method = "POST"
    if (response.method == "POST"):
        form = Handle(response.POST)
        if (form.is_valid()):
            for field in form:
                response.session[field.label] = form.cleaned_data[field.label]
            return HttpResponseRedirect("/profile")
    else:
        form = Handle()
    return render(response, 'login/login.html',{"form":form})
    
def profile(response):
    context = {}
    # form = Handle
    h = response.session.get('Handle') 
    if(h==None):
        return HttpResponseRedirect("/login")
    for field in Handle():
        context.update({field.label: response.session.get(field.label)})
    graphs = {"output":graph.get_submission_chart(h).render(),"verdict":graph.get_verdict_chart(h).render(),"level":graph.get_level_chart(h).render()}
    val = {"values": scrape.get_contests(context["Handle"])}
    
    t = {"context":context,"rating":scrape.get_rating(context["Handle"])}
    t.update(val)
    t.update(graphs)
    # for field in Handle():
    #     try:
    #         del response.session[field.label]
    #     except KeyError:
    #         pass
    return render(response, 'login/profile.html', t)
    
def contests(response):
    scrape.get_timetable()
    context = {"timetable": time_table.objects.all()}
    # print(context)
    # print(response.session['django_timezone'])
    return render(response,'login/contests.html',context)
