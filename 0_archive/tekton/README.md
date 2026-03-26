# Tekton

## Install

```shell
kubectl apply --filename https://storage.googleapis.com/tekton-releases/pipeline/latest/release.yaml
```

dashboard

```shell
kubectl apply --filename https://storage.googleapis.com/tekton-releases/dashboard/latest/release-full.yaml
```

## Access the dashboard

```shell
kubectl port-forward -n tekton-pipelines service/tekton-dashboard 9097:9097
```
