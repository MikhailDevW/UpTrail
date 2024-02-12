# import re
from pydantic import BaseModel, validator


class Track(BaseModel):
    title: str
    description: str
    distance: float

    @validator("distance")
    @classmethod
    def validate_distance(cls, value):
        if value < 0:
            raise ValueError("must be > 0")
        return value

    # @validator("email")
    # @classmethod
    # def validate_email(cls, value):
    #     if not bool(re.fullmatch(r'[\w.-]+@[\w-]+\.[\w.]+', value)):
    #         raise ValueError("Email is invalid")
    #     return value

    # @validator("password")
    # @classmethod
    # def validate_password(cls, value):
    #     password_length = len(value)
    #     if password_length < 8 or password_length > 16:
    #         raise ValueError(
    # "The password must be between 8 and 16 characters long")
    #     return value

# # Valid User
# valid_user = {
#     'username': 'test_name',
#     'age': 20,
#     'email': 'name@test.gr',
#     'password': '123456789'
# }

# # Invalid User
# invalid_user = {
#     'username': 'test_name',
#     'age': 16,
#     'email': 'name_test.gr',
#     'password': '1234'
# }

# try:
#     valid_result = Track(**valid_user)
#     print(valid_result)
#     # Valid Output: username='test_name' age=20 email='name@test.gr'
    #  password='123456789'
#     invalid_result = Track(**invalid_user)
# except ValueError as e:
#     print(e.errors())
#     # Invalid Output:
#     [
#       {
#           "loc":"(""age",")",
#           "msg":"User must be adult",
#           "type":"value_error"
#       },
#       {
#           "loc":"(""email",")",
#           "msg":"Email is invalid",
#           "type":"value_error"
#       },
#       {
#           "loc":"(""password",")",
#           "msg":"The password must be between 8 and 16 characters long",
#           "type":"value_error"
#       }
#     ]
