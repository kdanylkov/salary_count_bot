class UnknownCallbackError(Exception):
    def __init__(self, callback_data):
        self.message = f"Unknown callback data: {callback_data}"
        super().__init__(self.message)
