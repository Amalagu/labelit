#project search is the logic for the search feature on the project (index) page.
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def projectsearch(request, profile ):
	#TO GET SEARCH KEY FROM THE FRONTEND
	search_key = ''
	if request.GET.get("search_key"):
	   search_key = request.GET.get("search_key")
	   
	#GETTING THE QUERYSETS THAT MATCHES THE SEARCH KEY
	projects = profile.project_set.distinct().filter(Q(title__icontains=search_key) | Q(description__icontains =search_key) | Q(annotators__username__icontains=search_key))
	annotationprojects = profile.annotationprojects.distinct().filter(Q(title__icontains=search_key) | Q(description__icontains =search_key) | Q(annotators__username__icontains=search_key) )
	
	return projects, annotationprojects, search_key
	
	
#pagerfunction describes the logic for paginating a view
def pagerfunction(request, queryset, num_per_page ):
	#DIVIDES THE QUERYSET INTO PAGES OF num_per_page (e.g 5 per page)
	pages = Paginator(queryset, num_per_page)
	#GET THE REQUESTED PAGE FROM THE FRONTEND
	page = request.GET.get("page")
	try:
		pagedqueryset = pages.page(page)
	except PageNotAnInteger:
		page=1
		pagedqueryset = pages.page(page)	#Default Pagenumber
	except EmptyPage:
        	pagedqueryset = pages.page(pages.num_pages)	#Resolving Non-existent pages

	return pagedqueryset, pages, page