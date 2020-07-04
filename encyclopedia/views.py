from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render, reverse
from markdown2 import Markdown
from random import choice

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def page(request, title=""):
    if title == "":
        title = request.GET.get("title")

    content = util.get_entry(title) 
    # if no exact search match
    if content == None:
        # do search
        list = util.list_entries()
        results = []
        for item in list:
            upper_item = item.upper()
            if title.upper() in upper_item:
                results.append(item)
        # return search results
        return render(request, "encyclopedia/search_results.html", 
        {
            "word": title,
            "results": results
        })
    # if exact search match, or followed link
    else:   
        markdowner = Markdown()
        content = markdowner.convert(content)
        return render(request, "encyclopedia/info.html", {
            "title": title,
            "content": content
        })
    
def new(request):
    if request.method == "GET":
        return render(request, "encyclopedia/new_page.html")
    else:
        title = request.POST["title"]
        if title in util.list_entries():
            return HttpResponse("This page already exists")
        else:
            content = request.POST["content"]
            util.save_entry(title, content)
            return redirect(page, title)

def edit(request, title):
    if request.method == "GET":
        content = util.get_entry(title)
        return render(request, "encyclopedia/edit.html", {
            "title": title,
            "content": content
        })
    else:
        content = request.POST["content"]
        util.save_entry(title, content)
        return redirect(page, title)

def random(request):
    list = util.list_entries()
    title = choice(list)
    return redirect(page, title)

def delete(request, title):
    util.delete_entry(title)
    return redirect(index)
