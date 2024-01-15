import re

# java_string = """public Class Hello {
# @Test
# public void testLastName_whenPersonIsNull_shouldReturnNull() {
#     // Arrange
#     Person person = null;
#
#     // Act
#     String lastName = person.getLastName();
#
#     // Assert
#     assertNull(lastName);
# }
# }"""


# java_string = """public void testGetFirstName() {
#     // Create a new Person object and retrieve its first name
#     Person person = new Person();
#     String actualFirstname = person.getFirstName();
#
#     // Assert that the first name is null
#     assertNull(actualFirstname);
# }"""

java_string = """/**
 * Tests that the first name of a person is null when a new person is created.
 * This test demonstrates the use of assertNull to check that a value is null.
 */
public void testFirstNameIsNull() {
    Person person = new Person();
    String firstName = person.getFirstName();
    // Assert that the first name is null
    assertNull(firstName);
}"""


keywords = ["import", "@Test", "public", "void", "}", "Class"]

java_string_split = java_string.split("\n")

had_keyword = False

while True:
    for k in keywords:
        if (k in java_string_split[0] or
                len(java_string_split[0].strip()) == 0 or
                java_string_split[0].strip()[0] == "*" or
                java_string_split[0][0:2] == "/*" or
                java_string_split[0][0:2] == "*/"):
            java_string_split.remove(java_string_split[0])
            had_keyword = True
            break

    if had_keyword:
        had_keyword = False
        continue

    else:
        break

while True:
    for k in keywords:
        if (k in java_string_split[len(java_string_split) - 1] or
                len(java_string_split[len(java_string_split) - 1].strip()) == 0 or
                java_string_split[len(java_string_split) - 1].strip()[0] == "*" or
                java_string_split[len(java_string_split) - 1][0:2] == "/*" or
                java_string_split[len(java_string_split) - 1][0:2] == "*/"):
            java_string_split.remove(java_string_split[len(java_string_split) - 1])
            had_keyword = True
            break

    if had_keyword:
        had_keyword = False
        continue

    else:
        break

finalized_code = str.join("\n", [x.strip() for x in java_string_split])
print(finalized_code)