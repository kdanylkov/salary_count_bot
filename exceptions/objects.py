class NotLaserProcedure(Exception):
    message = "Not an instance of a `Laser` procedure was returned"

    def __init__(self):
        super().__init__(self.message)


class VisitNotDeleted(Exception):
    def __init__(self, from_db: bool, from_obj: bool):
        value = 'database' if from_db else 'object'
        if not (from_db and from_obj):
            value = 'both database and object'

        message = f'Visit was not deleted {value}'
        super().__init__(message)
