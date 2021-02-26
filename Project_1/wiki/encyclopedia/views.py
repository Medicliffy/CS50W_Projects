from django.shortcuts import render, HttpResponseRedirect, reverse
from django import forms

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def entry_page(request, entry_name):
    
    content = util.get_entry(entry_name)

    if not content:
        return render(request, "encyclopedia/error.html", {
            "message": f'Unforunately no entry was found for "{entry_name}"',
            "title": "Page does not exist",
            "name": entry_name,
            "allow_create": True,
        })

    content = util.md_to_html(content)

    return render(request, "encyclopedia/entry.html", {
        "name": entry_name,
        "content": content
    })


class NewPageForm(forms.Form):
    title = forms.CharField(label="Title")
    content = forms.CharField(label="Content", widget=forms.Textarea)


def new_page(request):

    if request.method=='POST':
        
        # Get data user put into new page
        form = NewPageForm(request.POST)
        
        # Ensure form is valid
        if form.is_valid():
            
            title = form.cleaned_data['title']
            content = form.cleaned_data['content']

            # Ensure entry doesn't exist already
            if title in util.list_entries():
                
                return render(request, "encyclopedia/error.html", {
                    "message": f'An entry already exists for "{title}"',
                    "title": "Page already exists",
                    "name": title,
                    "allow_create": False,
                    "already_exists": True,
                })

            # Save new entry
            util.save_entry(title, content)

            # Redirect (both of these work, leaving both for my reference)
            # return HttpResponseRedirect(reverse("entry", kwargs={'entry_name': title}))
            return HttpResponseRedirect(reverse("entry", args=[title]))
        
        # Re-prompt user if form is invalid
        else:
            return render(request, "encyclopedia/new_page.html",{
                "form": form
            })
    
    return render(request, "encyclopedia/new_page.html", {
        "form": NewPageForm(initial=request.GET)
    })


def search(request):

    params = request.GET

    # Redirect to index if no get parameters are specified
    if params == {}:
        return HttpResponseRedirect(reverse("index"))
    
    term = params.get('q')
    entries = util.list_entries()
    lower_entries = list(map(str.lower, entries))

    if term in entries:
        return HttpResponseRedirect(reverse("entry", args=[term]))
    elif term.lower() in lower_entries:
        # Also redirect cases that don't match capitalization
        term = entries[lower_entries.index(term.lower())]
        return HttpResponseRedirect(reverse("entry", args=[term]))
    else:
        # Return list of entries with search as a subterm. Ignore capitalization.

        matching_entries = [x for x in entries if term.lower() in x.lower()]

        if matching_entries == []:
            # Render error page if no matching entries are found
            return render(request, "encyclopedia/error.html", {
                "message": f'No matching entries were found for your search "{term}"',
                "title": "No entries found",
                "name": term,
                "allow_create": False,
            })
        else:
            # Render page listing potential matches
            return render(request, "encyclopedia/search.html",{
                "results": matching_entries,
                "search_term": term,
            })

def edit_entry(request, entry_name):

    # It would be more efficient to write a funciton and share w/ new page logic
    # But, this will get me processing through form management more ¯\_(ツ)_/¯

    if request.method=='POST':
        
        # Get data that user submitted
        form = NewPageForm(request.POST)

        # Check if form is valid
        if form.is_valid():
            
            title = form.cleaned_data['title']
            content = form.cleaned_data['content']

            # Don't allow editing or creating other pages
            if not title == entry_name:
                
                if title in util.list_entries():
                    allow_create = False
                    already_exists = True
                    text = "edit"
                else:
                    allow_create = True
                    already_exists = False
                    text = "create"
                
                return render(request, "encyclopedia/error.html",{
                    "message": f'Unable to {text} "{title}" from the page for "{entry_name}"',
                    "title": "Wrong page!",
                    "name": title,
                    "allow_create": allow_create,
                    "already_exists": already_exists,
                })

            # Save modified entry
            util.save_entry(title, content)

            # Redirect to edited page
            return HttpResponseRedirect(reverse("entry", args=[title]))
        else:
            # Reprompt if input is invalid
            return render(request, "encyclopedia/edit_page.html", {
                "form": form,
                "title": entry_name
            })
        
    # Get existing page data & initialize form
    current_entry = {'title': entry_name, 'content': util.get_entry(entry_name)}
    form = NewPageForm(initial=current_entry)

    return render(request, "encyclopedia/edit_page.html", {
        "form": form,
        "title": entry_name
    })