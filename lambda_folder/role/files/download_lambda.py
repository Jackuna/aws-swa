"""
    Script to download individual Lambda Function and dump code in specified directory
"""
import os
import sys
from urllib.request import urlopen
import zipfile
from io import BytesIO

import boto3


def get_lambda_functions_code_url(fn_name):

    client = boto3.client("lambda")
    functions_code_url = []
    fn_code = client.get_function(FunctionName=fn_name)["Code"]
    fn_code["FunctionName"] = fn_name
    functions_code_url.append(fn_code)
    return functions_code_url


def download_lambda_function_code(fn_name, fn_code_link, dir_path):

    function_path = os.path.join(dir_path, fn_name)
    if not os.path.exists(function_path):
        os.mkdir(function_path)
    with urlopen(fn_code_link) as lambda_extract:
        with zipfile.ZipFile(BytesIO(lambda_extract.read())) as zfile:
            zfile.extractall(function_path)


if __name__ == "__main__":
    inp = sys.argv[1:]
    print("Destination folder {}".format(inp))
    if inp and os.path.exists(inp[0]):
        dest = os.path.abspath(inp[0])
        fc = get_lambda_functions_code_url(sys.argv[2])
        for i, f in enumerate(fc):
            print("Downloading Lambda function {}".format(f["FunctionName"]))
            download_lambda_function_code(f["FunctionName"], f["Location"], dest)
    else:
        print("Destination folder doesn't exist")
