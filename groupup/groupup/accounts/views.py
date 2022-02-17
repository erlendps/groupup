from re import template
from django.shortcuts import render
from django.http    import HttpResponse, HttpResponseRedirect
from .models import GroupUpUser
from django.contrib.auth.models import User


# Create your views here.
def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        profile_pic = request.POST.get('profile_pics')
        interests = request.POST.get('interests')
        password = request.POST.get('password')

        user = User(username = username, password = password)
        #Sjekk for unikt navn, hvis den ikke finnes lagre den
        if len(list(User.objects.filter(username=username))) != 0:
            #Feilmelding
            return
        groupupuser = GroupUpUser(user, profile_pic, interests)

        #Kan lage en FOR-løkke for interest
        groupupuser.save()


        return HttpResponseRedirect('/home')
    print(request.POST.get)
    return render(request, "registration/registerForm.html")

    # Create your views here.
def index(request):
    return render(request, "groupup/accounts/templates/registration/index.html")
