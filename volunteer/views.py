from django.shortcuts import render

from django.shortcuts import render, redirect, HttpResponseRedirect, render_to_response


# Create your views here.

def homepage_view(request):
    if request.method == 'GET':
        if not request.user.is_authenticated:
            context = {"nav1": "Login", "signed_in": False}
        else:
            context = {"nav1": "Logout", "signed_in": True}
        return render(request,'home.html', context)
        #return HttpResponse("Hello, world, You're at the volunteer home page")
    else:
        return render(request, "layout.html")
