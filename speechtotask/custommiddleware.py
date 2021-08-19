from django.utils.deprecation import MiddlewareMixin

class CsrfHeaderMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        if "CSRF_COOKIE" in request.META:
            # csrfviewmiddleware sets response cookie as request.META['CSRF_COOKIE']
            response["X-CSRFTOKEN"] = request.META['CSRF_COOKIE']
        return response