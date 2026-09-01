import molotov
import sys

import numpy as np
import tritonclient.grpc.aio as grpcclient

from utils import test_output

@molotov.global_setup()
def init_test(args):
    global triton_client
    triton_client = get_triton_client()

def get_triton_client():
    try:
        triton_client = grpcclient.InferenceServerClient(
            url="localhost:8001",
            verbose=False,
        )
    except Exception as e:
        print("channel creation failed: " + str(e))
        sys.exit()

    return triton_client

@molotov.scenario(100)
async def infer(session):
    inputs, outputs, input0_data, input1_data = get_inputs_and_outputs()
    results = await triton_client.infer(model_name="simple", inputs=inputs, outputs=outputs)
    test_output(input0_data, input1_data, results)

def get_inputs_and_outputs():
    # Infer
    inputs = []
    outputs = []
    inputs.append(grpcclient.InferInput("INPUT0", [1, 16], "INT32"))
    inputs.append(grpcclient.InferInput("INPUT1", [1, 16], "INT32"))

    # Create the data for the two input tensors. Initialize the first
    # to unique integers and the second to all ones.
    input0_data = np.arange(start=0, stop=16, dtype=np.int32)
    input0_data = np.expand_dims(input0_data, axis=0)
    input1_data = np.ones(shape=(1, 16), dtype=np.int32)

    # Initialize the data
    inputs[0].set_data_from_numpy(input0_data)
    inputs[1].set_data_from_numpy(input1_data)

    outputs.append(grpcclient.InferRequestedOutput("OUTPUT0"))
    outputs.append(grpcclient.InferRequestedOutput("OUTPUT1"))

    return inputs, outputs, input0_data, input1_data
