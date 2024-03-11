from datetime import datetime
import os
from ssl import SSLContext, PROTOCOL_TLS_SERVER

def validate_datetime(datetime_str):
    try:
        datetime_format = "%Y-%m-%dT%H:%M:%S"
        datetime_obj = datetime.strptime(datetime_str, datetime_format)
        return True
    except ValueError:
        return False
    
def get_file_path(relative_file_path=None):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, relative_file_path)
    return file_path

def check_https_desired():
    use_https = os.getenv('USE_HTTPS')
    if use_https is not None:

        if not use_https.isdigit():
            if use_https.startswith("-") and not use_https[1:].isdigit(): # supports negative numbers
                raise Exception('If USE_HTTPS is set, it must be an integer. Values > 0 will set up HTTPS. Values <= 0 will bypass HTTPS.')
        
        use_https = int(use_https)
        if (use_https > 0):
            return True
        
    return False

def set_up_https(httpd):
    print('Setting up HTTPS...\n')
    print('Please enter cert password...\n')
    sslctx = SSLContext(PROTOCOL_TLS_SERVER)
    sslctx.check_hostname = False
    httpd.socket = sslctx.wrap_socket(httpd.socket, server_side=True)

    ssl_keyfile_file_path = get_file_path('../../ssl/key.pem') # TODO change these to accept from ENV variables
    ssl_certfile_file_path = get_file_path('../../ssl/cert.pem')

    sslctx.load_cert_chain(certfile=ssl_certfile_file_path, keyfile=ssl_keyfile_file_path)
