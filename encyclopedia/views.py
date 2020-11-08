
from django.shortcuts import redirect

from django.http import HttpResponse

from django.shortcuts import render

from django import forms

from . import util

import random

entries = util.list_entries()
current_title=None

class SearchForm(forms.Form):
	search = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Search Encyclopedia'}))


class NewPageForm(forms.Form):
	title = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter Title'}))
	new_page_content = forms.CharField(widget=forms.Textarea(attrs={'rows':80, 'cols':20,'placeholder':'write content here'}),label="")

class EditPageForm(forms.Form):
	edit_page_content = forms.CharField(widget=forms.Textarea(attrs={'rows':80, 'cols':20}),label="")

	
def index(request):
	if request.method == 'GET':
		return search(request)
	else:
	    return render(request, "encyclopedia/index.html", {
	        "entries": entries,
	        "form": SearchForm(),
	        "search": 0
    })

def page(request,title):

	if title in entries:
		global current_title
		current_title = title
		return render(request,"encyclopedia/page.html",{
			"title": title,
			"html":util.markdown_to_html(title),
        	"form": SearchForm()
        	})
	else:
		return HttpResponse(f"The requsted page : {title} is not a valid wiki page")

def search(request):

	#form = SearchForm(request.GET)
	form = SearchForm(request.GET or None)

	if form.is_valid():
		title = form.cleaned_data["search"]
		if(title in entries):

			return page(request,title)
		else:
			query_sub_string = []
			for t in entries:
				if title in t:
					query_sub_string.append(t)

			return render(request,"encyclopedia/index.html",{
			"entries": entries,
	        "form": form,
	        "query_sub_string": query_sub_string,
	        "search": 1
			})
	else:
		return render(request,"encyclopedia/index.html",{
			"entries": entries,
	        "form": form,
	        "search": 0
			})

def random_page(request):
	n = random.randint(0,len(entries)-1)
	random_entry = entries[n]

	return redirect('wiki/'+random_entry)


def new_page(request):
	if request.method == 'POST':
		form = NewPageForm(request.POST)
		if form.is_valid():
			page_title = form.cleaned_data['title']
			page_content = form.cleaned_data['new_page_content']

			if page_title not in entries:
				util.save_entry(page_title,page_content)
				entries.append(page_title)
				return page(request,page_title)
			else:
				return HttpResponse("Sorry this title exists.")
		else:
			return render(request,"encyclopedia/new_page.html",{
				"form": SearchForm(),
				"search_form": form
				})
	else:
		return render(request,"encyclopedia/new_page.html",{
				"form": SearchForm(),
				"search_form": NewPageForm()
				})

def edit_page(request):
	if request.method == 'POST':
		form = EditPageForm(request.POST)
		if form.is_valid():
			edit_content = form.cleaned_data['edit_page_content']

			util.save_entry(current_title,edit_content)
			return page(request,current_title)

		else:
			return render(request,"encyclopedia/edit_page.html",{
				"form": SearchForm(),
				"edit_form": form,
				})
	else:
		initial = {'edit_page_content': util.get_entry(current_title)}
		return render(request,"encyclopedia/edit_page.html",{
				"form": SearchForm(),
				"edit_form": EditPageForm(initial=initial),
				"title": current_title
				})