import threading
from exceptions import UnsupportedHTTPMethod, IncorrectRequestBody
import requests
from queue import Queue
import json


class Request(threading.Thread):
    SUPPORTED_METHODS = ["GET", "PUT"]

    def __init__(self, status_queue, endpoint, method="GET", body=None, host="127.0.0.1", port="8080"):
        super().__init__()

        if method not in Request.SUPPORTED_METHODS:
            raise UnsupportedHTTPMethod(method)

        if not isinstance(endpoint, str):
            raise TypeError("The endpoint {} should be a string".format(endpoint))
        if not isinstance(host, str):
            raise TypeError("The host {} should be a string".format(host))
        if not isinstance(status_queue, Queue):
            raise TypeError("The status_queue {} should be an instance of Queue".format(status_queue))

        if body is not None and not isinstance(body, dict):
            raise IncorrectRequestBody(body)

        self.__body = body

        self.__method = method
        self.__url_string = "http://{}:{}/{}".format(host, port, endpoint)

        self.__status_queue = status_queue

    @property
    def url(self):
        return self.__url_string

    # Override
    def run(self, *args, **kwargs):
        request_fn = None
        if self.__method == "GET":
            request_fn = requests.get
        elif self.__method == "PUT":
            request_fn = requests.put

        lock = threading.Lock()
        lock.acquire()
        self.__status_queue.put("sent")
        lock.release()
        # since status queue will be in heap, it'll be ok to modify it here
        try:
            req = None
            if self.__body is not None:
                req = request_fn(self.__url_string, data=json.dumps(self.__body), headers={
                    "Content-Type": "application/json; charset=utf-8"
                })
            else:
                req = request_fn(self.__url_string)
        except Exception:
            lock.acquire()
            self.__status_queue.put("error")
            lock.release()
            return

        lock.acquire()
        self.__status_queue.put("received")

        if req.status_code != 200:
            self.__status_queue.put("error")
        else:
            try:
                self.__status_queue.put("ok")
                self.__status_queue.put(req.json())
            except Exception:
                self.__status_queue.put("error")

        lock.release()
