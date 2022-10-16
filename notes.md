
To Do:

Read Queue, return number of items in Queue


Set config params from Env Vars?


populate dropdown from json obtained by scryfall



## Running on TAP

```bash
tanzu apps workload create python-pipenv \
  --git-repo https://github.com/benwilcock/python-pipenv \
  --git-branch main \
  --type web \
  --label app.kubernetes.io/part-of=python-pipenv \
  --label apps.tanzu.vmware.com/has-tests=true \
  --param-yaml testing_pipeline_matching_labels='{"apps.tanzu.vmware.com/pipeline":"test", "apps.tanzu.vmware.com/language":"python"}' \
  --annotation autoscaling.knative.dev/minScale=1 \
  --namespace default \
  --tail \
  --yes
```