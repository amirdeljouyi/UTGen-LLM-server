# LLM-server

## Project Overview

This project aims to integrate Large Language Models (LLMs) into the EvoSuite test framework. 
This repository specifically serves as the request handling component of the proposed framework.
The goal is to enhance the understandability of generated tests and assist in resolving coverage stalls, 
inspired by methods like CodaMosa. The current phase focuses on handling requests through Strawberry to interact with LLMs.

## Getting Started

### Prerequisites

- Python >= 3.8
- Pip (Python package installer)

### Installation

1. **Clone the Repository**: Since the repository is private, ensure you have access. Once public, it can be cloned as follows:
   ```
   git clone https://github.com/amirdeljouyi/LLM-server
   ```
2. **Install Dependencies**: Navigate to the project directory and install required Python packages:
   ```
   pip install strawberry requests
   ```
3. **TOKEN_SETUP**: in `main.py` change the value of `api_token` to your hugging face token:
   ```python
   api_token = "hf_XXXXXXX" # <- your hugging face token
   ```
   Replace `hf_XXXXXXX` with your actual API token.

### Running the Application

1. **Set the Environment Variables**: Ensure that your python environment is set up properly.
2. **Start the Server**: Run the following command to start the Strawberry server:
   ```
   strawberry server main
   ```

## Project Structure

### main.py
- `strawberry`: Handles GraphQL requests and responses.
- `requests`: Manages HTTP requests to the Hugging Face API.
- `Prompt`: A class for structuring the input prompt.
- `Response`: A class for structuring the LLM response.
- `Query`: Contains the logic for the GraphQL query and interaction with the LLM.

### requirements.txt
- contains the names of the dependencies of the project

### completeQuery.txt
- contains the format of the query that you can use to test the LLM Server

## Expanding the Project

The project is designed for easy expansion. When adding new features, modifying existing ones, or removing components:
1. **Update Code**: Implement the changes in the appropriate files.
2. **Document Changes**: Reflect these changes in this README, detailing new dependencies, environment variables, or usage instructions.

## Future Directions

This project is part of a larger research effort to integrate LLMs with the EvoSuite framework. Future updates will include:
- Advanced LLM interactions.
- Enhanced request handling capabilities.
- capability of having the models be locally run.
- More comprehensive integration with EvoSuite.

## Contributing

As the project is intended for open-source contribution after becoming public, we welcome contributions. Please read `CONTRIBUTING.md` (TODO) for details on our code of conduct and the process for submitting pull requests.

## License

This project is licensed under the [LICENSE] - see the LICENSE file for details.

## Contact

For any inquiries or contributions, please contact a.deljouyi@tudelft.nl

---
