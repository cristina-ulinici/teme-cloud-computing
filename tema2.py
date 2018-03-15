from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import SocketServer
import json
import re

def get_collection(name):
    data = json.load(open("colectie1.json"))
    return json.dumps(data[name])

def get_collection_length(name):
    data = json.load(open("colectie1.json"))
    return len(data[name])

def get_collection_item(name, nr_item):
    data = json.load(open("colectie1.json"))
    return json.dumps(data[name][nr_item - 1])

def find_collection(name):
    data = json.load(open("colectie1.json"))
    if name in data:
        return True
    else:
        return False

def check_get(path):
    col_item = re.match(r'/(\w+)/(\d+)', path)
    if (col_item):
        if (int(col_item.group(2)) <= get_collection_length(col_item.group(1))):
            return (200, get_collection_item(col_item.group(1), int(col_item.group(2))))
        else:
            return (404, "{ \"" + path + "\" : \"not found\"  }")
    else:
        col = re.match(r'/(\w+)', path)
        if (col):
            name_col = col.group(1)
            if(find_collection(name_col)):
                return (200, get_collection(name_col))
            else:
                return (404, "{ \"" + path + "\" : \"not found\"  }")
        else:
            return(400, "{ \"" + path + "\" : \"bad request\"  }")

def check_post(path, body):
    #adauga un el nou in colectie
    req = re.match("/(\w+)", path)
    if(not req):
        return 400
    name = req.group(1)
    if(not find_collection(name)):
        return 404
    f = open("colectie1.json", "r")
    data = json.load(f)
    f.close()
    b = json.loads(body)
    data[name].append(b)
    f = open("colectie1.json", "w")
    json.dump(data, f, indent=4)
    f.close()
    return 201

def check_put(path, body):
    #modifica element sau colectie
    re1 = re.match(r'/(\w+)/(\d+)', path)
    if(re1):
        name = re1.group(1)
        index = int(re1.group(2))
        if(not find_collection(name)):
            return 404
        if(get_collection_length(name) <= index):
            return 404
        f = open("colectie1.json", "r")
        data = json.load(f)
        f.close()
        b = json.loads(body)
        data[name][index-1] = b
        f = open("colectie1.json", "w")
        json.dump(data, f, indent=4)
        f.close()
        return 200
    else:
        re2 = re.match(r'/(\w+)', path)
        if (not re2):
            return 400
        name = re2.group(1)
        if(not find_collection(name)):
            return 404
        f = open("colectie1.json", "r")
        data = json.load(f)
        f.close()
        b = json.loads(body)
        l = []
        l.append(b)
        data[name] = l
        f = open("colectie1.json", "w")
        json.dump(data, f, indent=4)
        f.close()
        return 200

def check_delete(path):
    re1 = re.match(r'/(\w+)/(\d+)', path)
    if(re1):
        name = re1.group(1)
        index = int(re1.group(2))
        if(not find_collection(name)):
            return 404
        if(get_collection_length(name) < index):
            return 404
        f = open("colectie1.json", "r")
        data = json.load(f)
        f.close()
        del data[name][index-1]
        f = open("colectie1.json", "w")
        json.dump(data, f, indent=4)
        f.close()
        return 200
    else:
        re2 = re.match(r'/(\w+)', path)
        if (not re2):
            return 400
        name = re2.group(1)
        if(not find_collection(name)):
            return 404
        f = open("colectie1.json", "r")
        data = json.load(f)
        f.close()
        del data[name]
        f = open("colectie1.json", "w")
        json.dump(data, f, indent=4)
        f.close()
        return 200
        


class HandlerClass(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_header('Content-type', 'text/json')
        self.end_headers()

    def do_HEAD(self):
        self._set_headers()

# 404 - not found / 200 - succes / 400 - bad request
    def do_GET(self):
        resp, text = check_get(self.path)
        self.send_response(resp)
        self._set_headers()
        if(resp == 200):
            self.wfile.write(text)

# 201 - created / 400 - bad request / 404 - not found
    def do_POST(self):
        content_len = int(self.headers.getheader('content-length'))
        post_body = self.rfile.read(content_len)
        resp = check_post(self.path, post_body)
        self.send_response(resp)
        self._set_headers()
        
# 200 succes / 404 - not found / 400 - bad rquest
    def do_PUT(self):
        content_len = int(self.headers.getheader('content-length'))
        post_body = self.rfile.read(content_len)
        resp = check_put(self.path, post_body)
        self.send_response(resp)
        self._set_headers()

# 200 - success / 404 - not found
    def do_DELETE(self):
        resp = check_delete(self.path)
        self.send_response(resp)
        self._set_headers()

httpd = HTTPServer(("", 80), HandlerClass)
print 'Starting httpd...'
httpd.serve_forever()
