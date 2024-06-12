Feature: Request Factory

Scenario Outline: Create request with default params
    Given a request factory
    When sending a <request> to factory
    Then new object will be generated

    Examples: Request
      | request |
      | GET     |
      | POST    |
      | PATCH   |
      | DELETE  |
      | PUT     |