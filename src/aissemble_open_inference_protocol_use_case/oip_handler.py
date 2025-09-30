###
# #%L
# aiSSEMBLE::Open Inference Protocol Use Cases::FastAPI, gRPC, and Kserve Inference
# %%
# Copyright (C) 2024 Booz Allen Hamilton Inc.
# %%
# This software package is licensed under the Booz Allen Public License. All Rights Reserved.
# #L%
###
from typing import Optional

from krausening.logging import LogManager
from aissemble_open_inference_protocol_shared.handlers.dataplane import (
    DataplaneHandler,
)
from aissemble_open_inference_protocol_shared.handlers.model_handler import ModelHandler
from aissemble_open_inference_protocol_shared.types.dataplane import (
    InferenceRequest,
    InferenceResponse,
    ModelMetadataResponse,
    ModelReadyResponse,
    MetadataTensor,
    ResponseOutput,
    Datatype,
)

from ultralytics import YOLO


class OIPHandler(DataplaneHandler, ModelHandler):
    """
    Custom handler that implements all Open Inference Protocol endpoints.
    This example demonstrates how to implement custom handlers for each endpoint:
    - ModelInfer: Performs simple Yolo predict operations on input data
    - ModelMetadata: Returns metadata about the model
    - ModelReady: Checks if the model is ready for inference
    - ServerMetadata: Returns server information
    - ServerReady: Returns server readiness status
    - ServerLive: Returns server liveness status
    """

    logger = LogManager.get_instance().get_logger("OIPHandler")

    def __init__(self):
        super().__init__()
        self.model = None
        self.ready = False

    def infer(
        self,
        payload: InferenceRequest,
        model_name: str,
        model_version: Optional[str] = None,
    ) -> InferenceResponse:
        """
        Perform inference using the provided input data.
        This example performs simple YOLO perdict operations based on the input requests.
        """

        input_tensor = payload.inputs[0]

        # Get the data from the TensorData object
        try:
            data_list = input_tensor.data.root
            is_grpc_request = False

            # decode to bytes list to string list if it's a grpc request
            if len(data_list) > 0 and isinstance(data_list[0], bytes):
                is_grpc_request = True
                data_list = [b.decode("utf-8") for b in data_list]
            self.logger.info(f"Processing input data: {data_list}")
        except Exception as e:
            self.logger.error(f"Error processing data: {e}")
            raise ValueError(f"Invalid input data format: {e}")

        # Perform yolo perdict
        results = self.model(data_list, stream=True)

        # Process output generator
        output_data = []
        for result in results:
            boxes = result.boxes  # Boxes object for bounding box outputs
            for i, box in enumerate(boxes):
                # Extract class ID
                cls_id = int(box.cls)

                # get the class label using the class_id
                class_label = result.names[cls_id]

                # encode the content if it's grpc request
                if is_grpc_request:
                    class_label = class_label.encode("utf-8")

                output_data.append(class_label)
            result.show()
        self.logger.info(f"Output data: {output_data}")

        response_name = model_name
        if payload.outputs and len(payload.outputs) > 0:
            response_name = payload.outputs[0].name

        # create response with proper TensorData structure
        response = InferenceResponse(
            model_name=model_name,
            model_version=model_version,
            id=payload.id,
            outputs=[
                ResponseOutput(
                    name=response_name,
                    shape=[len(output_data)],
                    datatype=Datatype.BYTES,
                    data=output_data,
                )
            ],
        )

        if is_grpc_request:
            response.parameters = {"content_type": "string_param"}

        return response

    def model_metadata(
        self,
        model_name: str,
        model_version: Optional[str] = None,
    ) -> ModelMetadataResponse:
        """
        Return metadata about the model including input/output tensor specifications.
        """
        self.logger.info(
            f"Received model metadata request for model: {model_name}, version: {model_version}"
        )

        return ModelMetadataResponse(
            name=model_name,
            versions=[model_version] if model_version else None,
            platform="python",
            inputs=[MetadataTensor(name="input", datatype=Datatype.BYTES, shape=[1])],
            outputs=[MetadataTensor(name="output", datatype=Datatype.BYTES, shape=[1])],
        )

    def model_ready(
        self,
        model_name: str,
        model_version: Optional[str] = None,
    ) -> ModelReadyResponse:
        """
        Check if the model is ready for inference.
        This example considers specific models as ready.
        """
        self.logger.info(
            f"Received model ready request for model: {model_name}, version: {model_version}"
        )
        return ModelReadyResponse(name=model_name, ready=self.ready)

    def model_load(self, model_name) -> bool:
        self.model = YOLO("model/" + model_name + ".pt")
        self.ready = True
        self.logger.info("Model has been loaded")
        return True
