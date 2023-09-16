class UnknownCallbackError(Exception):
    def __init__(self, callback_data, func_name):
        self.message = f"Unknown callback data: {callback_data}"
        super().__init__(self.message)
