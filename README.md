<div align="center">

# Atrium

![Image of an atrium created by chatgpt](.github/images/bg.webp)

> My kubernetes infrastructure built in public

This repository contains my personal Kubernetes cluster setup (on hetzner), and is highly opinionated.

</div>

## Goal

- Make it as easy as possible to deploy to your own Kubernetes cluster.
- All infrastructure is written in this Git folder, should be easy to migrate to a new server.
- Have a self sustained CI/CD with secrets system.
- Metrics, Logs, BI should work out of the box.
- goteleport act as your jump point.

## Why creating this repository

- build in public
- no vendor lock in
- be able to move to other providers or self host

## Installing or upgrading RKE2

```shell
curl -sfL https://get.rke2.io | sh -
```

## To sync or not to sync (ArgoCD)

Some applications are synced via ArgoCD and some are not. When synced, it means that ArgoCD will check this github repository to validate and update to the desired state.
to sync an application, we require to write atleast 2 sources see [https://argo-cd.readthedocs.io/en/latest/user-guide/multiple_sources/#helm-value-files-from-external-git-repository](https://argo-cd.readthedocs.io/en/latest/user-guide/multiple_sources/#helm-value-files-from-external-git-repository)

## Secrets

All secrets are stored in a `.env` file for not synced applications ([envvar](https://github.com/sevaho/scripts/blob/master/envvar) is used to load the ENV variables). When an application should be synced via ArgoCD, [SealedSecrets](https://github.com/bitnami-labs/sealed-secrets)

## What's in this repository?

### Charts

Custom helm charts, makes it easier to work with to deploy self written applications.

### Deployments

All applications that are being deployed to kuberentes (via ArgoCD).

### infrastructure-as-code

Infrastructure as code written with Pulumi

### server-configuration-automation

> Still looking for a good name for this folder...

This contains the ansible configuration for underlying servers.

## TODO

- Grafana dashboards (in git)
- Quickwit logs be able to see em in 1 view
- Fix clickhouse deployment -> now there is a memory issue
- .env.example
- Add alertmanager and be able to get notification when new release is out
- Be able to send mails / telegram as notification (alertmanager)
- Have a good CI/CD flow (tekton, woodpecker, kargo, ...)
- Be able to see releasenotes of new versions?
test
