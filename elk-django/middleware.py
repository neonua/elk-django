import logging

from django.utils.deprecation import MiddlewareMixin


request_logger = logging.getLogger('django.request')


class LoggingMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        """
        Adding request and response INFO logging
        """
        http_accept = request.META.get('HTTP_ACCEPT', '')
        content_type = request.META.get('CONTENT_TYPE', '')
        status_code = getattr(response, 'status_code', None)
        streaming = getattr(response, 'streaming', False)

        is_allowed_http_accept = 'text/html' in http_accept or 'application/json' in http_accept
        is_allowed_content_type = 'multipart' not in content_type

        if not streaming and (200 <= status_code <= 400) and is_allowed_http_accept and is_allowed_content_type:
            request_logger.log(
                logging.INFO, f'{request.method}: {request.build_absolute_uri()}', extra={
                    'request': request,
                    'status_code': response.status_code
                }
            )
        return response
