from logstash.formatter import LogstashFormatterVersion1


class LogstashFormatter(LogstashFormatterVersion1):
    def format(self, record, sent_request=None):
        caddr = 'unknown'
        if hasattr(record, 'request'):
            caddr = record.request.META.get('HTTP_X_FORWARDED_FOR') or record.request.META.get('REMOTE_ADDR')

        message = {
            '@timestamp': self.format_timestamp(record.created),
            '@version': '1',
            'message': record.getMessage(),
            'host': self.host,

            'client': caddr,
            'username': str(record.request.user) if hasattr(record, 'request') else None,

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
