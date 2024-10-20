<div align="center">

# Atrium

![Image of an atrium created by chatgpt](.github/images/bg.webp)

> My kubernetes infrastructure built in public

This repository contains my personal Kubernetes cluster setup (on hetzner), and is highly opinionated.

</div>

## Why creating this repository

- build in public
- no vendor lock in
- be able to move to other providers or self host

## Installing or upgrading RKE2

```shell
curl -sfL https://get.rke2.io | sh -

```

## To sync or not to sync

Some applications are synced via ArgoCD and some are not. When synced, it means that ArgoCD will check this github repository to validate and update to the desired state.
to sync an application, we require to write atleast 2 sources see [https://argo-cd.readthedocs.io/en/latest/user-guide/multiple_sources/#helm-value-files-from-external-git-repository](https://argo-cd.readthedocs.io/en/latest/user-guide/multiple_sources/#helm-value-files-from-external-git-repository)

## Secrets

All secrets are stored in a SealedSecrets

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
