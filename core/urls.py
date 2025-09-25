from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    
    # Airport management
    path('airports/', views.airport_list, name='airport_list'),
    path('airports/add/', views.add_airport, name='add_airport'),
    
    # Route management
    path('routes/', views.route_list, name='route_list'),
    path('routes/add/', views.add_route, name='add_route'),
    
    # Question 1: Find Nth Node
    path('find-nth-node/', views.find_nth_node, name='find_nth_node'),
    
    # Question 2: Longest Route
    path('longest-route/', views.longest_route, name='longest_route'),
    
    # Question 3: Shortest Route Between Airports
    path('shortest-route/', views.shortest_route, name='shortest_route'),
]