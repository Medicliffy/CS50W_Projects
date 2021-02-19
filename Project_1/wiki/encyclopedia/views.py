from django.shortcuts import render

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry_page(request, entry_name):
    
    return render(request, "encyclopedia/entry.html", {
        "name": entry_name,
        # TODO: fix using .capitalize() (doesn't work for CSS, etc.)
        "content": util.get_entry(entry_name.capitalize())
    })