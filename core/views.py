from django.shortcuts import render, redirect
from django.db.models import Max, Min
from django.contrib import messages

from core.localization import SUCSESS_MESSEGE,FAILD_MESSEGE
from .models import Airport, Route
from .forms import AirportForm, RouteForm, AirportRouteForm, SearchNthNodeForm, ShortestRouteForm



def home(request):
    return render(request, 'home.html')



def add_airport(request):
    if request.method == 'POST':
        form = AirportForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,SUCSESS_MESSEGE.format("Airport"))
            return redirect('airport_list')
    else:
        form = AirportForm()
        messages.error(request,FAILD_MESSEGE.format("Airport"))
    return render(request, 'add_airport.html', {'form': form})



def add_route(request):
    if request.method == 'POST':
        form = RouteForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,SUCSESS_MESSEGE.format("Route"))
            return redirect('route_list')
    else:
        form = RouteForm()
        messages.error(request,FAILD_MESSEGE.format("Route"))
    return render(request, 'add_route.html', {'form': form})



def airport_list(request):
    airports = Airport.objects.all()
    return render(request, 'airport_list.html', {'airports': airports})



def route_list(request):
    routes = Route.objects.all().select_related('from_airport', 'to_airport')
    return render(request, 'route_list.html', {'routes': routes})




def find_nth_node(request):
    result = None
    if request.method == 'POST':
        form = SearchNthNodeForm(request.POST)
        print(request.POST,'request.POST')
        if form.is_valid():
            start_airport = form.cleaned_data['start_airport']
            n = form.cleaned_data['n']
            direction = form.cleaned_data['direction']
            print(direction,"direction")
            print(start_airport,"start_airport")
            print(n,"n")
            routes = None
            try:
                routes = Route.objects.get(
                    from_airport=start_airport,
                    direction='R',
                    position=n

                )
                

                result = {
                    'route': routes,
                    'from_airport': routes.from_airport,
                    'to_airport': routes.to_airport,
                    'position': routes.position,  
                    'direction': 'Right' if direction == 'R' else 'Left',
                    'duration': routes.duration  
                }

            except Exception as e:
                result = {'error': str(e)}
    else:
        form = SearchNthNodeForm()
    
    return render(request, 'find_nth_node.html', {
        'form': form,
        'result': result
    })



def longest_route(request):
    max_duration = Route.objects.aggregate(Max('duration'))['duration__max']
    if max_duration is not None:
        longest_routes = Route.objects.filter(duration=max_duration).select_related('from_airport', 'to_airport')
    else:
        longest_routes = None
    
    return render(request, 'longest_route.html', {
        'longest_routes': longest_routes,
        'max_duration': max_duration
    })



def shortest_route(request):
    min_duration = Route.objects.aggregate(Min('duration'))['duration__min']
    if min_duration is not None:
        shortest_routes = Route.objects.filter(duration=min_duration).select_related('from_airport', 'to_airport')
    else:
        shortest_routes = None
    
    return render(request, 'shortest_route.html', {
        'shortest_routes': shortest_routes,
        'min_duration': min_duration
    })




def shortest_route_between_airports(request):
    result = None
    if request.method == 'POST':
        form = ShortestRouteForm(request.POST)
        if form.is_valid():
            from_airport = form.cleaned_data['from_airport']
            to_airport = form.cleaned_data['to_airport']
            
            routes = Route.objects.filter(
                from_airport=from_airport,
                to_airport=to_airport
            ).select_related('from_airport', 'to_airport')
            
            if routes.exists():
                shortest_route = routes.order_by('duration').first()
                result = {
                    'route': shortest_route,
                    'all_routes': routes
                }
            else:
                result = {'error': f'No routes found between {from_airport.code} and {to_airport.code}'}
    else:
        form = ShortestRouteForm()
    
    return render(request, 'shortest_route.html', {
        'form': form,
        'result': result
    })