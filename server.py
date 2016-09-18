# coding: utf-8 
import SocketServer
import mimetypes

# Copyright 2013 Abram Hindle, Eddie Antonio Santos
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/


class MyWebServer(SocketServer.BaseRequestHandler):
    
    def handle(self):
        self.success = True
        self.data = self.request.recv(1024).strip()
        print ("Got a request of: %s\n" % self.data)
	self.parse_data(self.data)

        self.get_page_info()
        #shows the webpage if it exists
        if self.success:
            self.request.sendall("HTTP/1.1 200 OK\r\n")
	    self.request.sendall("Content-Type: "+str(self.url_type)+"\r\n")
	    self.request.sendall("Content-Length: "+ str(len(self.file_content))+"\r\n\r\n")
            self.request.sendall(self.file_content)
		
    #https://docs.python.org/2/tutorial/inputoutput.html
    #Displays the webpage
    def get_page_info(self):
    	#gets the url of the requested page
        url = self.path
        url_split = url.split("/")
	
	#gets the mimetype of the url
	url_type = mimetypes.guess_type(url)[0] 
        file_content = ""
        self.file_content = file_content
        self.url_type = url_type
        print url_split
        print self.url_type
            
        #redirect to index.html if not specified
	if url_split[-1] == "":
           self.url_type = "text/html"
           f = open("www/" + url + "/index.html","r")
           self.file_content = f.read()
	   f.close

        #redirects to index.html if index specified
        elif url_split[-1] == "index":
           self.url_type = "text/html"
           f = open("www/" + url + ".html","r")
           self.file_content = f.read()
	   f.close

        #opens specified file content
        elif self.url_type == "text/css" or self.url_type == "text/html":
           try:
               f = open("www/" + url, "r")
               self.file_content = f.read()
               f.close
           except:
               self.throw_error()
     	else:
	   self.throw_error()
           self.success = False
        print self.url_type

    #Gives 404 error when page not found
    def throw_error(self):
        response_content = "HTTP/1.1 404 NOT FOUND\r\n\r\n <html><body><h1>404 File Not Found</h1></body><html>"
	self.request.sendall(response_content)	
	
    #from sberry at http://stackoverflow.com/questions/18563664/socketserver-python
    #parses data to get separate headers
    def parse_data(self,data):
    	headers = {}
	lines = data.splitlines()
	inbody = False
        body = ''
        for line in lines[1:]:
            if line.strip() == "":
                inbody = True
            if inbody:
                body += line
            else:
                k, v = line.split(":", 1)
                headers[k.strip()] = v.strip()
        method, path, _ = lines[0].split()
        self.path = path.lstrip("/")
        self.headers = headers
        self.body = body

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080  

    SocketServer.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = SocketServer.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
