from django.shortcuts import get_object_or_404, render

# Create your views here.
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from .models import Listing
from .choices import price_choices, bedroom_choices, state_choices

def index(request):
  listings = Listing.objects.order_by('-list_date').filter(is_published=True)

  paginator = Paginator(listings, 6)
  page = request.GET.get('page')
  paged_listings = paginator.get_page(page)

  context = {
    'listings': paged_listings
  }

  return render(request, 'listings/listings.html', context)

def listing(request, listing_id):
  listing = get_object_or_404(Listing, pk=listing_id)

  context = {
    'listing': listing
  }

  return render(request, 'listings/listing.html', context)

def search(request):
  queryset_list = Listing.objects.order_by('-list_date')

  # Keywords
  if 'keywords' in request.GET:
    keywords = request.GET['keywords']
    if keywords:
      queryset_list = queryset_list.filter(description__icontains=keywords)

  # City
  if 'city' in request.GET:
    city = request.GET['city']
    if city:
      queryset_list = queryset_list.filter(city__iexact=city)

  # State
  if 'state' in request.GET:
    state = request.GET['state']
    if state:
      if state == 'INT':    
          # Include all regions except the 7 specified above
          excluded_states = ["Jerusalem", "North", "Haifa", "Central", "Tel-Aviv Area", "South", "Judea and Samaria"]
          queryset_list = queryset_list.exclude(state__in=excluded_states)
      else:
          # Filter by the selected state
          queryset_list = queryset_list.filter(state__iexact=state)

  # Bedrooms
  if 'bedrooms' in request.GET:
    bedrooms = request.GET['bedrooms']
    if bedrooms:
      queryset_list = queryset_list.filter(bedrooms__lte=bedrooms)

  # Price
  if 'price' in request.GET:
      price = request.GET['price']
      if price:
          if price == '1000000':
              # Price up to $1M
              queryset_list = queryset_list.filter(price__lte=1000000)
          elif price == '1000001':
              # Price bigger than $1M
              queryset_list = queryset_list.filter(price__gt=1000000)
          else:
              # Filter by the selected price range
              queryset_list = queryset_list.filter(price__lte=int(price))

  context = {
    'state_choices': state_choices,
    'bedroom_choices': bedroom_choices,
    'price_choices': price_choices,
    'listings': queryset_list,
    'values': request.GET
  }

  return render(request, 'listings/search.html', context)