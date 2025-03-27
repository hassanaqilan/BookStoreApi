class BookStoreApiError(Exception):
    """
    Base Exception for all the errors
    """

    def __init__(
        self, message: str = "Service is unavailable", name: str = "BookStore"
    ):
        self.message = message
        self.name = name
        super().__init__(self.message, self.name)


class ServiceError(BookStoreApiError):
    """database or third party error"""

    pass


class BookNotFoundError(BookStoreApiError):
    """What is this book bruh"""

    pass


class BookAlreadyBorrowed(BookStoreApiError):
    """za book is borrowed my guy"""
    pass


class MemberNotFound(BookStoreApiError):
    """za book is borrowed my guy"""
    pass


class ErrorInDBC(BookStoreApiError):
    """Error in database"""
    pass
