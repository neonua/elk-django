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

        status_code = getattr(response, 'status_code', None)

        if 200 >= status_code <= 400:
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
