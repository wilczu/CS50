from django.shortcuts import render, redirect
from django.http import HttpResponse
from django import forms

from . import util

class CreateForm(forms.Form):
    title = forms.CharField(label="Title of your wiki page")
    content = forms.CharField(label="Content of the page",
        widget=forms.Textarea(attrs={'style' : 'height: 500px;'}))

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def wiki(request, query):
    result = util.get_entry(query)

    if result != None:
        return render(request, "encyclopedia/displayQuery.html", {
            "query_title": query,
            "query_result": result
        })
    else:
        return render(request, "encyclopedia/error.html", {
            "error_message": (f"Query {query} was not found!")
        })

def create_page(request):
    if request.method == "POST":
        form = CreateForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            exists = util.get_entry(title)

            if exists == None:
                util.save_entry(title, content)
                return redirect(f"wiki/{title}")
            else:
                return render(request, "encyclopedia/create.html", {
                    "create_form": form,
                    "error": f"Page with the title of {title} already exists!"
                })

    return render(request, "encyclopedia/create.html", {
        "create_form": CreateForm()
    })
