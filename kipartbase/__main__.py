#!/usr/bin/python3

import os, sys
sys.path.append(os.path.dirname(__file__))

import connexion
from swagger_server.encoder import JSONEncoder
from os.path import expanduser


def main(args=None):    
    home = expanduser("~")

    app = connexion.App(__name__, specification_dir='./swagger_server/swagger/')
    app.app.json_encoder = JSONEncoder
    app.add_api('swagger.yaml', arguments={'title': 'Kipartman api specifications'})

    from flask import Flask, request, send_from_directory
    @app.route('/file/<path:path>')
    def send_js(path):
        return send_from_directory(home+'/.kipartman/storage', path)

    app.run(port=8200, debug=True)


if __name__ == '__main__':
    main()