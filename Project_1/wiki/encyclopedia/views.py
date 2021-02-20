from django.shortcuts import render, HttpResponseRedirect, reverse
from django import forms

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
                # TODO: change this to an error message
                # Did confirm the code/redirect works, though
                return HttpResponseRedirect(reverse('index'))

            # Save new entry
            util.save_entry(title, content)

            # Redirect
            return HttpResponseRedirect(title)
        
        # Re-prompt user if form is invalid
        else:
            return render(request, "encyclopedia/new_page.html",{
                "form": form
            })
    
    # Render blank page if request method isn't POST
    return render(request, "encyclopedia/new_page.html",{
        "form": NewPageForm()
    })