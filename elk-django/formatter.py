from logstash.formatter import LogstashFormatterVersion1


class LogstashFormatter(LogstashFormatterVersion1):
    def format(self, record, sent_request=None):
        caddr = 'unknown'
        user = None
        domain = None
        useragent = None
        if hasattr(record, 'request'):
            caddr = record.request.META.get('HTTP_X_FORWARDED_FOR') or record.request.META.get('REMOTE_ADDR')
            user = record.request.user if hasattr(record.request, 'user') else None
            domain = record.request.META.get('HTTP_HOST')
            useragent = record.request.META.get('HTTP_USER_AGENT')

        if user:
            user_id = record.request.user.id
            is_anonymus = record.request.user.is_anonymous
        else:
            user_id = None
            is_anonymus = True

        message = {
            '@timestamp': self.format_timestamp(record.created),
            '@version': '1',
            'message': record.getMessage(),
            'host': self.host,

            'client': caddr,
            'geoip.ip': caddr,
            'user.username': str(user),
            'user.id': str(user_id),
            'user.is_anonymus': str(is_anonymus),
            'domain': domain,
            'user-agent': str(useragent),

            'path': record.pathname,
            'tags': self.tags,
            'type': self.message_type,

            'level': record.levelname,
            'logger_name': record.name,
        }

        message.update(self.get_extra_fields(record))

        if record.exc_info:
            message.update(self.get_debug_fields(record))

        return self.serialize(message)
