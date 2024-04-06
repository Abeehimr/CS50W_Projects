from django.shortcuts import render
from django.http import Http404 , HttpResponseRedirect
from django.urls import reverse
from django import forms
from . import util
import markdown2
import random

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "title":"Encyclopedia",
        "heading":"All Pages",
    })

class NewTaskForm(forms.Form): # create forms for us
    title = forms.CharField(label="Title")
    md = forms.CharField(widget=forms.Textarea(attrs={
                "placeholder": "write content in Markdown Syntax here",
            }),label="",initial="")

class EditingForm(forms.Form):
    def __init__(self, *args, **kwargs):
        prev = kwargs.pop("prev","")
        super(EditingForm, self).__init__(*args, **kwargs)
        self.fields['md'].initial = prev

    md = forms.CharField(widget=forms.Textarea(attrs={
                "placeholder": "write content in Markdown Syntax here",
            }),label="")

def edit(request,title:str):
    if request.method == "POST":
        form = EditingForm(request.POST)
        if form.is_valid():
            md = form.cleaned_data["md"]
            util.save_entry(title, md)
            return HttpResponseRedirect(reverse("entry",args=[title]))
    else:
        form = EditingForm(prev=util.get_entry(title))
    return render(request,"encyclopedia/edit.html",{
        "form":form,
        "title":title,
    })

def newpage(request):
    heading = "An Entry with this name already exist"
    if request.method == "POST":
        form = NewTaskForm(request.POST)
        if form.is_valid() and form.cleaned_data["title"].lower() not in [x.lower() for x in util.list_entries()]:
            title , md = form.cleaned_data["title"],form.cleaned_data["md"]
            util.save_entry(title, md)
            return HttpResponseRedirect(reverse("entry",args=[title]))
    else:
        form = NewTaskForm()
        heading = "ADD Content for the new Entry"
    return render(request,"encyclopedia/newpage.html",{
        "form":form,
        "heading":heading,
    })

def entry(request,title:str):
    if title == "None":
        title = random.choice(util.list_entries())
        return HttpResponseRedirect(reverse("entry",args=[title]))
    md  = util.get_entry(title)
    if md:
        body = markdown2.markdown(md)
    else:
        raise Http404("your requested page was not found")
    return render(request, "encyclopedia/entry.html",{
        "title":title,
        "markdown":body,
    })

def results(request):
    if request.method == "POST":
        search = request.POST["q"]
    else:
        search = ""
    lower_search = search.lower()
    names = util.list_entries()
    for name in names:
        if lower_search == name.lower():
            return HttpResponseRedirect(reverse("entry",args=[name]))
    #else:
    search_result = filter(lambda x: lower_search in x.lower(),names)
    return render(request, "encyclopedia/index.html", {
        "entries": search_result,
        "title":"Search Result",
        "heading":f"All matches with \"{search}\"",
    })