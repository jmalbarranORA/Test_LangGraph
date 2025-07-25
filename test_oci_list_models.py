import os
import logging
from dotenv import load_dotenv

import oci
from oci.response import Response



# Load environment
load_dotenv()

# Initialize logging
logger = logging.getLogger(__name__)
logger.setLevel(os.getenv("APP_LOGLEVEL", "INFO"))



# Create a default config using DEFAULT profile in default location
# Refer to
# https://docs.cloud.oracle.com/en-us/iaas/Content/API/Concepts/sdkconfig.htm#SDK_and_CLI_Configuration_File
# for more info
config = oci.config.from_file(profile_name=os.getenv("OCI_PROFILE")) # type: ignore


# Initialize service client with default config file
generative_ai_client = oci.generative_ai.GenerativeAiClient(config=config, service_endpoint=os.getenv("OCI_GENAI_MGT_SERVICE_ENDPOINT"))


# Send the request to service, some parameters are not required, see API
# doc for more info
list_models_response: Response = generative_ai_client.list_models(
    compartment_id=os.getenv("OCI_COMPARTMENT_OCID"),
    # opc_request_id="ZE59UGS2YXI2OADCTDH4<unique_ID>",
    # vendor="EXAMPLE-vendor-Value",
    capability=["TEXT_GENERATION"],
    # lifecycle_state="ACTIVE",
    # display_name="EXAMPLE-displayName-Value",
    # id="ocid1.test.oc1..<unique_ID>EXAMPLE-id-Value",
    # limit=857,
    # page="EXAMPLE-page-Value",
    # sort_order="DESC",
    # sort_by="timeCreated"
    ) # type: ignore

# Get the data from response
print(list_models_response.data)
