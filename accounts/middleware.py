from tools.visitor import get_visitor_ip_address
from .models import User
from django import http


def block_ip_middleware(get_response):
    def middleware(request):
        ip = get_visitor_ip_address(request)
        try:
            User.objects.get(ip=ip, banned_by_ip=True)
            return http.HttpResponseNotFound()
        except:
            return get_response(request)

    return middleware
