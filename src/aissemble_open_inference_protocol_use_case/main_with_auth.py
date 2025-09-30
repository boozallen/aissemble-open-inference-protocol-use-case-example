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
from aissemble_open_inference_protocol_grpc.aissemble_oip_grpc import AissembleOIPgRPC
from aissemble_open_inference_protocol_fastapi.aissemble_oip_fastapi import (
    AissembleOIPFastAPI,
)
from aissemble_open_inference_protocol_shared.auth.authzforce_adapter import (
    AuthzforceAdapter,
)


def get_oip_fastapi(oip_handler) -> AissembleOIPFastAPI:
    return AissembleOIPFastAPI(oip_handler, AuthzforceAdapter())


def get_oip_grpc(oip_handler) -> AissembleOIPgRPC:
    return AissembleOIPgRPC(oip_handler)


os.environ["KRAUSENING_BASE"] = "src/resources/krausening/base"
_oip_handler = OIPHandler()
_app_wrapper = get_oip_fastapi(_oip_handler)
_app_wrapper.model_load("yolo11n")
app = _app_wrapper.server
