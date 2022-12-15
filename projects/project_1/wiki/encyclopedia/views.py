from django.shortcuts import render
from django.http import HttpResponse
from . import util
from django import forms
from django.http import HttpResponseRedirect
import markdown2

class SearchForm(forms.Form):
    key_word = forms.CharField(label="Search Encyclopedia")

class AddForm(forms.Form):
    title = forms.CharField()
    page_content = forms.CharField(widget=forms.Textarea)
    
class EditForm(forms.Form):
    new_content = forms.CharField()
        

def index(request):
    if request.method == "POST":
        form = SearchForm(request.POST)
        if form.is_valid():
            key_word = form.cleaned_data["key_word"]
            
            if util.get_entry(key_word) != None:
                return render(request, "encyclopedia/entry.html", {
                    "entry_page": util.get_entry(key_word)
                })
                
            else:
                entries = util.list_entries()
                results = []
                for entry in entries:
                    if key_word.lower() in entry.lower():
                        results.append(entry)
                return render(request, "encyclopedia/search.html", {
                    "results": results,
                    "seach_form" : SearchForm()
                })
            
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "search_form" : SearchForm()
    })
    
def entry(request, title):
    if util.get_entry(title) == None:
        return render(request, "encyclopedia/error.html", {
            "message": "Page Not Found"
        })
    else:
        return render(request, "encyclopedia/entry.html", {
            "entry_page": util.get_entry(title),
            "entry": title
        })

def add(request):
    if request.method == "POST":
        form = AddForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            entries = util.list_entries()
            if title in entries:
                return render(request, "encyclopedia/error.html", {
                    "message": "Page already existed"
                })
            else:
                page_content = form.cleaned_data["page_content"]
                util.save_entry(title, page_content)
                return render(request, "encyclopedia/index.html", {
                    "entries": util.list_entries(),
                    "search_form" : SearchForm()
                })
                
        
    return render(request, "encyclopedia/add.html", {
        "add_form": AddForm()
    })

def edit(request, entry):
    if request.method == "POST":
        form = EditForm(request.POST)
        if form.is_valid():
            new_content = form.cleaned_data.get("new_content")
            util.save_entry(entry, new_content)
            return render(request, "encyclopedia/index.html", {
                    "entries": util.list_entries(),
                    "search_form" : SearchForm()
                })
    

    
    return render(request, "encyclopedia/edit.html", {
        "original_content": util.get_entry(entry),
        "entry": entry
    })