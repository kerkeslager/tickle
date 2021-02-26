from django.views.generic import DetailView, ListView

from . import models

class AreaDetailView(DetailView):
    model = models.Area
area_detail = AreaDetailView.as_view()

class AreaListView(ListView):
    queryset = models.Area.objects.filter(parent=None)
area_list = AreaListView.as_view()

class AttemptListView(ListView):
    pass
attempt_list = AttemptListView.as_view()

class BoulderDetailView(DetailView):
    pass
boulder_detail = BoulderDetailView.as_view()

class BoulderListView(ListView):
    pass
boulder_list = BoulderListView.as_view()

class RouteDetailView(DetailView):
    pass
route_detail = RouteDetailView.as_view()

class RouteListView(ListView):
    pass
route_list = RouteListView.as_view()

class TodoListView(ListView):
    pass
todo_list = TodoListView.as_view()
