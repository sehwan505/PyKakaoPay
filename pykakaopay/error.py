class KakaoPayException(Exception):
    """Basic Exception"""


class ArgumentError(KakaoPayException):
    """Exception For Wrong Argument"""


class AuthenticationErro(KakaoPayException):
    """Exception For Authentication Fail"""


class InternalServerError(KakaoPayException):
    """Exception For Internal Server Error"""

    def __init__(self, *args: object) -> None:
        super().__init__("Server Error, Please report error to Developer Forum")
