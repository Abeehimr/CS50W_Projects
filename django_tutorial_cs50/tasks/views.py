from django.shortcuts import render
from django import forms
from django.http import HttpResponseRedirect
from django.urls import reverse
#tasks = ["foo","bar","baz"]

class NewTaskForm(forms.Form): # create forms for us
    task = forms.CharField(label="New Task")


# Create your views here.
def index(request):
    # exe in terminal python manage.py migrate to create django table that stores session
    if "tasks" not in request.session: #session: dict that have all data we have on file inside the session of user
        request.session["tasks"] = []
    return render(request,"tasks/index.html",{
        "tasks":request.session["tasks"],
    })

def add(request):
    if request.method == "POST": # if the user has submitted some form data
        form = NewTaskForm(request.POST) # save up all data they submitted
        if form.is_valid(): #server side validation
            task = form.cleaned_data["task"] #get the subimitted data
            request.session["tasks"] += [task]
            return HttpResponseRedirect(reverse("tasks:index"))
        else:
            return render(request,"tasks/add.html",{
                "form":form
            })
    return render(request,"tasks/add.html",{
        "form":NewTaskForm()
    })