import logging

from django.utils.deprecation import MiddlewareMixin


request_logger = logging.getLogger('django.request')


class LoggingMiddleware(MiddlewareMixin):

    _initial_http_body = None

    def process_request(self, request):
        self._initial_http_body = request.body

    def process_response(self, request, response):
        """
        Adding request and response INFO logging
        """
        http_accept = request.META.get('HTTP_ACCEPT', '')
        is_allowed_content_type = 'text/html' in http_accept or 'application/json' in http_accept
        status_code = getattr(response, 'status_code', None)
        streaming = getattr(response, 'streaming', False)

        if not streaming and (200 >= status_code <= 400) and is_allowed_content_type:
            request_logger.log(
                logging.INFO, f'GET: {request.GET}', extra={
                    'request': request,
                    'request_method': request.method,
                    'request_url': request.build_absolute_uri(),
                    'request_body': self._initial_http_body.decode("utf-8"),
                    'response_body': response.content,
                    'status_code': response.status_code
                }
            )
        return response
