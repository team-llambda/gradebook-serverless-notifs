from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from hashlib import sha256

import requests as r
from bs4 import BeautifulSoup as bs

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()

        cookies = self.headers.get("cookie")        # Get cookies
        
        # Make the request to the grades page
        classes_page = r.get("https://wa-bsd405-psv.edupoint.com/PXP2_Gradebook.aspx?AGU=0", headers = {
            "cookie" : cookies
        })

        parsed_page = bs(classes_page.text)
        table = parsed_page.find("table", attrs = {
            "class" : "data-table"
        })

        classes = table.find_all('tr')
        
        class_data = []

        grades_blob = ""

        for c in classes[1:]:
            grade = c.find("span", attrs = {
                "class" : "score"
            }).get_text()

            grades_blob += grade

        print(grades_blob)

        # Hash that mf
        digest = sha256().hexdigest()

        message = json.dumps({
            "digest" : digest
        })
        
        self.wfile.write(message.encode())

