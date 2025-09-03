# export VAULT_ADDR=XXX

NAMESPACE=applications
SECRET=external-secrets-sa-secret

# Enable kubernetes in vault
# vault auth enable kubernetes

# Get the correct env vars
TOKEN_REVIEW_JWT=$(kubectl -n $NAMESPACE get secret $SECRET -o jsonpath={.data.token} | base64 -d)
KUBE_CA_CERT=$(kubectl config view --raw --minify --flatten -o jsonpath='{.clusters[].cluster.certificate-authority-data}' | base64 --decode)
KUBE_HOST=$(kubectl config view --raw --minify --flatten --output='jsonpath={.clusters[].cluster.server}')

echo TOKEN:
echo $TOKEN_REVIEW_JWT
echo TOKEN CA CERT:
echo $KUBE_CA_CERT
echo KUBE HOST:
echo $KUBE_HOST

# Write the token to vault, so that the token is allowed
vault write auth/kubernetes/config token_reviewer_jwt="$TOKEN_REVIEW_JWT" kubernetes_host="$KUBE_HOST" kubernetes_ca_cert="$KUBE_CA_CERT"

# Create a policy for external-secrets
vault policy write external-secrets-policy - <<EOF
path "applications/data/*" {
  capabilities = ["read"]
}
path "applications/metadata/*" {
  capabilities = ["list", "read"]
}
EOF

# Create a Kubernetes auth role
vault delete auth/kubernetes/role/external-secrets-vault-role
vault write auth/kubernetes/role/external-secrets-vault-role \
    bound_service_account_names=external-secrets-sa \
    bound_service_account_namespaces=$NAMESPACE \
    policies=external-secrets-policy \
    ttl=24h
