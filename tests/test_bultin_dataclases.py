import json
from dataclasses import dataclass, asdict

@dataclass
class ExampleModel:
    string: str
    number: int
    email: str
    optional: str = None

def test_correct_datamodel():
    """ Expeting no errors in this test """
    test = ExampleModel(string='foobar', number=123, email='example@example.com')
    print(json.dumps(asdict(test), indent=4))

