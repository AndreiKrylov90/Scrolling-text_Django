from django.conf import settings


def dynamic_host_middleware(get_response):
    def middleware(request):
        host = request.get_host().split(':')[0]
        if host not in settings.ALLOWED_HOSTS:
            settings.ALLOWED_HOSTS.append(host)
        response = get_response(request)
        return response
    return middleware
