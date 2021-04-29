from logstash.handler_tcp import TCPLogstashHandler
from logstash.formatter import LogstashFormatterVersion0

from .formatter import LogstashFormatter


class ELKTCPLogstashHandler(TCPLogstashHandler, object):

    def __init__(self, host, port=5959, message_type='logstash', tags=None, fqdn=False, version=1):
        super().__init__(host, port)
        if version == 1:
            self.formatter = LogstashFormatter(message_type, tags, fqdn)
        else:
            self.formatter = LogstashFormatterVersion0(message_type, tags, fqdn)
