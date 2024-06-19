#!/bin/bash

# Test the common_factors_classification endpoint with 1000 requests

# save output to a file
ab -n 100 -c 1 -l -p payload.json -T application/json http://localhost:8000/common_factors_classification > ab_output_1_1.txt
ab -n 100 -c 2 -l -p payload.json -T application/json http://localhost:8000/common_factors_classification > ab_output_1_2.txt
ab -n 100 -c 4 -l -p payload.json -T application/json http://localhost:8000/common_factors_classification > ab_output_1_4.txt
ab -n 100 -c 8 -l -p payload.json -T application/json http://localhost:8000/common_factors_classification > ab_output_1_8.txt