docker build -t base -f dockerfiles/base-dockerfile .
docker build -t source -f dockerfiles/source-dockerfile .
docker build -t java -f dockerfiles/java-dockerfile .