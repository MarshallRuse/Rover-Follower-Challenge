
#class Error(Exception):
 #   pass

class RoverCoordinatesReturnError(Exception):

    def __init__(self, message):
        super().__init__(message)


class RoverCompassReturnError(Exception):

    def __init__(self, message):
        super().__init__(message)