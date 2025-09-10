# export VAULT_ADDR=XXX

# ==========================================================
# FOLLOWING SHOULD BE DONE ONLY ONCE TO CONFIGURE KUBE AUTH
# ==========================================================


# Enable kubernetes in vault (should be done only once)
# vault auth enable kubernetes

# NAMESPACE=tooling
# SECRET=external-secrets-sa-secret
#
# # Get the correct env vars
# TOKEN_REVIEW_JWT=$(kubectl -n $NAMESPACE get secret $SECRET -o jsonpath={.data.token} | base64 -d)
# KUBE_CA_CERT=$(kubectl config view --raw --minify --flatten -o jsonpath='{.clusters[].cluster.certificate-authority-data}' | base64 --decode)
# KUBE_HOST=$(kubectl config view --raw --minify --flatten --output='jsonpath={.clusters[].cluster.server}')
#
# echo TOKEN:
# echo $TOKEN_REVIEW_JWT
# echo TOKEN CA CERT:
# echo $KUBE_CA_CERT
# echo KUBE HOST:
# echo $KUBE_HOST
#
# # Write the token to vault, so that the token is allowed
# # This is in essence the master key
# vault write auth/kubernetes/config token_reviewer_jwt="$TOKEN_REVIEW_JWT" kubernetes_host="$KUBE_HOST" kubernetes_ca_cert="$KUBE_CA_CERT"

# ==========================================================
# TOOLING ACCESS
# ==========================================================

NAMESPACES=tooling,applications

# Create a policy
vault policy write external-secrets-policy - <<EOF
path "kubernetes/data/*" {
  capabilities = ["read"]
}
path "kubernetes/metadata/*" {
  capabilities = ["list", "read"]
}
EOF

# Create a Kubernetes auth role
vault write auth/kubernetes/role/external-secrets-vault-role \
    bound_service_account_names=external-secrets-sa \
    bound_service_account_namespaces=$NAMESPACES \
    policies=external-secrets-policy \
    ttl=24h
