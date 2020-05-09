# docker

`docker build -t eduardofcbg/openwhisk-pandoc:latest .`

`docker push eduardofcbg/openwhisk-pandoc:latest`

# undeploy

`ibmcloud fn undeploy --manifest manifest.yaml`

# deploy

Choose eu-gb region

`ibmcloud login -r eu-gb`

`ibmcloud target -g default`

`ibmcloud target --cf`

`ibmcloud fn deploy --manifest manifest.yaml`

`ibmcloud fn api list`
