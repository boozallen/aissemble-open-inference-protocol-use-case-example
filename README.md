# aissemble-open-inference-protocol-use-case-example

This use case repository is to show that when wrapping the YOLO model with `aissemble-open-inference-protocol` (OIP), 
we can easily deploy to different endpoints (KServe, Fastapi, and gRPC) with minimal changes.

Each service requires a handler and a service. When using the aissemble open inference protocol, we can define one 
handler and pass to different endpoint service class.

Following deploy steps will show how easy that we can switch to use different service with minimal code changes.

- [Clone and build the project](#clone-and-build-the-project)
- [Deploy KServe](#deploy-kserve)
- [Deploy FastAPI](#deploy-fastapi)
- [Deploy gRPC](#deploy-grpc)


## Clone and build the project
```bash
git clone git@github.com:boozallen/aissemble-open-inference-protocol-use-case-example.git
```
## Deploy KServe

### Preparation

#### pyproject.toml
Due to dependency conflicts, comment out the `aissemble-open-inference-protocol-fastapi` and 
`aissemble-open-inference-protocol-grpc` dependencies and uncomment `aissemble-open-inference-protocol-kserve` as following:
```toml
# comment out both FastAPI and gRPC endpoint packages if using kserve because of dependencies conflict
#aissemble-open-inference-protocol-fastapi = "1.1.0.*"
#aissemble-open-inference-protocol-grpc = "1.1.0.*"

# uncomment to switch to kserve endpoints
aissemble-open-inference-protocol-kserve = "1.1.0.*"
```

#### main.py
1. Comment out the code for FastAPI and gRPC from line #16 to line #37 as following:
   ```python
   ## comment out to start() function when starting kserve
   ## start of FastAPI and gRPC functions definitions

   # import asyncio
   # from aissemble_open_inference_protocol_fastapi.aissemble_oip_fastapi import (
   #     AissembleOIPFastAPI,
   # )
   #
   # from aissemble_open_inference_protocol_grpc.aissemble_oip_grpc import AissembleOIPgRPC
   #
   #
   # def get_oip_fastapi(oip_handler) -> AissembleOIPFastAPI:
   #     return AissembleOIPFastAPI(oip_handler)
   #
   #
   # def get_oip_grpc(oip_handler) -> AissembleOIPgRPC:
   #     return AissembleOIPgRPC(oip_handler)
   #
   #
   # async def start(oip_handler, model_name):
   #     app = get_oip_fastapi(oip_handler)
   #     # app = get_oip_grpc(oip_handler)
   #
   #     app.model_load(model_name)
   #     await app.start_server()

   ## end of FastAPI and gRPC functions definitions
   ```

2. Uncomment KServe functions definitions from line #44 to line #56
   ```python
   ## uncomment when starting kserve
   # start of kserve function definition
   from aissemble_open_inference_protocol_kserve.aissemble_oip_kserve import (
       AissembleOIPKServe,
   )
   
   
   def start_oip_kserve(oip_handler, model_name):
       kserve = AissembleOIPKServe(
           name=model_name,
           model_handler=oip_handler,
       )
       # model needs to be loaded before server start
       kserve.load()
       kserve.start_server()
   ## end of kserve function definition
   ```

3. Comment out the FastAPI and gRPC `start` function (line #66), uncomment KServe `start` (line #69) function, as following:
   ```python
       # comment out this line when starting kserve
       # asyncio.run(start(oip_handler, model_name))
   
       # uncomment this line when starting kserve
       start_oip_kserve(oip_handler, model_name)
   
   ```
### Build
   ```bash
   mvn clean install
   ```

### Deploy
Navigate to the `deploy` folder and follow the [deploy/README](deploy/README.md) documentation.

## Deploy FastAPI

### Preparation

#### pyproject.toml
Due to dependency conflicts, comment out the `aissemble-open-inference-protocol-kserve` and uncomment
`aissemble-open-inference-protocol-grpc` and `aissemble-open-inference-protocol-fastapi` dependencies as following:
   ```toml
   # comment out both FastAPI and gRPC endpoint packages if using kserve because of dependencies conflict
   aissemble-open-inference-protocol-fastapi = "1.1.0.*"
   aissemble-open-inference-protocol-grpc = "1.1.0.*"
   
   # uncomment to switch to kserve endpoints
   # aissemble-open-inference-protocol-kserve = "1.1.0.*"
   ```

#### main.py
1. Comment out KServe functions definitions from line #44 to line #56, as following: 
   ```python
   ## uncomment when starting kserve
   # start of kserve function definition
   # from aissemble_open_inference_protocol_kserve.aissemble_oip_kserve import (
   #     AissembleOIPKServe,
   # )
   # 
   # 
   # def start_oip_kserve(oip_handler, model_name):
   #     kserve = AissembleOIPKServe(
   #         name=model_name,
   #         model_handler=oip_handler,
   #     )
   #     # model needs to be loaded before server start
   #     kserve.load()
   #     kserve.start_server()
   ## end of kserve function definition
   ```

2. Uncomment the code for FastAPI and gRPC from line #16 to line #37 as following:
   ```python
   ## comment out to start() function when starting kserve
   ## start of FastAPI and gRPC functions definitions
   
   import asyncio
   from aissemble_open_inference_protocol_fastapi.aissemble_oip_fastapi import (
       AissembleOIPFastAPI,
   )
   
   from aissemble_open_inference_protocol_grpc.aissemble_oip_grpc import AissembleOIPgRPC
   
   
   def get_oip_fastapi(oip_handler) -> AissembleOIPFastAPI:
       return AissembleOIPFastAPI(oip_handler)
   
   
   def get_oip_grpc(oip_handler) -> AissembleOIPgRPC:
       return AissembleOIPgRPC(oip_handler)
   
   
   async def start(oip_handler, model_name):
       app = get_oip_fastapi(oip_handler)
       # app = get_oip_grpc(oip_handler)
   
       app.model_load(model_name)
       await app.start_server()
   
   ## end of FastAPI and gRPC functions definitions
   ```

3. Use `AissembleOIPFastAPI` - Ensure the app (line #33) was using the `AissembleOIPFastAPI` service
   ```python
   async def start(oip_handler, model_name):
       app = get_oip_fastapi(oip_handler)
       # app = get_oip_grpc(oip_handler)
   
       app.model_load(model_name)
       await app.start_server()
   ```

4. Uncomment out the FastAPI and gRPC `start` function (line #66), comment out KServe `start` (line #69) function, as following:
   ```python
       # comment out this line when starting kserve
       asyncio.run(start(oip_handler, model_name))
   
       # uncomment this line when starting kserve
       #start_oip_kserve(oip_handler, model_name)
   
   ```
### Build
When deploy to use FastAPI, the image isn't required.
   ```bash
   mvn clean install -Pskip-docker
   ```

### Deploy

#### Deploy the Application
1. Run start server command at the project root directory.
   ```bash
   poetry run run_server
   ```
2. Upload data and monitor results
   ```bash
   curl -w "\nHTTP Code: %{http_code}\n" \
   -H 'Content-Type: application/json' \
   -d '{"id" : "2214",
        "inputs" : [{
        "name" : "sample",
        "shape" : [3],
        "datatype"  : "BYTES",
        "data" : ["src/resources/images/cat.png","src/resources/images/bus.png","https://ultralytics.com/images/bus.jpg"]
       }]}' \
   -X POST \
   http://127.0.0.1:8082/v2/models/yolo11n/infer   
   ```

## Deploy gRPC

### Preparation

#### pyproject.toml
Due to dependency conflicts, comment out the `aissemble-open-inference-protocol-kserve` and uncomment
`aissemble-open-inference-protocol-grpc` and `aissemble-open-inference-protocol-fastapi` dependencies as following:
   ```toml
   # comment out both FastAPI and gRPC endpoint packages if using kserve because of dependencies conflict
   aissemble-open-inference-protocol-fastapi = "1.1.0.*"
   aissemble-open-inference-protocol-grpc = "1.1.0.*"
   
   # uncomment to switch to kserve endpoints
   # aissemble-open-inference-protocol-kserve = "1.1.0.*"
   ```

#### main.py
2. Comment out KServe functions definitions from line #44 to line #56, as following:
   ```python
   ## uncomment when starting kserve
   # start of kserve function definition
   # from aissemble_open_inference_protocol_kserve.aissemble_oip_kserve import (
   #     AissembleOIPKServe,
   # )
   # 
   # 
   # def start_oip_kserve(oip_handler, model_name):
   #     kserve = AissembleOIPKServe(
   #         name=model_name,
   #         model_handler=oip_handler,
   #     )
   #     # model needs to be loaded before server start
   #     kserve.load()
   #     kserve.start_server()
   ## end of kserve function definition
   ```

2. Uncomment the code for FastAPI and gRPC from line #16 to line #37 as following:
   ```python
   ## comment out to start() function when starting kserve
   ## start of FastAPI and gRPC functions definitions
   
   import asyncio
   from aissemble_open_inference_protocol_fastapi.aissemble_oip_fastapi import (
       AissembleOIPFastAPI,
   )
   
   from aissemble_open_inference_protocol_grpc.aissemble_oip_grpc import AissembleOIPgRPC
   
   
   def get_oip_fastapi(oip_handler) -> AissembleOIPFastAPI:
       return AissembleOIPFastAPI(oip_handler)
   
   
   def get_oip_grpc(oip_handler) -> AissembleOIPgRPC:
       return AissembleOIPgRPC(oip_handler)
   
   
   async def start(oip_handler, model_name):
       app = get_oip_fastapi(oip_handler)
       # app = get_oip_grpc(oip_handler)
   
       app.model_load(model_name)
       await app.start_server()
   
   ## end of FastAPI and gRPC functions definitions
   ```

3. Use `AissembleOIPgRPC` - Ensure the app (line #34) was using the `AissembleOIPgRPC` service
   ```python
   async def start(oip_handler, model_name):
       #app = get_oip_fastapi(oip_handler)
       app = get_oip_grpc(oip_handler)
   
       app.model_load(model_name)
       await app.start_server()
   ```

4. Uncomment out the FastAPI and gRPC `start` function (line #66), comment out KServe `start` (line #69) function, as following:
   ```python
       # comment out this line when starting kserve
       asyncio.run(start(oip_handler, model_name))
   
       # uncomment this line when starting kserve
       #start_oip_kserve(oip_handler, model_name)
   
   ```
### Build
When deploy to use gRPC, the image isn't required.
```bash
mvn clean install -Pskip-docker
```

### Deploy

#### Deploy the Application
1. Run start server command at the project root directory.
   ```bash
   poetry run run_server
   ```
2. Upload data and monitor results
   ```bash
   grpcurl -plaintext \
   -import-path proto/ \
   -proto grpc_inference_service.proto \
   -d '{
       "model_name": "default",
       "model_version": "1.0",
       "id": "test_request",
       "inputs": [{
       "name": "input",
       "datatype": "BYTES",
       "shape": [3],
       "contents": {"bytes_contents": ["c3JjL3Jlc291cmNlcy9pbWFnZXMvY2F0LnBuZw==", "c3JjL3Jlc291cmNlcy9pbWFnZXMvYnVzLnBuZw==", "aHR0cHM6Ly91bHRyYWx5dGljcy5jb20vaW1hZ2VzL2J1cy5qcGc="]}
       }],
   "outputs": [{"name": "output"}]
   }' \
   localhost:8081 inference.GrpcInferenceService/ModelInfer   
   ```
   **Note**: gRPC requires the inputs data in encoded state so the image path has been encoded using base64 (i.e.: `echo -n "src/resources/images/cat.png" | base64`)

## Run FastAPI with authentication enabled

In this example we will enable authentication and attempt to make an inference call using a generated JWT token.  The token will include an authorized username, which will permit users to call inference.  
Part of this example is running an Authzforce service, which will be handled by the launch example code (step 4).

1. Run the pyproject.toml step from the [Deploy FastAPI section](README.md#pyprojecttoml-1), but !!!IMPORTANT!!! Stop after the pyproject.toml section.
2. Edit `src/resources/krausening/base/oip.properties` and change `auth_enabled=false` to `auth_enabled=true`
3. Run the build `mvn clean install -Pskip-docker` Note: if you get a build error, try deleting the poetry.lock file.
4. Start the aiSSEMBLE OIP FastAPI endpoint and the Authzforce server
   ```bash
   python ./src/aissemble_open_inference_protocol_use_case/launch_fastapi_auth_example.py
   ```
5. In another terminal, run the following command to generate a JWT token and store it in the `OIP_JWT` environment variable (will be used in the inference request)
   ```bash
   export OIP_JWT=$(python src/aissemble_open_inference_protocol_use_case/generate_simple_jwt.py | jq -r .jwt)
   ```
6. Once the services are up and ready (step 4), run a curl command with the JWT token stored in `OIP_JWT`
   ```bash
   curl -X "POST" -w "\nHTTP Code: %{http_code}\n" \
   "http://127.0.0.1:8000/v2/models/yolo11n/infer" \
   -H 'Content-Type: application/json' \
   -H "Authorization: Bearer $OIP_JWT" \
   -d '{"id" : "2214",
   "inputs" : [{
   "name" : "sample",
   "shape" : [3],
   "datatype"  : "BYTES",
   "data" : ["src/resources/images/cat.png","src/resources/images/bus.png","https://ultralytics.com/images/bus.jpg"]
       }]}'
   ```
7. You should get a 200 response code and an inference for the images sent.





