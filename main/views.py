from django.shortcuts import render, redirect
from .models import Discussion, Comment
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages

def homepage(request):
    return render(request, "main/home.html", {"discussions" : Discussion.objects.all})

def discussion(request, dis_t):
    dis = Discussion.objects.get(title=dis_t)
    comments = Comment.objects.all().filter(discussion=dis)
    return render(request, "main/discussion.html", {"discussion" : dis, "comments" : comments})

def newmessage_request(request):
    if(request.user.is_authenticated):
        if(request.method == "POST"):
            try:
                if(request.POST['comment'] != ""):
                    dis = Discussion.objects.get(title=request.POST['discussion'])
                    form = Comment(author=request.user, comment=request.POST['comment'], discussion=dis)
                    form.save()
            except ValueError as ve:
                print(ve)
            return redirect("/discussion/" + request.POST['discussion'])
    else:
        return redirect("main:Login") #Attenzione quando farai il login

def login_request(request):
    if(request.user.is_authenticated):
        return redirect("main:Home")
    else:
        if(request.method == "POST"):
            form = AuthenticationForm(request, data=request.POST)
            if(form.is_valid()):
                username = form.cleaned_data.get("username")
                password = form.cleaned_data.get("password")
                user = authenticate(username=username, password=password)
                if(user is not None):
                    login(request, user)
                    return redirect("main:Home")

        form = AuthenticationForm()
        return render(request, "main/login.html", {"form" : form})

def logout_request(request):
    logout(request)
    return redirect("main:Home")

def register(request):
    if(request.user.is_authenticated):
        return redirect("main:Home")
    else:
        if(request.method == "POST"):
            form = UserCreationForm(request.POST)
            if(form.is_valid()):
                user = form.save()
                login(request, user)
                return redirect("main:Home")
        form = UserCreationForm
        return render(request, "main/register.html", {"form" : form})

def profile(request):
    if(request.user.is_authenticated):
        dis = Discussion.objects.all().filter(author=request.user)
        return render(request, "main/profile.html", {"discussions" : dis})
    else:
        return redirect("main:Login")

def newdiscussion_request(request):
    if(request.user.is_authenticated):
        url = "main:Profile"
        if(request.method == "POST"):
            try:
                title = request.POST['title']
                description = request.POST['description']

                actual_dis = Discussion.objects.all().filter(title=title)

                if(title != "" and description != "" and actual_dis.count() == 0):
                    form = Discussion(author=request.user, title=title, description=description)
                    form.save()
                    url = "/discussion/" + title
            except ValueError as ex:
                print(ex)
            return redirect(url)
    else:
        return redirect("main:Login")

def deletedis_request(request, dis_t):
    if(request.user.is_authenticated):
        dis = Discussion.objects.all().filter(title=dis_t)
        dis.delete()

        return redirect("main:Profile")
    else:
        return redirect("main:Login")

def editdiscussion_request(request, old_title):
    if(request.user.is_authenticated):
        url = "main:Profile"
        if(request.method == "POST"):
            try:
                title = request.POST['title']
                description = request.POST['description']

                dis = Discussion.objects.get(title=old_title)
                if(title != "" and description != ""):
                    dis.title = title
                    dis.description = description
                    dis.save()
                    url = "/discussion/" + title
            except ValueError as ex:
                print(ex)
            return redirect(url)
    else:
        return redirect("main:Login")

def editprofile_request(request):
    if(request.user.is_authenticated):
        if(request.method == "POST"):
            try:
                request.user.username = request.POST['username']
                request.user.first_name = request.POST['first-name']
                request.user.last_name = request.POST['last-name']
                request.user.save()
                messages.success(request, "The account has been updated successfully!")
                return redirect("main:Profile")
            except ValueError as ex:
                print(ex)
    else:
        return redirect("main:Login")

def editcredentials_request(request):
    if(request.user.is_authenticated):
        if(request.method == "POST"):
            try:
                password = request.POST['password']
                if(password == request.POST['confirm-password']):
                    #Control password strenght
                    if(len(password) > 8 and password.isdigit() == False):
                        user = request.user
                        user.set_password(password)
                        user.save()
                    else:
                        messages.error(request, "Invalid password!")
            except ValueError as ex:
                print(ex)
        return redirect("main:Profile")
    else:
        return redirect("main:Login")

def rules_page(request):
    return render(request, "main/rules.html")
