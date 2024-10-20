# Usage

For a Deployment called foo have a ConfigMap called foo-configmap or Secret called foo-secret or both. Then add your annotation (by default reloader.stakater.com/auto) to main metadata of your Deployment

```
kind: Deployment
metadata:
  annotations:
    reloader.stakater.com/auto: "true"
spec:
  template:
    metadata:
```
