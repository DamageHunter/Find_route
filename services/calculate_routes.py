from abc import ABC, abstractmethod
from trains.models import Train


class Handler(ABC):

    @abstractmethod
    def set_next(self, handler):
        pass

    @abstractmethod
    def handle(self, request):
        pass


class RouteHandler(Handler):
    _next_handler: Handler = None

    def set_next(self, handler: Handler) -> Handler:
        self._next_handler = handler
        return handler

    @abstractmethod
    def handle(self, request: dict) -> bool:
        if self._next_handler:
            return self._next_handler.handle(request)


class ExistHandler(RouteHandler):
    """
        Checks possible paths from start to endpoint

        Take transport type and return queryset of all routes for this transport after that method handle call
        get_all_routes function which create graph by all transport paths (with get_graph function)and add all
        possible ways to request and call next handler or raise Value error
    """
    _transport_routes = {
        "Train": Train.objects.all()
    }

    def __init__(self, transport):
        self._transport_routes = self._transport_routes.get(transport)

    def handle(self, request: dict):
        start = request['from_city'].id
        finish = request['to_city'].id
        request['transport_routes_queryset'] = self._transport_routes
        request['routes'] = list(self.get_all_routes(start, finish))

        if request['routes']:
            super().handle(request=request)
        else:
            raise ValueError('Нет путей удовлетворяющий начальной и конечной точкам')

    def get_all_routes(self, start, goal) -> list:
        # find existing routes for condition (by dfs)
        graph = self.get_graph_for_transport()
        stack = [(start, [start])]
        while stack:
            (vertex, path) = stack.pop()
            if vertex in graph.keys():
                for next_ in graph[vertex] - set(path):
                    if next_ == goal:
                        yield path + [next_]
                    else:
                        stack.append((next_, path + [next_]))

    def get_graph_for_transport(self) -> dict:
        # Create graph for dfs algorithm
        graph = dict()
        for route in self._transport_routes:
            graph.setdefault(route.from_city_id, set())
            graph[route.from_city_id].add(route.to_city_id)
        return graph


class ThroughCitiesHandler(RouteHandler):
    """
    Checks if there are routes passing through the cities specified in the form; if not, it gives an error, otherwise it
    calls the next handler
    """

    def handle(self, request: dict):
        if request['cities']:
            request['routes'] = self.through_cities_condition(request)

        if request['routes']:
            super().handle(request=request)
        else:
            raise ValueError('Нет путей проходящих через данные города')

    @staticmethod
    def through_cities_condition(request) -> list:
        # Builds a list of routes passing through cities
        cities_id = [city.id for city in request['cities']]
        routes_tmp = []
        for route in request['routes']:
            if all(city in route for city in cities_id):
                routes_tmp.append(route)
        return routes_tmp


class TimeHandler(RouteHandler):
    """
    Checks if there are paths that match in time, also removes the queryset with all paths
    """

    def handle(self, request: dict):
        if request['time']:
            request['trains'] = self.time_condition(request)
            dict.pop(request, 'transport_routes_queryset')

        if request['trains']:
            super().handle(request=request)
        else:
            raise ValueError('Нет маршрутов удовлетворяющих данному времени')

    @staticmethod
    def time_condition(request) -> list:
        # Check time condition and build routes
        all_trains = {}
        result_trains = []
        for route in request['transport_routes_queryset']:
            all_trains.setdefault((route.from_city_id, route.to_city_id), [])
            all_trains[(route.from_city_id, route.to_city_id)].append(route)
        for route in request['routes']:
            tmp = {'trains': [], 'total_time': 0, 'trains_lst': route}
            for i in range(len(route) - 1):
                trains = all_trains[(route[i], route[i + 1])]
                tmp['total_time'] += trains[0].travel_time
                tmp['trains'].append(trains[0])
            if tmp['total_time'] <= request['time']:
                result_trains.append(tmp)
        return sorted(result_trains, key=lambda x: x['total_time'])


def find_routes(data: dict):
    # Assign handlers to variables
    EXIST_ROUTES = ExistHandler("Train")
    THROUGH_CITIES = ThroughCitiesHandler()
    TIME_MATCHING = TimeHandler()

    # Set handlers chain
    EXIST_ROUTES.set_next(THROUGH_CITIES).set_next(TIME_MATCHING)
    EXIST_ROUTES.handle(data)
    if data:
        return data
    else:
        raise ValueError('Маршрутов не существует')
