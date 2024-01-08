
# Usage: bash deploy_image.sh local-docker-image:tag cloud-docker-image:tag

# Check if all arguments are provided
if [ "$#" -ne 2 ]; then
  echo "Usage: $0 docker_name docker_tag"
  exit 1
fi

# Chekck gsutil installed
if ! command -v gsutil &> /dev/null ; then
    echo "Error: gsutil could not be found. Please install gsutil (https://cloud.google.com/sdk/docs/downloads-interactive#linux-mac)."
    exit 1
fi


# Chekck gsutil installed
if ! command -v docker &> /dev/null ; then
    echo "Error: docker could not be found. Please install docker."
    exit 1
fi

# Create local variables
docker_name="$1"
docker_tag="$2"

# Build
docker build -f Dockerfile -t "$docker_name" .
echo INFO: docker image built "$docker_name"
# Tag
docker tag "$docker_name" "$docker_tag"
echo INFO: docker image tagged
# Push
docker push "$docker_tag"
echo INFO: docker image pushed "$docker_tag"