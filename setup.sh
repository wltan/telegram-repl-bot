docker build -t base -f dockerfiles/base-dockerfile .
docker build -t source-repl -f dockerfiles/source-repl-dockerfile .
docker build -t java -f dockerfiles/java-dockerfile .
docker build -t java-repl -f dockerfiles/java-repl-dockerfile .
docker build -t python -f dockerfiles/python-dockerfile .
docker build -t python-repl -f dockerfiles/python-repl-dockerfile .
docker build -t c-repl -f dockerfiles/c-repl-dockerfile .
docker build -t main -f dockerfiles/main-dockerfile .
