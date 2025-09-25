from django.shortcuts import render, redirect
from django.db.models import Max, Min
from django.contrib import messages
from django.db import models

from core.localization import SUCSESS_MESSEGE, FAILD_MESSEGE
from .models import Airport, Route
from .forms import AirportForm, RouteForm, SearchNthNodeForm, ShortestRouteForm




def home(request):
    return render(request, 'home.html')





def add_airport(request):
    if request.method == 'POST':
        form = AirportForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, SUCSESS_MESSEGE.format("Airport"))
            return redirect('airport_list')
        else:
            messages.error(request, FAILD_MESSEGE.format("Airport"))
    else:
        form = AirportForm()
    return render(request, 'add_airport.html', {'form': form})




def add_route(request):
    if request.method == 'POST':
        form = RouteForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, SUCSESS_MESSEGE.format("Route"))
            return redirect('route_list')
        else:
            messages.error(request, FAILD_MESSEGE.format("Route"))
    else:
        form = RouteForm()
    return render(request, 'add_route.html', {'form': form})




def airport_list(request):
    airports = Airport.objects.all()
    return render(request, 'airport_list.html', {'airports': airports})




def route_list(request):
    routes = Route.objects.all().select_related('from_airport', 'to_airport')
    return render(request, 'route_list.html', {'routes': routes})



from django.shortcuts import render, redirect
from django.db.models import Max, Min
from django.contrib import messages
from django.db import models

from core.localization import SUCSESS_MESSEGE, FAILD_MESSEGE
from .models import Airport, Route
from .forms import AirportForm, RouteForm, SearchNthNodeForm, ShortestRouteForm


def home(request):
    return render(request, 'home.html')


def add_airport(request):
    if request.method == 'POST':
        form = AirportForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, SUCSESS_MESSEGE.format("Airport"))
            return redirect('airport_list')
        else:
            messages.error(request, FAILD_MESSEGE.format("Airport"))
    else:
        form = AirportForm()
    return render(request, 'add_airport.html', {'form': form})


def add_route(request):
    if request.method == 'POST':
        form = RouteForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, SUCSESS_MESSEGE.format("Route"))
            return redirect('route_list')
        else:
            messages.error(request, FAILD_MESSEGE.format("Route"))
    else:
        form = RouteForm()
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
        if form.is_valid():
            start_airport = form.cleaned_data['start_airport']
            n = form.cleaned_data['n']
            direction = form.cleaned_data['direction']
            
            try:
                current_airport = start_airport
                path = [current_airport]  
                for step in range(n):
                    next_route = Route.objects.filter(
                        from_airport=current_airport,
                        position=direction
                    ).select_related('to_airport').order_by('distance').first()
                    
                    if next_route:
                        current_airport = next_route.to_airport
                        path.append(current_airport)
                    else:
                        direction_display = 'Right' if direction == 'R' else 'Left'
                        result = {
                            'success': False,
                            'error': f'Cannot find {n}th {direction_display.lower()} node from {start_airport.code}. Path ends at step {step + 1}.',
                            'partial_path': path,
                            'steps_completed': step,
                            'direction_searched': direction_display
                        }
                        break
                else:
                    direction_display = 'Right' if direction == 'R' else 'Left'
                    if len(path) >= 2:
                        final_route = Route.objects.filter(
                            from_airport=path[-2],
                            to_airport=path[-1],
                            position=direction
                        ).select_related('from_airport', 'to_airport').first()
                    else:
                        final_route = None
                    
                    result = {
                        'success': True,
                        'nth_node': current_airport,
                        'n': n,
                        'direction_searched': direction_display,
                        'full_path': path,
                        'path_display': ' → '.join([airport.code for airport in path]),
                        'final_route': final_route,
                        'total_steps': n
                    }

            except Exception as e:
                result = {
                    'success': False,
                    'error': f'Error finding {n}th node: {str(e)}'
                }
    else:
        form = SearchNthNodeForm()
    
    return render(request, 'find_nth_node.html', {
        'form': form,
        'result': result
    })




def longest_route(request):
    # Find the route(s) with maximum distance
    max_distance = Route.objects.aggregate(Max('distance'))['distance__max']
    
    if max_distance is not None:
        longest_routes = Route.objects.filter(distance=max_distance).select_related('from_airport', 'to_airport')
    else:
        longest_routes = None
    
    return render(request, 'longest_route.html', {
        'longest_routes': longest_routes,
        'max_distance': max_distance
    })




def shortest_route(request):
    # Find the route(s) with minimum distance
    min_distance = Route.objects.aggregate(Min('distance'))['distance__min']
    
    if min_distance is not None:
        shortest_routes = Route.objects.filter(distance=min_distance).select_related('from_airport', 'to_airport')
    else:
        shortest_routes = None
    
    return render(request, 'shortest_route.html', {
        'shortest_routes': shortest_routes,
        'min_distance': min_distance
    })




def shortest_route_between_airports(request):
    result = None
    if request.method == 'POST':
        form = ShortestRouteForm(request.POST)
        if form.is_valid():
            from_airport = form.cleaned_data['from_airport']
            to_airport = form.cleaned_data['to_airport']
            
            # Find all routes between the two airports
            routes = Route.objects.filter(
                from_airport=from_airport,
                to_airport=to_airport
            ).select_related('from_airport', 'to_airport')
            
            if routes.exists():
                # Get the shortest route by distance
                shortest_route = routes.order_by('distance').first()
                result = {
                    'route': shortest_route,
                    'all_routes': routes,
                    'from_airport': from_airport,
                    'to_airport': to_airport
                }
            else:
                # Also check reverse direction
                reverse_routes = Route.objects.filter(
                    from_airport=to_airport,
                    to_airport=from_airport
                ).select_related('from_airport', 'to_airport')
                
                if reverse_routes.exists():
                    shortest_route = reverse_routes.order_by('distance').first()
                    result = {
                        'route': shortest_route,
                        'all_routes': reverse_routes,
                        'from_airport': to_airport,
                        'to_airport': from_airport,
                        'note': 'Route found in reverse direction'
                    }
                else:
                    result = {'error': f'No routes found between {from_airport.code} and {to_airport.code}'}
    else:
        form = ShortestRouteForm()
    
    return render(request, 'shortest_route_between.html', {
        'form': form,
        'result': result
    })