# Install

Create a local user:

```
$ kubectl -n teleport exec -i deployment/teleport-cluster-auth -- tctl users add root --roles=editor
```

Apply github login

see: https://goteleport.com/docs/admin-guides/access-controls/sso/github-sso/#step-24-create-a-github-authentication-connector

```
$ envvar github.yaml |  kubectl -n teleport exec -i deployment/teleport-cluster-auth -- tctl create -f
```

# Auth token problems

When removing teleport namespace and want to reconfigure, adjust the hardcoded authToken in the application.yaml
