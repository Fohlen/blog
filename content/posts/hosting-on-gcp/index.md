---
title: "Hosting on the Google Cloud Platform"
description: "Dissecting different hosting options on GCP at varying levels of complexity."
author: "Lennard Berger"
date: "2024-12-08"
categories: [cloud,infrastructure,java,microservices]
---

Let's face it, deployment is the worst part of software engineering. In the decade I've been writing code, deployment has been the largest driver of headaches.
When Docker first debuted in 2013, many had high hopes the times of sysadmin-battles with failing hardware and complexity would finally come to an end. Well, things have improved, but many issues remain.

I recently had to deploy an application with the following requirements:

- the application was packaged in a Docker container exposing web traffic to port 8080
- the application needs hot storage, a local SSD with 10GB will do
- a public facing proxy which handles SSL certificates is necessary

Since this app already uses Firebase, launching the infrastructure on the Google Cloud comes naturally. We'll dive through several distinct architectural patterns you could deploy, if you ever find yourself in a similar situation.

# Why I couldn't use Cloud Run to begin with

I needed hot (block) storage. One can mount object storage to Cloud Run. It's simply too slow for my use case.
I imagine this isn't a crazy use case, given the amount of requests Google has gotten to support it.
Without using the most straightforward, I had to be a bit more creative.

# The cloud-native way

The correct way to deploy a containerized application is using Kubernetes. Google Cloud has the Google Kubernetes Engine, with which this is really straightforward.

In order to go down this route:

