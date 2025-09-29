# KServe Deployment

This guide provides instructions for deploying the YOLO model using KServe infrastructure and running inference examples via both HTTP and gRPC protocols.

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
4. Upload data and monitor results

   **HTTP Request:**

   1. Set up port forwarding for HTTP:
      ```bash
      kubectl port-forward -n kserve-test service/kserve-model-predictor 9090:80
      ```

   2. Send HTTP request:
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

   **gRPC Request (alternative):**

   1. Set up port forwarding for gRPC:
      ```bash
      kubectl port-forward -n kserve-test service/kserve-model-predictor 8081:8081
      ```

   2. Save the following as `test_kserve_grpc.py`:
      ```python
      import asyncio
      from kserve import InferRequest, InferInput
      from kserve.inference_client import InferenceGRPCClient

      async def test_grpc():
          client = InferenceGRPCClient(
              url="localhost:8081",
              use_ssl=False,
          )

          infer_input = InferInput(
              name="sample",
              shape=[3, 1],
              datatype="BYTES",
              data=["src/resources/images/cat.png", "src/resources/images/bus.png", "https://ultralytics.com/images/bus.jpg"]
          )

          request = InferRequest(
              infer_inputs=[infer_input],
              model_name="yolo11n",
              model_version="1.0",
              request_id="1",
              from_grpc=True,
          )

          res = await client.infer(infer_request=request)
          print(res)

      if __name__ == "__main__":
          asyncio.run(test_grpc())
      ```

   3. Run the gRPC test:
      ```bash
      poetry run python test_kserve_grpc.py
      ```

# Tear Down

```bash
kubectl delete InferenceService  kserve-model -n kserve-test 
helm uninstall kserve 
helm uninstall kserve-crds 
helm uninstall cert-manager --namespace cert-manager 
helm uninstall ingress-nginx --namespace ingress-nginx
kubectl delete namespace kserve-test
```
