from django.shortcuts import render
from django.http import HttpResponse

from . import util


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
