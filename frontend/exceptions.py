class UnsupportedHTTPMethod(Exception):
    def __init__(self, method_tried):
        super().__init__()
        self.__method_tried = method_tried

    def __str__(self):
        return "\"{}\" method unsupported, probably is a valid HTTP method, but our server does not handle it".format(self.__method_tried)

    def __repr__(self):
        return "UnsupportedHTTPMethod(\"{}\")".format(self.__method_tried)


class IncorrectRequestBody(ValueError):
    def __init__(self, body):
        super().__init__()
        self.__body = body

    def __str__(self):
        return "Incorrect body \"{}\". Must be a dictionary, it'll be converted to JSON string later".format(self.__body)

    def __repr__(self):
        return "IncorrectRequestBody({})".format(self.__body)