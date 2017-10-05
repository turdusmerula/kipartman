#!/usr/bin/env python

import connexion
from swagger_server.encoder import JSONEncoder
from os.path import expanduser

home = expanduser("~")

if __name__ == '__main__':
    app = connexion.App(__name__, specification_dir='./swagger/')
    app.app.json_encoder = JSONEncoder
    app.add_api('swagger.yaml', arguments={'title': 'Kipartman api specifications'})

    from flask import Flask, request, send_from_directory
    @app.route('/file/<path:path>')
    def send_js(path):
        print "aaaaa"
        return send_from_directory(home+'/.kipartman/storage', path)

    app.run(port=8200, debug=True)
