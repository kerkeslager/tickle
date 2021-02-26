from django.urls import path

from . import views

# TODO Move attempts and todos to sub-area under user URLs
# TODO Use something other than primary keys in URLs

app_name = 'tickle'

urlpatterns = (
    path('area', views.area_list, name='area-list'),
    path('area/<int:pk>', views.area_detail, name='area-detail'),
    path('attempt', views.attempt_list, name='attempt-list'),
    path('boulder', views.boulder_list, name='boulder-list'),
    path('boulder/<int:pk>', views.boulder_detail, name='boulder-detail'),
    path('route', views.route_list, name='route-list'),
    path('route/<int:pk>', views.route_detail, name='route-detail'),
    path('todo', views.todo_list, name='todo-list'),
)
