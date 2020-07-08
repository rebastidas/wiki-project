from django.shortcuts import render
from django.http import HttpResponseRedirect
from django import forms
from django.urls import reverse
from . import util
from django.core.files.storage import default_storage
import secrets
import markdown2


class SearchForm(forms.Form):

    search = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    
class createNewEntry(forms.Form):

    title = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    content = forms.CharField(widget=forms.Textarea(attrs={'rows':10, 'class':'form-control'}))

def index(request):

    return render(request, "encyclopedia/index.html", {
    "entries": util.list_entries(), "form":SearchForm()
    })

def title(request, title):

    titulo = util.get_entry(title)

    if (titulo is None):
        titulo="No such Entry"

    content = markdown2.markdown(titulo)

    return render(request, "encyclopedia/content.html", {"titulo": content, "form":SearchForm(), "title":title})

def matchs(request):

    if request.method == "POST":
        form = SearchForm(request.POST)
        if form.is_valid():
            
            search = form.cleaned_data["search"]
            titulo= util.get_entry(search)

            if (titulo is None):
                titulo = util.list_entries()
                results = []

                for titles in titulo:
                    result = util.get_entry(titles)

                    if search.lower() in result.lower():
                        results +=[titles]

                return render(request, "encyclopedia/matchs.html", {"results": results, "form":SearchForm(), "search":search})
            else:
                content = markdown2.markdown(titulo)
                return render(request, "encyclopedia/content.html", {"titulo": content, "form":SearchForm()})

def newentry(request):

    return render(request, "encyclopedia/newentry.html",{"form":SearchForm(),"nentry":createNewEntry()})

def newcreation(request):

    if request.method == "POST":
        form = createNewEntry(request.POST)
        if form.is_valid():

            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            titulo = util.get_entry(title)

            if (titulo is None):
                util.save_entry(title, content)
                contentido = util.get_entry(title)
                titulo= markdown2.markdown(contentido)
                return render(request, "encyclopedia/content.html", {"titulo": titulo, "title":title, "form":SearchForm()})
            else:
                error= "File already exist"
                return render(request, 'encyclopedia/newentry.html', {"error":error, "nentry":createNewEntry()})

def editentry(request, title):

    titulo = util.get_entry(title)

    return render(request, "encyclopedia/edit.html",{"titulo":titulo, "title":title, "form":SearchForm()})

def edition(request):

    title = request.POST.get("new_title")
    content = request.POST.get("new_content")

    util.save_entry(title, content)

    titulo= markdown2.markdown(content)

    return render(request, "encyclopedia/content.html", {"titulo": titulo, "title":title, "form":SearchForm()})

def random(request):

    url_list = util.list_entries()
    title = secrets.choice(url_list)
    contentido = util.get_entry(title)
    content = markdown2.markdown(contentido)

    return render(request, "encyclopedia/content.html", {"titulo": content, "form":SearchForm(), "title":title})