from django.shortcuts import render
from .forms import Handle
from django.http import HttpResponseRedirect
from . import scrape

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
    val = scrape.get_contests(context["Handle"])
    t = {"context":context,"rating":scrape.get_rating(context["Handle"])}
    t.update(val)
    # for field in Handle():
    #     try:
    #         del response.session[field.label]
    #     except KeyError:
    #         pass
    return render(response,'login/profile.html',t)