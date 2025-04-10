# Enable ingress (if you want public access)


```
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: metabase-ingress
  namespace: metabase
  annotations:
    cert-manager.io/cluster-issuer: letsencrypt-prod
    nginx.ingress.kubernetes.io/whitelist-source-range: IP RANGE
    nginx.ingress.kubernetes.io/proxy-connect-timeout: "300"
    nginx.ingress.kubernetes.io/proxy-read-timeout: "300"
    nginx.ingress.kubernetes.io/proxy-send-timeout: "300"

spec:
  ingressClassName: nginx
  tls:
    - hosts:
        - HOST
      secretName: metabase-ingress
  rules:
    - host: HOST
      http:
        paths:
          - pathType: Prefix
            path: /
            backend:
              service:
                name: metabase
                port:
                  number: 80
```
