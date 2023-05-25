
To Do:

Read Queue, return number of items in Queue


Set config params from Env Vars?


populate dropdown from json obtained by scryfall



## Running on TAP

```
tanzu apps workload create python-mtg-queue-fetcher \
  --git-repo https://github.com/BrianRagazzi/python-mtg-queue-fetcher \
  --git-branch main \
  --type web \
  --label app.kubernetes.io/part-of=python-mtg-queue-fetcher \
  --label apps.tanzu.vmware.com/has-tests=false \
  --annotation autoscaling.knative.dev/minScale=1 \
  --namespace default \
  --tail \
  --env "RABBITMQ_HOST=192.168.103.10" \
  --env "RABBITMQ_QUEUE=cards" \
  --env "RABBITMQ_USERNAME=myuser" \
  --env "RABBITMQ_PASSWORD=mypass" \
  --yes
```


```
tanzu apps workload update python-mtg-queue-fetcher \
  --git-repo https://github.com/BrianRagazzi/python-mtg-queue-fetcher \
  --git-branch main \
  --type web \
  --label app.kubernetes.io/part-of=python-mtg-queue-fetcher \
  --label apps.tanzu.vmware.com/has-tests=false \
  --annotation autoscaling.knative.dev/minScale=1 \
  --namespace default \
  --tail \
  --env "RABBITMQ_HOST=192.168.103.27" \
  --env "RABBITMQ_QUEUE=cards" \
  --env "RABBITMQ_USERNAME=myuser" \
  --env "RABBITMQ_PASSWORD=mypass" \
  --env "S3SERVER"="minio.lab.brianragazzi.com" \
  --env "S3BUCKET"="cardimages" \
  --env "S3ACCESSKEY"="MCACCESS" \
  --env "S3SECRETKEY"="MCSECRET" \
  --yes
```
