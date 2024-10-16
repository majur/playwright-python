Feature: User registration and messaging

  Scenario: Register two users and send a private message
    Given I navigate to the user registration page
    When I register a new user with random data
    And I register a second user with random data
    And I log in as the first user
    And I send a private message to the second user
    Then I log in as the second user
    And I verify that the private message was received
