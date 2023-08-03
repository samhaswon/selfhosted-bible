build-and-push:
	docker buildx build --push --platform linux/arm/v6,linux/arm/v7,linux/arm64/v8,linux/amd64,linux/386 --tag samhaswon/self-hosted-bible:latest .
