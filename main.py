import urllib.request, json, socket
from urllib.parse import urlencode
from flask import Flask, render_template, request

app = Flask(
    __name__,
    instance_relative_config=False,
    template_folder="templates",
    static_folder="static"
)

"""
    Handler for calls to the Looking Glass API.
"""
def call_api(endpoint, params = None):
    query = ""
    if params != None:
        query = urlencode(params)

    api = "http://192.0.2.4:8001/api/v1/%s?%s" % (endpoint, query)
    code = 200
    response = None

    try:
        response = urllib.request.urlopen(api).read()
    except urllib.error.HTTPError as e:
        response = e.read()
        code = e.code

    if code == 200 or code == 400:
        return code, json.loads ( response )
    else:
        return code, response

"""
    Flask frontend for Looking Glass API.
"""
@app.route('/')
def home():
    code, routers = call_api(endpoint="routers")

    return render_template(
        'main.html',
        title    = "AS36198 looking glass",
        link     = "https://lg.as36198.net",
        keywords = "looking glass,as36198 looking glass,as36198 lg,bgp looking glass,bgp route server,route server",
        routers  = routers,
    )

"""
    Endpoint to receive AJAX requests from home() above and interface w/ API.
"""
@app.route('/ajax', methods=['GET'])
def ajax():

    router  = request.args['router']
    cmd     = request.args['cmd']
    host    = request.args['host']
    version = request.args['version']

    """
        Try DNS resolution for host. If version set to v4 then try A first and
        then AAAA. Otherwise try AAAA first. If unresolvable then assume host
        is an IP address.
    """
    if version == 'v4':
        try:
            record = socket.getaddrinfo(host, None, socket.AF_INET)[0][4][0]
            host   = record
        except (socket.gaierror):
            try:
                record = socket.getaddrinfo(host, None, socket.AF_INET6)[0][4][0]
                host   = record
            except (socket.gaierror):
                pass
    else:
        try:
            record = socket.getaddrinfo(host, None, socket.AF_INET6)[0][4][0]
            host   = record
        except (socket.gaierror):
            try:
                record = socket.getaddrinfo(host, None, socket.AF_INET)[0][4][0]
                host   = record
            except (socket.gaierror):
                pass

    code, result = call_api(endpoint=cmd, params={"router": router, "target": host})

    if code == 200:
        result_str = "%s> %s<br>%s" % ( router, result['command'], result['output'] )
    elif code == 400:
        result_str = result['message']
    else:
        result_str = 'Error connecting to router. Please try again.'

    return result_str
