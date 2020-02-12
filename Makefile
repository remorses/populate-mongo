ci:
	npx bumpversions
	[ -n $DOCKER_USERNAME ] && docker login -u $DOCKER_USERNAME -p $DOCKER_PASSWORD
	docker build . -t mongoke/populate-mongo
	docker push mongoke/populate-mongo

