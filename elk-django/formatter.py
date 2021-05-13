import json

from logstash.formatter import LogstashFormatterVersion1


class LogstashFormatter(LogstashFormatterVersion1):
    def format(self, record):
        message = {
            '@timestamp': self.format_timestamp(record.created),
            '@version': '1',
            'message': record.getMessage(),
            'host': self.host,
            'status_code': getattr(record, 'status_code', None),

            'path': record.pathname,
            'tags': self.tags,
            'type': self.message_type,
            'level': record.levelname,
            'logger_name': record.name,
        }

        if request := getattr(record, 'request', None):
            message['request_method'] = request.method
            message['request_url'] = str(request.build_absolute_uri())
            try:
                message['request_body'] = json.loads(request.body) if request.body else ''
            except:
                message['request_body'] = ''

            message['request_body'] = str(request.body)
            message['request_get_query'] = str(request.GET)

            message['user-agent'] = request.META.get('HTTP_USER_AGENT')
            message['domain'] = request.META.get('HTTP_HOST')
            message['geoip.ip'] = request.META.get('HTTP_X_FORWARDED_FOR') or request.META.get('REMOTE_ADDR')

            if user := getattr(request, 'user', None):
                message['user.username'] = str(user)
                message['user.id'] = getattr(user, 'id', None)
                message['user.email'] = getattr(user, 'email', None)
                message['user.is_anonymus'] = getattr(user, 'is_anonymous', None)

        message.update(self.get_extra_fields(record))

        if record.exc_info:
            message.update(self.get_debug_fields(record))

        return self.serialize(message)
