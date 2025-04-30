import requests
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from .models import Route
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json


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

    def get_queryset(self):
        return Route.objects.filter(user=self.request.user)

# class RouteCreateView(CreateView):
#     def post(self, request):
#         start_lat = request.POST.get("start_lat")
#         start_lng = request.POST.get("start_lng")
#         end_lat = request.POST.get("end_lat")
#         end_lng = request.POST.get("end_lng")
#         name = request.POST.get("name", "Без названия")
#
#         if not all([start_lat, start_lng, end_lat, end_lng]):
#             return JsonResponse({"error": "Не все данные переданы"}, status=400)
#
#         route = Route.objects.create(
#             user=request.user,
#             start_lat=start_lat,
#             start_lng=start_lng,
#             end_lat=end_lat,
#             end_lng=end_lng,
#             name=name
#         )
#
#         return JsonResponse({
#             "id": route.id,
#             "name": route.name,
#             "start_lat": route.start_lat,
#             "start_lng": route.start_lng,
#             "end_lat": route.end_lat,
#             "end_lng": route.end_lng,
#             "created_at": route.created_at
#         }, status=201)


class RouteDetailView(DetailView):
    model = Route
    template_name = "routes/route_detail.html"
    context_object_name = "route"


class RouteUpdateView(UpdateView):
    def post(self, request, pk):
        route = get_object_or_404(Route, pk=pk)
        if route.user != request.user:
            return JsonResponse({"error": "Нет прав на изменение"}, status=403)

        data = json.loads(request.body)
        for field in ['start_lat', 'start_lng', 'end_lat', 'end_lng', 'name']:
            if field in data:
                setattr(route, field, data[field])
        route.save()
        return JsonResponse(route.to_dict())


class RouteDeleteView(DeleteView):
    def post(self, request, pk):
        route = get_object_or_404(Route, pk=pk)
        if route.user != request.user:
            return JsonResponse({"error": "Нет прав на удаление"}, status=403)
        route.delete()
        return JsonResponse({"status": "success"})


class KaliningradRouteView(TemplateView):
    template_name = "kaliningrad_routes.html"


@method_decorator(csrf_exempt, name='dispatch')
class RouteSaveView(CreateView):
    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({'error': 'Требуется авторизация'}, status=401)

        try:
            data = json.loads(request.body)
            route = Route.objects.create(
                user=request.user,
                start_lat=data['start_lat'],
                start_lng=data['start_lng'],
                end_lat=data['end_lat'],
                end_lng=data['end_lng'],
                name=data.get('name', 'Без названия')
            )
            return JsonResponse(route.to_dict(), status=201)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)


# Новые методы API
@login_required
def user_routes(request):
    routes = Route.objects.filter(user=request.user).values(
        'id', 'name', 'start_lat', 'start_lng', 'end_lat', 'end_lng'
    )
    return JsonResponse({'routes': list(routes)})


@login_required
def delete_route(request, route_id):
    route = get_object_or_404(Route, id=route_id, user=request.user)
    route.delete()
    return JsonResponse({'status': 'deleted'})


# views.py
@login_required
def delete_route(request, route_id):
    try:
        route = Route.objects.get(id=route_id, user=request.user)
        route.delete()
        return JsonResponse({'status': 'success'})
    except Route.DoesNotExist:
        return JsonResponse({'error': 'Маршрут не найден'}, status=404)


@method_decorator(csrf_exempt, name='dispatch')
class RouteSaveView(CreateView):
    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({'error': 'Требуется авторизация'}, status=401)

        try:
            data = json.loads(request.body)
            if not all(key in data for key in ['start_lat', 'start_lng', 'end_lat', 'end_lng']):
                return JsonResponse({'error': 'Недостаточно данных'}, status=400)

            route = Route.objects.create(
                user=request.user,
                start_lat=float(data['start_lat']),
                start_lng=float(data['start_lng']),
                end_lat=float(data['end_lat']),
                end_lng=float(data['end_lng']),
                name=data.get('name', 'Без названия')
            )
            return JsonResponse(route.to_dict(), status=201)
        except ValueError:
            return JsonResponse({'error': 'Неверный формат координат'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)