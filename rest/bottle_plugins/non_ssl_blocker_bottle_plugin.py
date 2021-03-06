from biicode.common.utils.bii_logging import logger
from bottle import HTTPResponse, request


class NonSSLBlockerBottlePlugin(object):
    ''' The NonSSLBlockerBottlePlugin plugin blocks non-SSL requests'''

    name = 'nonsslblocker'

    def apply(self, callback, context):
        '''method called for wrap plugin operation'''
        def wrapper(*args, **kwargs):
            '''Check request and raise if its not https'''
            if request.headers.get('X-Forwarded-Proto', 'http') != 'https':
                logger.debug("Non http request blocked: %s" % request)
                raise self.default_non_ssl_http_response
            else:
                return callback(*args, **kwargs)

        return wrapper

    @property
    def default_non_ssl_http_response(self):
        '''Default response for non ssl request'''
        r = HTTPResponse(body="Connect to https", status="403 - SSL required.")
        r.set_header('Content-Type', 'text/plain')  # Never respond with text/html client doesnt understand it
        return r
