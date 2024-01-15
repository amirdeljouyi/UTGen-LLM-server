import json

from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport
import asyncio

# Select the endpoint
transport = AIOHTTPTransport(url="http://127.0.0.1:8000/graphql")

# Create Graphql client
client = Client(transport=transport, fetch_schema_from_transport=True, execute_timeout=None)

num = 1
test_code = """Person person = new Person();
String firstName = person.getFirstName();
assertNull(firstName);"""

codes = [
    """Person person = new Person();\nString firstName = person.getFirstName();\nassertNull(firstName);""",
    """Person person = new Person();\nString lastName = "Johnson";\nperson.setLastName(lastName);\nString lastName = person.getLastName();\nassertEquals("Johnson", lastName);""",
    """Person person = new Person();\nString lastName = person.getLastName();\nassertNull(lastName);""",
    """Person person = new Person();\nString firstName = "Mary";\nperson.setFirstName(firstName);\nString firstName = person.getFirstName();\nassertEquals("Mary", firstName);"""
]


async def get_llm_response(num_test, code):
    print(f"Test {num_test} was :")
    print(code)

    query_string = """{
        prompt(prompt: {
            promptText: """ + json.dumps(code) + """,
            promptType: "finalTestImprovement"
        }){
            llmResponse
        }
        }"""

    # Make Query
    query = gql(
        query_string
    )

    res = await client.execute_async(query)

    # Execute
    print("\n\nThe improved test is:")
    print(res['prompt']['llmResponse'])
    print("\n\n\n==========================================\n\n\n")


for i in range(len(codes)):
    asyncio.run(get_llm_response(i+1, codes[i]))
