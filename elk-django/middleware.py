import logging

from django.utils.deprecation import MiddlewareMixin


request_logger = logging.getLogger('django.request')


class LoggingMiddleware(MiddlewareMixin):
    _initial_http_body = None
    is_request_validate = None
    is_response_validate = None

    def __call__(self, request):
        response = None

        self._validate_request(request)
        if self.is_request_validate:
            response = self.process_request(request)
        response = response or self.get_response(request)

        self._validate_response(response)
        if self.is_request_validate and self.is_response_validate:
            response = self.process_response(request, response)

        return response

    def _validate_request(self, request):
        http_accept = request.META.get('HTTP_ACCEPT', '')
        content_type = request.META.get('CONTENT_TYPE', '')

        is_allowed_http_accept = 'text/html' in http_accept or 'application/json' in http_accept
        is_allowed_content_type = 'multipart' not in content_type

        self.is_request_validate = is_allowed_http_accept and is_allowed_content_type

    def _validate_response(self, response):
        status_code = getattr(response, 'status_code', None)
        streaming = getattr(response, 'streaming', False)

        self.is_response_validate = not streaming and (200 <= status_code <= 399)

    def process_request(self, request):
        self._initial_http_body = request.body

    def process_response(self, request, response):
        """
        Adding request and response INFO logging
        """
        request_logger.log(
            logging.INFO, f'{request.method}: {request.build_absolute_uri()}', extra={
                'request': request,
                'status_code': response.status_code
            }
        )
        return response
