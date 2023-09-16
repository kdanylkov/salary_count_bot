class NotLaserProcedure(Exception):
    message = "Not an instance of a `Laser` procedure was returned"

    def __init__(self):
        super().__init__(self.message)
