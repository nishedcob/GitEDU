
echo "Localizing compiled Docker Images..."
echo "===================================="
echo ""

echo "Global Variables"
echo "----------------"

echo "Programming Languages..."
DOCKER_LANG_ARRAY=( shell python3 postgresql )
echo "Language Array: " $DOCKER_LANG_ARRAY
#for i in "${DOCKER_LANG_ARRAY[@]}"; do echo $i; done

sleep 2s

echo "Operating Systems..."
DOCKER_TAGS_ARRAY=( debian-stretch alpine-3.6 )
echo "Tags Array: " $DOCKER_TAGS_ARRAY
#for j in "${DOCKER_TAGS_ARRAY[@]}"; do echo $j; done

sleep 2s

DOCKER_NAMESPACE=nishedcob
echo "Namespace: " $DOCKER_NAMESPACE

sleep 1s

DOCKER_IMAGE_TEMPLATE_PREFIX=
echo "Template Prefix: " $DOCKER_IMAGE_TEMPLATE_PREFIX
DOCKER_IMAGE_TEMPLATE_SUFFIX=-executor
echo "Template Suffix: " $DOCKER_IMAGE_TEMPLATE_SUFFIX

sleep 2s

DOCKER_REMOTE_REGISTRY=10.10.10.1:5000
#DOCKER_REMOTE_REGISTRY=10.0.0.1:5000
#DOCKER_REMOTE_REGISTRY=localhost:5000
echo "Remote Registry: " $DOCKER_REMOTE_REGISTRY
DOCKER_REMOTE_REPOSITORY=nishedcob
echo "Remote Repository: " $DOCKER_REMOTE_REPOSITORY

sleep 2s

echo ""
echo "Local Variables and Executions:"
echo "-------------------------------"

for i in "${DOCKER_LANG_ARRAY[@]}"; do
	echo ""
	DOCKER_PROG_LANG=$i
	echo "PROGRAMING LANGUAGE = "$DOCKER_PROG_LANG

	sleep 1s

	DOCKER_IMAGE_NAME=$DOCKER_IMAGE_TEMPLATE_PREFIX$DOCKER_PROG_LANG$DOCKER_IMAGE_TEMPLATE_SUFFIX
	echo "IMAGE_NAME = " $DOCKER_IMAGE_NAME

	sleep 1s

	DOCKER_LOCAL_IMAGE=$DOCKER_NAMESPACE/$DOCKER_IMAGE_NAME
	echo "LOCAL_IMAGE = " $DOCKER_LOCAL_IMAGE

	sleep 1s

	DOCKER_REMOTE_IMAGE=$DOCKER_REMOTE_REGISTRY/$DOCKER_IMAGE_NAME
	echo "REMOTE_IMAGE = " $DOCKER_REMOTE_IMAGE
	DOCKER_REMOTE_REPOSITORY_IMAGE=$DOCKER_REMOTE_REGISTRY/$DOCKER_REMOTE_REPOSITORY/$DOCKER_IMAGE_NAME
	echo "REMOTE_IMAGE = " $DOCKER_REMOTE_REPOSITORY_IMAGE

	sleep 1s

	for j in "${DOCKER_TAGS_ARRAY[@]}"; do
		DOCKER_IMAGE_TAG=$j
		echo "TAG = " $DOCKER_IMAGE_TAG

		sleep 1s

		DOCKER_LOCAL_TAGGED_IMAGE=$DOCKER_LOCAL_IMAGE:$DOCKER_IMAGE_TAG
		echo "LOCAL_TAGED_IMAGE = " $DOCKER_LOCAL_TAGGED_IMAGE

		sleep 1s

		DOCKER_REMOTE_TAGGED_IMAGE=$DOCKER_REMOTE_IMAGE:$DOCKER_IMAGE_TAG
		echo "REMOTE_TAGED_IMAGE = " $DOCKER_REMOTE_TAGGED_IMAGE
		DOCKER_REMOTE_TAGGED_REPOSITORY_IMAGE=$DOCKER_REMOTE_REPOSITORY_IMAGE:$DOCKER_IMAGE_TAG
		echo "REMOTE_TAGED_REPOSITORY_IMAGE = " $DOCKER_REMOTE_TAGGED_REPOSITORY_IMAGE

		echo ""
		echo "Docker Operations..."
		DOCKER_TAG_CMD="docker tag $DOCKER_LOCAL_TAGGED_IMAGE $DOCKER_REMOTE_TAGGED_REPOSITORY_IMAGE"
		echo $DOCKER_TAG_CMD
		eval $DOCKER_TAG_CMD
		DOCKER_PUSH_CMD="docker push $DOCKER_REMOTE_TAGGED_REPOSITORY_IMAGE"
		echo $DOCKER_PUSH_CMD
		eval $DOCKER_PUSH_CMD
		echo ""
	done;
done;

