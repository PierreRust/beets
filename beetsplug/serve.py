# This file is part of beets.
# Copyright 2013, Adrian Sampson.
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
from beets.dbcore import query
from beets.dbcore.query import MatchQuery, AndQuery
from beets.library import Album

"""REST API to beets."""
from beets.plugins import BeetsPlugin
from beets import ui, config, util
import beets.library
import flask
from flask import g, request
from flask import jsonify
import json
from marshmallow import Serializer, fields
import time

class BeetsDateField(fields.Raw):
    def format(self, value):
        return time.strftime(beets.config['time_format'].get(unicode),
                             time.localtime(value or 0))


# TODO: create several serializer with a different set of fields ?
# TODO: dynamically add flexattr 
class AlbumSerializer(Serializer):

    created_at = fields.DateTime()
    id = fields.String(required=True)
    added = BeetsDateField()
    albumartist = fields.String()
    albumartist_sort = fields.String()
    albumartist_credit = fields.String()
    album = fields.String()
    genre = fields.String()
    year = fields.Integer()
    month = fields.Integer()
    day = fields.Integer()
    tracktotal = fields.Integer()
    disctotal = fields.Integer()


album_simple_serializer = AlbumSerializer.factory(only = ('id','album','genre','albumartist'))
album_full_serializer = AlbumSerializer.factory()

# Flask setup.
app = flask.Flask(__name__)

@app.before_request
def before_request():
    g.lib = app.config['lib']
    

@app.route('/albums', methods=['GET'])
def albums_list():
    
    # build a query out of the parameter
    # TODO: add sort option : needs support in the core
    # TODO: add (optional?) pagination
    # TODO: add links to related objects (tracks, and album ?)
    # with url template
    # with include documents for tracks ?
    queries = []
    for (arg_name, arg_value) in request.args.iteritems():
        # Check if the arg is a valid filter name
        if arg_name in Album._fields: 
            queries.append(MatchQuery(arg_name, arg_value))

    albums = g.lib.albums(AndQuery(queries))
        
    #return jsonify({"args" : request.args})        
    
#     return jsonify({"albums" : album_simple_serializer(albums, many=True).data})        
    return jsonify({"albums" : album_full_serializer(albums, many=True).data})        


@app.route('/albums/<int:album_id>/art', methods=['GET'])
def album_art():
    """This enpoint returns the album art  
    """
    pass

@app.route('/albums/<int:album_id>/file', methods=['GET'])
def album_file():
    """This enpoint returns an archive file that contains all files for this 
    album.  
    """
    pass


#api.add_resource(AlbumsResource, '/albums')
#api.decorators=[cors.crossdomain(origin='*')]

class WebPlugin(BeetsPlugin):
    def __init__(self):
        super(WebPlugin, self).__init__()
        self.config.add({
            'host': u'',
            'port': 8337,
        })

    def commands(self):
        cmd = ui.Subcommand('serve', help='start serving the REST API')
        cmd.parser.add_option('-d', '--debug', action='store_true',
                              default=False, help='debug mode')

        def func(lib, opts, args):
            args = ui.decargs(args)
            if args:
                self.config['host'] = args.pop(0)
            if args:
                self.config['port'] = int(args.pop(0))

            app.config['lib'] = lib
            app.run(host=self.config['host'].get(unicode),
                    port=self.config['port'].get(int),
                    debug=opts.debug, threaded=True)
        cmd.func = func
        return [cmd]
        