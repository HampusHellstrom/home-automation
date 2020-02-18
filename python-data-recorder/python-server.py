from http.server import HTTPServer, BaseHTTPRequestHandler
from optparse import OptionParser
import argparse
import json
from pprint import pprint
from datetime import datetime as dt
import csv

"""
curl --header "Content-type: application/json" --request POST --data '{"sensor":"sensor_1","measure":"temperature", "value": 100,"note": "outside"}' http://localhost:8080
"""

CSV_FILE = "logs/log.csv"


class RequestHandler(BaseHTTPRequestHandler):

    def _html(self, message):
        """This just generates an HTML document that includes `message`
        in the body. Override, or re-write this do do more interesting stuff.
        """
        content = f"<html><body><h1>{message}</h1></body></html>"
        return content.encode("utf8")  # NOTE: must return a bytes object!

    def _set_headers(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

    def do_GET(self):
        self._set_headers()
        self.wfile.write(self._html("Hello!"))
        # self.send_response(200)u

    def do_POST(self):

        print(self.headers)

        content_type = self.headers['Content-Type']  # <--- Gets the size of data

        if content_type != 'application/json':
            self.send_response(400)
            self.end_headers()
            return

        content_length = int(self.headers['Content-Length'])  # <--- Gets the size of data
        post_data = self.rfile.read(content_length)  # <--- Gets the data itself
        j_son = json.loads(post_data.decode("utf-8"))

        pprint(j_son)

        with open(CSV_FILE, "a", newline='') as f:
            csv_writer = csv.writer(f)
            timestamp = dt.now().strftime("%m/%d/%Y, %H:%M:%S")
            row = [timestamp, j_son["sensor"], j_son["measure"], j_son["value"], j_son["note"]]
            csv_writer.writerow(row)

        self._set_headers()
        self.wfile.write(self._html("Kolla på posten!"))

    do_PUT = do_POST
    do_DELETE = do_GET


def run(server_class=HTTPServer, handler_class=RequestHandler, addr="localhost", port=8080):
    server_address = (addr, port)
    httpd = server_class(server_address, handler_class)

    print(f"Starting httpd server on {addr}:{port}")
    httpd.serve_forever()


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Run a simple HTTP server")
    parser.add_argument(
        "-l",
        "--listen",
        default="localhost",
        help="Specify the IP address on which the server listens",
    )

    parser.add_argument(
        "-p",
        "--port",
        type=int,
        default=8080,
        help="Specify the port on which the server listens",
    )

    args = parser.parse_args()
    run(addr=args.listen, port=args.port)
