from logging.handlers import RotatingFileHandler
import multiprocessing, threading, logging, sys, traceback
from concurrent.futures import *

class MultiProcessingLogHandler(logging.Handler):
    def __init__(self, name, mode, log_size_in_bytes, backup_count, max_workers):
        #app.config['LOG_THREAD_POOL']
        logging.Handler.__init__(self)
        self._handler = RotatingFileHandler(name, mode=mode, maxBytes=log_size_in_bytes,backupCount= backup_count)
        self.queue = multiprocessing.Queue(-1)
        executor = ThreadPoolExecutor(max_workers=max_workers)
        executor.submit(self.receive)

    def setFormatter(self, fmt):
        logging.Handler.setFormatter(self, fmt)
        self._handler.setFormatter(fmt)

    def receive(self):
        while True:
            try:
                record = self.queue.get()
                self._handler.emit(record)
            except (KeyboardInterrupt, SystemExit):
                pass
            except EOFError:
                pass
            except:
                pass
                # traceback.print_exc(file=sys.stderr)

    def send(self, s):
        self.queue.put_nowait(s)

    def _format_record(self, record):
        # ensure that exc_info and args
        # have been stringified.  Removes any chance of
        # unpickleable things inside and possibly reduces
        # message size sent over the pipe
        if record.args:
            record.msg = record.msg +','.join([rec for rec in record.args if (rec is not None or rec is not '')])
            record.args = None
        if record.exc_info:
            dummy = self.format(record)
            record.exc_info = None

        return record

    def emit(self, record):
        try:
            s = self._format_record(record)
            self.send(s)
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            self.handleError(record)

    def close(self):
        self._handler.close()
        logging.Handler.close(self)