docker build -t humaneval-eval -f Dockerfile.eval .
docker run -v $(pwd):/app humaneval-eval