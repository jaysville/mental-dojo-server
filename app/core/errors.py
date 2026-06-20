class AppError(Exception):
    def __init__(self, code: str, message: str, status_code: int = 400, fields=None):
        self.code = code
        self.message = message
        self.status_code = status_code
        self.fields = fields or None

    def to_dict(self):
        return {
            "code": self.code,
            "message": self.message,
            "fields": self.fields,
        }

    def __str__(self):
        return f"{self.code}: {self.message}"