1. [upload your images to artifact registry](https://cloud.google.com/artifact-registry/docs/docker/pushing-and-pulling)
2. you'll need to [set up a GKE cluster in Autopilot mode](https://cloud.google.com/kubernetes-engine/docs/quickstarts/create-cluster)
3. create a persistent volume claim and deployment
4. [expose your deployment to the outside world using Google's Load Balancer](https://cloud.google.com/kubernetes-engine/docs/how-to/managed-certs)

I'll walk you through step three, because it is not documented in GCP itself.

Firstly, one creates a persistent volume claim (PVC):

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: pvc-my-files
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 10Gi
  storageClassName: standard-rwo
```

You [connect to your GKE](https://cloud.google.com/kubernetes-engine/docs/how-to/cluster-access-for-kubectl) and apply the PVC via `kubectl apply -f pvc.yaml`.
Next up, you can mount your PVC to your deployment:

```yaml
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp-deployment
  labels:
    app: myapp-api
spec:
  replicas: 3
  selector:
    matchLabels:
      app: myapp-api
  template:
    metadata:
      labels:
        app: myapp-api
    spec:
      volumes:
        - name: my-files
          persistentVolumeClaim:
            claimName: pvc-my-files
      containers:
        - name: myapp-api-container
          image: your_package_uri
          resources:
            requests:
              cpu: "0.5"
              memory: 512Mi
            limits:
              cpu: "1"
              memory: 1024Mi
          volumeMounts:
            - mountPath: /mnt/data
              name: my-files
          livenessProbe:
            httpGet:
              path: /health
              port: 8080
            initialDelaySeconds: 3
            periodSeconds: 3
          readinessProbe:
            httpGet:
              path: /health
              port: 8080
            initialDelaySeconds: 5
            periodSeconds: 5
```

We deploy our service via `kubectl apply -f deployment.yaml` as well. I'm making some notes of what is really important here:

- adjust the container URI
- don't forget environment variables etc.
- adjust resources according to your likes
- **DO NOT** forget to add health and readiness probes, or [you will regret it](https://stackoverflow.com/questions/72646899/getting-502-bad-gateway-with-ingress-gke-ingress-showing-warning-some-backend)
- remember the `myapp-api` label, because you need it for your service

When you are setting up the managed certificate tutorial, all you need to do is adapt the `mc-service.yaml` to correctly expose your deployment:

```yaml
apiVersion: v1
kind: Service
metadata:
  name: mc-service
spec:
  selector:
    app: myapi-api
  type: NodePort
  ports:
    - protocol: TCP
      port: 80
      targetPort: 8080
```

This setup will have your project sailing smooth ready for production. Depending on your underlying load and resource allocation, a simple REST api should easily be able to serve a few hundred thousand users using GKE in such a manner.
Notably, this setup offers a number of perks that really make it production-ready:

- Load Balancer comes with Google Cloud Armor, giving you DDoS protection and globally distributed edge endpoints
- Cloud Monitoring unifies all your log streams from everywhere, and Cloud Trace is a decent enough replacement for Sentry

Overall, this setup will probably be billed anywhere between 35-50$ monthly. This is fair-value for medium sized businesses.

However, if your service doesn't cater to 1000's of users, a 50$ monthly price point might be a little bit steep.

# Skip the Load Balancer

Another option is to skip load balancers and GKE. To do this, we'll:

1. upload our image to Artifact Registry
2. create a [persistent disk in Compute Engine](https://cloud.google.com/persistent-disk?hl=en)
3. from there on, you can simply follow the [deploy containers on Compute Engine](https://cloud.google.com/compute/docs/containers) guide
4. create a Cloud run service to use it as a reverse proxy

The last bit is actually a bit tricky and insane. Essentially, it involves three steps:

- creating a secret containg an nginx config
- creating a Cloud Run service with the `nginx:latest` image and mounting the `nginx` secret to `/etc/nginx/conf.d`, [Google actually describes how to do this](https://cloud.google.com/run/docs/internet-proxy-nginx-sidecar)
- mounting your default private virtual network to your Cloud Run service

An example `nginx.conf` might look like so:

```
server {
    # Listen at port 8080
    listen 8080;
    # Server at localhost
    server_name _;
    # Enables gzip compression to make our app faster
    gzip on;

    client_max_body_size 64M;

    #
    # Wide-open CORS config for nginx
    #

    location / {

        # Passes initial requests to port 8080 to `hello` container at port 8888
        proxy_pass   http://10.132.0.8:8080;
    }
}
```

Where `10.132.0.8` points to the internal IP of your instance. I'll note a few things about this approach as well:

- despite the documentation claiming so, you don't need a Serverless VPC connector, just connect straight to your network. If its in the same region, it is lightning fast
- you'll loose a lot of the observability compared to GKE
- some things like POST and file-upload support is notoriously hard to set up correctly, and the lack of observability doesn't help
- depending on the initial OS you select [Ops Agent](https://cloud.google.com/monitoring/api/metrics_opsagent) might be available, which will give you your container's logs. That's nice

This setup could get you started at 7$ per month (or even free in some regions), with DDoS protection.

# Rolling your own

Lastly, there's a solution that I want to point out. If you are in the early stages of your project and all you need is a quick way to get things up and running, you can roll your own PaaS.
You will need the following:

1. upload your image to Artifact Registry
2. create a persistent disk
3. [reserve an external static IP address](https://cloud.google.com/compute/docs/ip-addresses/configure-static-external-ip-address) for the VM you will create
4. create a VM of your liking and install Docker, this comes prebuilt via the [Container-Optimized OS](https://cloud.google.com/container-optimized-os/docs)
5. assign the external static IP address to your instance, and point a domain to it
6. log in your docker to Artifact Registry
7. run [caddy-docker-proxy](https://github.com/lucaslorentz/caddy-docker-proxy?tab=readme-ov-file#basic-usage-example-using-docker-compose)

This is a really low-effort solution, which will work on virtually any other VPS hoster, if you don't like GCP. However, you will loose all observability. It's like the sysadmin-days, with extra steps.

# Infrastructure is still complex

Unfortunately, infrastructure is still complex. Docker has helped, by removing the "it works on my machine" mantra. In a sense it has also added hurdles. Nowadays, every SaaS has to be _"cloud-ready"_, catering to houndreds of thousands of users.
This simply doesn't represent the reality for small to medium enterprises. One can move a lot on 2GB of RAM, and one should be able to do so as well.

Cloud Run generally does a decent job of enabling low-cost scalable infrastructure, and maybe in a few years they will also support my use case.
For the time being, the other strategies work just as well (albeit with caveats).
