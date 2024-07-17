AWS_DEFAULT_REGION=us-east-1
REGISTRY="ecr-registry"

aws ecr get-login-password \
        --region ${AWS_DEFAULT_REGION} | docker login \
        --username AWS \
        --password-stdin ${REGISTRY}

REPOSITORY="repository/keda/keda-restart"
REGISTRY_ADDR=${REGISTRY}/${REPOSITORY}
TAG=0.1

docker buildx build \
  --no-cache \
  --force-rm \
  -f Dockerfile -t ${REGISTRY_ADDR}:${TAG} .
docker push ${REGISTRY_ADDR}:${TAG}
docker rmi ${REGISTRY_ADDR}:${TAG}
