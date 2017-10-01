#!/usr/bin/env python

import os, sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
#sys.path.append(os.path.join(os.path.dirname(__file__), 'kipartbase'))


import connexion
from swagger_server.encoder import JSONEncoder
from os.path import expanduser

home = expanduser("~")


def migrate():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError:
        # The above import may fail for some other reason. Ensure that the
        # issue is really that Django is missing to avoid masking other
        # exceptions on Python 2.
        try:
            import django
        except ImportError:
            raise ImportError(
                "Couldn't import Django. Are you sure it's installed and "
                "available on your PYTHONPATH environment variable? Did you "
                "forget to activate a virtual environment?"
            )
        raise
    execute_from_command_line(["manage.py", "migrate"])
    

def serve(args=None):    

    app = connexion.App(__name__, specification_dir='./swagger_server/swagger/')
    app.app.json_encoder = JSONEncoder
    app.add_api('swagger.yaml', arguments={'title': 'Kipartman api specifications'})

    # add a static file server
    from flask import Flask, request, send_from_directory
    @app.route('/file/<path:path>')
    def send_js(path):
        return send_from_directory(home+'/.kipartman/storage', path)

    app.run(port=8200, debug=True)


def main():
    data_path = os.path.join(home, '.kipartman')
    if os.path.exists(data_path)==False:
        os.mkdir(os.path.join(home, '.kipartman'))
    
    os.chdir(os.path.dirname(__file__))

    # do django migrations
    migrate()
    
    # serve api
    serve()

if __name__ == '__main__':
    main()