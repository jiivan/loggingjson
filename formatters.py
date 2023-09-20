import collections.abc
import json
from logging import Formatter

class JSONFormatter(Formatter):
    def format(self, record) -> str:
        record.message = record.getMessage()
        d = {}
        d['level'] = record.levelno  # or levelname
        d['name'] = record.name
        d['pathname'] = record.pathname
        if self.usesTime():
            d['time'] = self.formatTime(record, self.datefmt)
        d['msg'] = self.formatMessage(record)
        if record.args and isinstance(record.args, collections.abc.Mapping):
            d.update(record.args)
        if record.exc_info:
            d['error'] = {
                    'text': self.formatException(record.exc_info),
                    'stack': self.formatStack(record.stack_info),
            }
        return json.dumps(d)

    def usesTime(self) -> bool:
        return True

if __name__ == '__main__':
    import logging
    l = logging.getLogger()
    h = logging.StreamHandler()
    h.setFormatter(JSONFormatter(style="{"))
    l.addHandler(h)
    l.setLevel(logging.INFO)
    l.info("ABC")
    l.warning("a={a} %s", {'a': "<a value>"})
