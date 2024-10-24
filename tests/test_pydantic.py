from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional
import pytest


# More on pydantic: https://docs.pydantic.dev/latest/
# https://www.youtube.com/watch?v=502XOB0u8OY

class ExampleModel(BaseModel):
    string: str = Field(..., min_length=3, max_length=30)
    number: int
    email: EmailStr # Builtin validator for email from pydantic[email]
    altEmail: Optional[str] = Field(None, pattern=r'^\S+@\S+\.\S+$')
    zip_code: Optional[str] = Field(None, pattern=r'^\d{2}-\d{3}$')  # regex pattern for 00-000
    optional: str = None
    optional2: Optional[str] = Field(None,
                                     examples=['example1', 'example2'],
                                     description='Optional field with examples',
                                     frozen=True
                                    )

    @field_validator('zip_code')
    @classmethod
    def validate_zip_code(cls, value):
        if value is None:
            return value
        # Optional: further custom validation if needed
        return value


def test_correct_datamodel():
    test = ExampleModel(string='foobar', number=123, email='example@example.com')
    print(test.model_dump_json(indent=4))
    assert test.string == 'foobar'
    assert test.number == 123
    assert test.email == 'example@example.com'
    assert test.optional is None
    assert test.optional2 is None

# test = ExampleModel(string='foo', number=123, email='whatever')
def test_invalid_example_model():
    """ Expeting validation error in this test """
    try:
        test = ExampleModel(string='foo', number=123, email='whatever')
    # except Exception as e:
    except ValueError as e:
        # This already prooves the ValidationError is raised
        # assert str(e) == '3 validation errors for ExampleModel\nstring\n  ensure this value has at least 3 characters (type=value_error)\nemail\n  value is not a valid email address (type=value_error)\naltEmail\n  field required (type=value_error)'
        # assert True, 'Validation error raised'
        assert "value is not a valid email address" in str(e)
    else:
        assert False, "Expected ValueError to be raised"



# integer_validation_test = ExampleModel(string='foo', number='123', email='whatever')

