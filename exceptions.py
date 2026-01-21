# exceptions.py

class CustomException(Exception):
    def __init__(self, message: str, status_code: int = 400):
        self.message = message
        self.status_code = status_code

class NotFoundException(CustomException):
    def __init__(self, message: str = "Resource not found"):
        super().__init__(message, status_code=404)

class DatabaseException(CustomException):
    def __init__(self, message: str = "Database error occurred"):
        super().__init__(message, status_code=500)