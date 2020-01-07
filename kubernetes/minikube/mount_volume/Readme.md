## NOTE
- Basic emptyDir
- Sharing emptyDir for Multiple Pods
- PersistentVolume and PersistentVolumeClaim 


### A. Basic emptyDir 
#### A.1 Yml File 
```
apiVersion: v1
kind: Pod
metadata:
  name: myvolumes-pod
spec:
  containers:
  - image: alpine
    imagePullPolicy: IfNotPresent
    name: myvolumes-container
    
    command: [    'sh', '-c', 'sleep 3600']
    
    volumeMounts:
    - mountPath: /demo
      name: demo-volume
  volumes:
  - name: demo-volume
    emptyDir: {}
```

#### A.2 Checking The Volume
```
kubectl exec myvolumes-pod -it -- /bin/sh
# find the /demo over there
```


### B. Sharing emptyDir for Multiple Pods
#### B.1 Yml File 
```
apiVersion: v1
kind: Pod
metadata:
  name: myvolumes-pod
spec:
  containers:
  - image: alpine
    imagePullPolicy: IfNotPresent
    name: myvolumes-container-1
    command: ['sh', '-c', 'sleep 3600']
    
    volumeMounts:
    - mountPath: /demo1
      name: demo-volume

  - image: alpine
    imagePullPolicy: IfNotPresent
    name: myvolumes-container-2
    command: ['sh', '-c', 'sleep 3600']
    
    volumeMounts:
    - mountPath: /demo2
      name: demo-volume

  - image: alpine
    imagePullPolicy: IfNotPresent
    name: myvolumes-container-3
    command: ['sh', '-c', 'sleep 3600']
    
    volumeMounts:
    - mountPath: /demo3
      name: demo-volume

  volumes:
  - name: demo-volume
    emptyDir: {}
```

#### B.2 Checking the Volume
```
kubectl exec myvolumes-pod -c myvolumes-container-1 -it -- /bin/sh
``` 

#### B.2 Note
```
If we mouted two or more container in same path, let say '/demo1', the update form a container is readble from others (sharing)
```














