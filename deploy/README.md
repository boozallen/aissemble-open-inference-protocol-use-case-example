# Infrastructure

## Building Helm charts

Run the following to install the helm dependent charts:

```bash
helm dependency build ./infrastructure/cert-manager/
helm dependency build ./infrastructure/kserve-crds/
helm dependency build ./infrastructure/kserve/
helm dependency build ./infrastructure/nginx/
```

## Install Services

```bash
helm install kserve-crds ./infrastructure/kserve-crds/
helm install ingress-nginx ./infrastructure/nginx/ --namespace ingress-nginx --create-namespace
helm install cert-manager ./infrastructure/cert-manager/ --create-namespace --namespace cert-manager
helm install kserve ./infrastructure/kserve/
```

# Deploy the Application

1. Create kserve test namespace
    ```bash
    kubectl create namespace kserve-test
    ```
2. Deploy kserve application
   ```bash
   kubectl apply -n kserve-test -f ./apps/inference-services/templates/inference-service.yaml
   ```
3. Wait for the KServe predictor pod to show "STATUS: Running" and "READY: 1/1" before uploading data for inference.
4. port forward
   ```bash
   kubectl port-forward -n kserve-test service/kserve-model-predictor 9090:80
   ```
3. Upload data and monitor results
   ```bash
   curl --request POST \
   -H "Content-Type: application/json" \
   --url http://localhost:9090/v2/models/yolo11n/infer \
   --data '{
   "id" : "1",
   "inputs" : [
     {
       "name" : "sample",
       "shape" : [3,1],
       "datatype"  : "BYTES",
       "data" : ["src/resources/images/cat.png","src/resources/images/bus.png","https://ultralytics.com/images/bus.jpg"]
     }
    ]
   }'   
   ```

# Tear Down

```bash
kubectl delete InferenceService  kserve-model -n kserve-test 
helm uninstall kserve 
helm uninstall kserve-crds 
helm uninstall cert-manager --namespace cert-manager 
helm uninstall ingress-nginx --namespace ingress-nginx
```
