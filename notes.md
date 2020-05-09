# build

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

# try

```
curl --request POST \
  --url $API_URL \
  --header 'accept: application/pdf' \
  --header 'content-type: text/plain' \
  --header 'pandoc-options: -f markdown -t pdf ' \
  --data '---
title: Test
...

This is a test
'
```
