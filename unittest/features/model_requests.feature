Feature: Model Request

Scenario Outline: Init the Model with data
    Given a request Model
    When init <key> <value> to object
    Then verify <key> <value> created

    Examples: Hands
      | key    | value             |
      | token  | hello             |
      | header | {'json': 'hello'} |
      | method | post              |
      | body   | {'json': 'hello'} |
      | files  | ('hello','world') |