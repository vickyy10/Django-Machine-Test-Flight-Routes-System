from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Max, Min

from core.localization import FAILD_MESSEGE, SUCSESS_MESSEGE
from .models import Airport, Route
from .forms import AirportForm, RouteForm, SearchNthNodeForm


# ------------------------- HOME -------------------------
def home(request):
    """
    Render the home page of the application.
    """
    return render(request, 'home.html')



# ------------------------- ADD AIRPORT -------------------------
def add_airport(request):
    """
    Handle creation of a new Airport.
    - If POST request: validate and save the airport form.
    - On success: show success message and redirect to airport list.
    - On failure: show error message and re-render the form with errors.
    - If GET request: render an empty form.
    """
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



# ------------------------- ADD ROUTE -------------------------
def add_route(request):
    """
    Handle creation of a new Route.
    - If POST request: validate and save the route form.
    - On success: show success message and redirect to route list.
    - On failure: show error message and re-render the form with errors.
    - If GET request: render an empty form.
    """
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



# ------------------------- AIRPORT LIST -------------------------
def airport_list(request):
    """
    Display a list of all Airports stored in the database.
    """
    airports = Airport.objects.all()
    return render(request, 'airport_list.html', {'airports': airports})



# ------------------------- ROUTE LIST -------------------------
def route_list(request):
    """
    Display a list of all Routes with related 'from_airport' and 'to_airport'.
    Uses select_related for query optimization.
    """
    routes = Route.objects.all().select_related('from_airport', 'to_airport')
    return render(request, 'route_list.html', {'routes': routes})



# ------------------------- FIND NTH NODE -------------------------
def find_nth_node(request):
    """
    Find the Nth Left or Right node from a starting airport.
    - Accepts a form with: start_airport, n (steps), and direction (L/R).
    - Iteratively traverses routes to find the destination after 'n' steps.
    - Handles cases where the path ends before reaching the Nth node.
    - Returns full/partial path information and result status.
    """
    result = None
    if request.method == 'POST':
        form = SearchNthNodeForm(request.POST)
        if form.is_valid():
            start_airport = form.cleaned_data['start_airport']
            n = form.cleaned_data['n']
            direction = form.cleaned_data['direction']
            
            try:
                current_airport = start_airport
                path = [current_airport]  # Keep track of the traversal path

                # Traverse step by step up to 'n' times
                for step in range(n):
                    next_route = Route.objects.filter(
                        from_airport=current_airport,
                        position=direction
                    ).select_related('to_airport').order_by('distance').first()
                    
                    if next_route:
                        # Move to next airport in the path
                        current_airport = next_route.to_airport
                        path.append(current_airport)
                    else:
                        # If no route is found, stop traversal and return partial path
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
                    # If traversal completes successfully
                    direction_display = 'Right' if direction == 'R' else 'Left'
                    
                    # Find the final route for display (from last two airports in path)
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
                # Handle unexpected errors gracefully
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



# ------------------------- LONGEST ROUTE -------------------------
def longest_route(request):
    """
    Find and display the route(s) with the maximum distance.
    - Uses aggregation to find max distance.
    - Retrieves all routes matching that distance.
    """
    max_distance = Route.objects.aggregate(Max('distance'))['distance__max']
    
    if max_distance is not None:
        longest_routes = Route.objects.filter(distance=max_distance).select_related('from_airport', 'to_airport')
    else:
        longest_routes = None
    
    return render(request, 'longest_route.html', {
        'longest_routes': longest_routes,
        'max_distance': max_distance
    })



# ------------------------- SHORTEST ROUTE -------------------------
def shortest_route(request):
    """
    Find and display the route(s) with the minimum distance.
    - Uses aggregation to find min distance.
    - Retrieves all routes matching that distance.
    """
    min_distance = Route.objects.aggregate(Min('distance'))['distance__min']
    
    if min_distance is not None:
        shortest_routes = Route.objects.filter(distance=min_distance).select_related('from_airport', 'to_airport')
    else:
        shortest_routes = None
    
    return render(request, 'shortest_route.html', {
        'shortest_routes': shortest_routes,
        'min_distance': min_distance
    })
