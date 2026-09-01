def test_output(input0_data, input1_data, results):
    # Get the output arrays from the results
    output0_data = results.as_numpy("OUTPUT0")
    output1_data = results.as_numpy("OUTPUT1")

    # Validate the output
    for i in range(16):
        assert (input0_data[0][i] + input1_data[0][i]) == output0_data[0][i]
        assert (input0_data[0][i] - input1_data[0][i]) == output1_data[0][i]