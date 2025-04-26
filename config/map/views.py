import requests
from django.views.generic import TemplateView
from django.http import HttpResponse
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from .models import Route
from django.http import JsonResponse
from django.shortcuts import get_object_or_404


def fetch_pois(lat, lng):
    ql = f"""
    [out:json][timeout:25];
    (
      node(around:2000,{lat},{lng})[amenity=cafe];
      way(around:2000,{lat},{lng})[amenity=cafe];
      node(around:2000,{lat},{lng})[tourism=attraction];
      way(around:2000,{lat},{lng})[tourism=attraction];
    );
    out center;
    """
    resp = requests.post(
        "https://overpass-api.de/api/interpreter",
        data={'data': ql},
        timeout=30
    )
    if resp.status_code != 200:
        return []

    data = resp.json()
    results = []

    for element in data.get('elements', []):
        tags = element.get('tags', {})
        results.append({
            'name': tags.get('name', 'Без названия'),
            'type': tags.get('amenity') or tags.get('tourism'),
            'lat': element.get('lat') or element.get('center', {}).get('lat'),
            'lng': element.get('lon') or element.get('center', {}).get('lon'),
        })

    return results


# # ищет POI по координатам
# class NearbyPOIAPIView(APIView):
#
#     def get(self, request):
#         try:
#             lat = float(request.query_params.get('lat'))
#             lng = float(request.query_params.get('lng'))
#         except (TypeError, ValueError):
#             return HttpResponse({'error': 'Неверные координаты'}, status=400)
#
#         pois = fetch_pois(lat, lng)
#         return HttpResponse({'results': pois})


class RouteListView(ListView):
    model = Route
    template_name = "routes/route_list.html"
    context_object_name = "routes"


class RouteCreateView(CreateView):
    def post(self, request):
        start_lat = request.POST.get("start_lat")
        start_lng = request.POST.get("start_lng")
        end_lat = request.POST.get("end_lat")
        end_lng = request.POST.get("end_lng")
        name = request.POST.get("name", "Без названия")

        if not all([start_lat, start_lng, end_lat, end_lng]):
            return JsonResponse({"error": "Не все данные переданы"}, status=400)

        route = Route.objects.create(
            user=request.user,
            start_lat=start_lat,
            start_lng=start_lng,
            end_lat=end_lat,
            end_lng=end_lng,
            name=name
        )

        return JsonResponse({
            "id": route.id,
            "name": route.name,
            "start_lat": route.start_lat,
            "start_lng": route.start_lng,
            "end_lat": route.end_lat,
            "end_lng": route.end_lng,
            "created_at": route.created_at
        }, status=201)


class RouteDetailView(DetailView):
    model = Route
    template_name = "routes/route_detail.html"
    context_object_name = "route"


class RouteUpdateView(UpdateView):
    def post(self, request, pk):
        route = get_object_or_404(Route, pk=pk)

        # Проверяем права пользователя
        if route.user != request.user:
            return JsonResponse({"error": "Нет прав на изменение этого маршрута"}, status=403)

        route.start_lat = request.POST.get("start_lat", route.start_lat)
        route.start_lng = request.POST.get("start_lng", route.start_lng)
        route.end_lat = request.POST.get("end_lat", route.end_lat)
        route.end_lng = request.POST.get("end_lng", route.end_lng)
        route.name = request.POST.get("name", route.name)
        route.save()

        return JsonResponse({
            "id": route.id,
            "name": route.name,
            "start_lat": route.start_lat,
            "start_lng": route.start_lng,
            "end_lat": route.end_lat,
            "end_lng": route.end_lng,
            "created_at": route.created_at
        })


class RouteDeleteView(DeleteView):
    def post(self, request, pk):
        route = get_object_or_404(Route, pk=pk)

        # Проверяем права пользователя
        if route.user != request.user:
            return JsonResponse({"error": "Нет прав на удаление этого маршрута"}, status=403)

        route.delete()
        return JsonResponse({"result": "Маршрут удален"})


class KaliningradRouteView(TemplateView):
    template_name = "kaliningrad_routes.html"
