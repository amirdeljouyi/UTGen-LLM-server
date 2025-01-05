docker exec ollama ollama pull codellama:7b-instruct

export OLLAMA_API_URL=http://ollama:11434/api/generate

./run-server.sh
