###
# #%L
# aiSSEMBLE::Open Inference Protocol Use Cases::FastAPI, gRPC, and Kserve Inference
# %%
# Copyright (C) 2024 Booz Allen Hamilton Inc.
# %%
# This software package is licensed under the Booz Allen Public License. All Rights Reserved.
# #L%
###
import os
from aissemble_open_inference_protocol_use_case.oip_handler import OIPHandler

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
#     # app = get_oip_fastapi(oip_handler)
#     app = get_oip_grpc(oip_handler)
#
#     app.model_load(model_name)
#     await app.start_server()


## end of FastAPI and gRPC functions definitions

# uncomment when starting kserve
## start of kserve function definition
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


def main():
    os.environ["KRAUSENING_BASE"] = "src/resources/krausening/base"
    oip_handler = OIPHandler()
    model_name = "yolo11n"

    # comment out this line when starting kserve
    # asyncio.run(start(oip_handler, model_name))

    # uncomment this line when starting kserve
    start_oip_kserve(oip_handler, model_name)
