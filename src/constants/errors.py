class InternalServerError(Exception):
    def __init__(self, message, ):
        Exception.__init__(self, message)


class NotFoundError(Exception):
    def __init__(self, message, ):
        Exception.__init__(self, message)


class UnauthenticatedError(Exception):
    def __init__(self, message, ):
        Exception.__init__(self, message)


class UnauthorizedError(Exception):
    def __init__(self, message, ):
        Exception.__init__(self, message)
