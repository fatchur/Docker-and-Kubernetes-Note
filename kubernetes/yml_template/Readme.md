# Definition
- Pod: is a docker container over the node
- pod yml: is a yml for configuring the docker container over the kubernetes nodes
- deployment yml: is a yml for configuring the deployment (ex: the replicaset) for the pod.
- service yml: is a yml for configuring the service for each pod (ex: how to send request the pod port, use Loadbalancer or NodePort, etc)


# Note
- We can only use pod and service .yml for deployment, but we can't set the replicaset for the pods.
- If we use deployment and service .yml, we don't need pod yml again. The pod configuration is already included in the deployment .yml under "template" key.
- If we deploy the app in the GCP or AWS, we don't need to configure the LoadBalancer (just set the spect type as "LoadBalancer" in services .yml, then they will configuring us the loadbalancer).
- If we deploy the app for onpremise, we must deploy the nginx for our loadbalancer and set the spec type as NodePort in our services .yml.

