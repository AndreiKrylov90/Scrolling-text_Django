from django.conf import settings


class DynamicHostMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        host = request.get_host().split(':')[0]
        if host not in settings.ALLOWED_HOSTS:
            settings.ALLOWED_HOSTS.append(host)
        response = self.get_response(request)
        return response
