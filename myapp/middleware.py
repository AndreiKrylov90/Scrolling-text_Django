from django.conf import settings


def dynamic_host_middleware(get_response):
    def middleware(request):
        host = request.META.get('HTTP_X_FORWARDED_HOST', '') or request.META.get('HTTP_HOST', '') or request.META.get('REMOTE_ADDR', '')

        if host:
            host = host.split(':')[0]
            if host not in settings.ALLOWED_HOSTS:
                settings.ALLOWED_HOSTS.append(host)
            origin = f"{request.scheme}://{host}"
            if origin not in settings.CSRF_TRUSTED_ORIGINS:
                settings.CSRF_TRUSTED_ORIGINS.append(origin)

        response = get_response(request)
        return response
    return middleware
