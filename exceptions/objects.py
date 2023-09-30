class NotLaserProcedure(Exception):
    message = "Not an instance of a `Laser` procedure was returned"

    def __init__(self):
        super().__init__(self.message)


class VisitNotDeleted(Exception):
    message = 'Visit was not deleted %s'

    def __init__(self, from_db: bool, from_obj: bool):
        value = 'database' if from_db else 'object'
        if not (from_db and from_obj):
            value = 'both database and object'

        super().__init__(self.message % (value,))


class ProcedureNotDeleted(VisitNotDeleted):
    message = 'Procedure was not deleted %s'
