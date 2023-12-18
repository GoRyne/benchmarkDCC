
# Use this command at this directory
docker build -t yourImageName -f Dockerfile .
docker run -it --net=host --gpus all --name containerName imageName


# Use this command in container
sh /benchmarkDCC/linear_road/generator.sh