from .backends import UserNotVerified
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.core.exceptions import PermissionDenied



class UserVerifyMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response
    
    def process_exception(self, request, exception):
        
        if isinstance(exception, UserNotVerified):
            return HttpResponseRedirect(reverse_lazy('resend'))
        
        
        
        
class Error404Middleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response
    
    def process_exception(self, request, exception):
        
        if isinstance(exception, PermissionDenied):
            return HttpResponseRedirect(reverse_lazy('not-permission'))