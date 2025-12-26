# Scale Streamlit Applications With Kubernetes :chart_with_upwards_trend:
Streamlit uses WebSockets for real-time, two-way communication between the browser and the server. Without configuring session affinity, inbound traffic may be redistributed across different backend replicas. This leads to broken WebSocket connections and the loss of in-memory session state.

Maintaining this persistence is critical because Streamlit stores user data and application progress locally on the server; if the connection shifts to a new instance, the user's session will immediately reset, resulting in a fragmented and unreliable user experience.

## Managing WebSocket Persistence When Scaling With Kubernetes :electric_plug:
To support the stateful nature of Streamlit during scaling, Kubernetes orchestrates Horizontal Pod Autoscaling ([HPA](https://kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale-walkthrough/)) to manage fluctuating demand while leveraging Ingress Controllers to enforce the sticky sessions essential for stateful stability.

Sticky sessions ensure session persistence by pinning each user to a specific backend pod, preventing the data loss and connection resets that occur when stateful Streamlit traffic is redistributed.


## Sticky Session Configuration :hammer_and_wrench:
To achieve session persistence, configure cookie-based affinity _(I am using Traefik load balancer in my raspberry pi k3s cluster)_:
```yaml
apiVersion: traefik.io/v1alpha1
kind: TraefikService
metadata:
  name: sticky-session-traefik-service
spec:
  weighted:
    sticky:
      cookie:
        name: lvl1 # Service-level cookie
    services:
      - name: streamlit-service
        port: 80
        weight: 10
        sticky:
          cookie:
            name: lvl2 # Pod-level stickiness
            httpOnly: true
            secure: false # Send over HTTP/HTTPS
            sameSite: strict # Cookie sent in first-party context, prevents CSRF

---
apiVersion: traefik.io/v1alpha1
kind: IngressRoute
metadata:
  name: traefik-ingress-route
spec:
  entryPoints:
  - web
  routes:
  # NOTE: Use IP address of Traefik load balancer
  - match: Host(`scale-streamlit-app.{IP_ADDRESS}.nip.io`) # Use *.nip.io DNS wildcard to route traffic
    kind: Rule
    services:
    - name: sticky-session-traefik-service
      kind: TraefikService
```

## Quickstart :page_facing_up:
1. Retrieve the IP address of your Traefik Load Balancer and replace the written IP address in `traefik-ingress.yml` with your actual IP under `IngressRoute` manifest.
    - To retrieve IP, run `kubectl get svc -A` and look for `LoadBalancer` Type and the value under `EXTERNAL-IP` column.
    - e.g. If your IP is `192.168.1.50`, your match rule should look like this:
`Host(scale-streamlit-app.192.168.1.50.nip.io)`
2. Deploy all k8s resources to your cluster:
```bash
kubectl apply -k k8s/
```
3. In a browser, verify that the application is accessible at:
`http://scale-streamlit-app.{YOUR_IP}.nip.io`
4. Refresh the application a few times to trigger autoscaling and notice how your session remains on the original pod.
    - To get all pod logs: `kubectl logs -l app=streamlit --prefix`


### References
- [Traefik Sticky Sessions](https://github.com/traefik-workshops/traefik-workshop-2/blob/main/05-sticky-session/00-traefik-service.yaml)
- [Streamlit WebSockets and session management](https://docs.streamlit.io/develop/concepts/architecture/architecture)