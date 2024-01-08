import strawberry
from qlient.http import HTTPClient, GraphQLResponse

client = HTTPClient("http://0.0.0.0:8000/graphql")


res: GraphQLResponse = client.query.prompt(
    "llmResponse",
    promptText="Person person = new Person()\nint _int = (-1950)\nInteger integer = new Integer(arg0)\nperson.setId(id)\nString firstName = person.getFirstName()\nint _int = (-384)\nInteger integer = new Integer(arg0)\nboolean equals = person.equals(obj)\nboolean equals = person.equals(obj)\nInteger integer = null\nperson.setId(id)\nperson.setId(id)\nperson.setLastName(lastName)\nString lastName = person.getLastName()\nInteger integer = new Integer(arg0)\nboolean equals = person.equals(obj)\nString firstName = person.getFirstName()\nperson.setLastName(lastName)\nString string = ''\nperson.setFirstName(firstName)\nString firstName = person.getFirstName()\nString string = ''\nperson.setFirstName(firstName)\nString lastName = person.getLastName()\nperson.setId(id)\nString lastName = person.getLastName()\nString firstName = person.getFirstName()\nperson.setId(id)\nperson.setLastName(lastName)\nString firstName = person.getFirstName()\nString firstName = person.getFirstName()\nString lastName = person.getLastName()\nString firstName = person.getFirstName()\nString lastName = person.getLastName()",
    promptType="testdata"
)

print(res.request.query)  # query film($id: ID) { film(id: $id) { id title episodeID } }
print(res.request.variables)  # {'id': 'ZmlsbXM6MQ=='}
print(res.data)  # {'film': {'id': 'ZmlsbXM6MQ==', 'title': 'A New Hope', 'episodeID': 4}}