# middleware.py

from django.http import JsonResponse
from django.shortcuts import render

class CustomExceptionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_exception(self, request, exception):
        # Handle server errors (500)
        response = render(request, 'account/500.html', {'error': str(exception)})
        response.status_code = 500
        return response

class MethodNotAllowedMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if response.status_code == 405:
            response = render(request, 'account/405.html')
        return response

class PageNotFoundMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if response.status_code == 404:
            response = render(request, 'account/404.html')
        return response

class ForbiddenMiddleware: 
    def __init__(self, get_response): 
        self.get_response = get_response 
    def __call__(self, request): 
        response = self.get_response(request) 
        if response and response.status_code == 403: 
            response = render(request, '403.html') 
        return response