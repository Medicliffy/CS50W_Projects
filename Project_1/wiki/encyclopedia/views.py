from django.shortcuts import render

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry_page(request, entry_name):
    
    content = util.get_entry(entry_name)
    content = util.md_to_html(content)

    return render(request, "encyclopedia/entry.html", {
        "name": entry_name,
        "content": content
    })