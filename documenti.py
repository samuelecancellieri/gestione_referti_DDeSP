from __future__ import print_function
import os
import time
import cloudmersive_convert_api_client
from cloudmersive_convert_api_client.rest import ApiException
from pprint import pprint

def elimina_documento(path_documento):
    try:
        os.remove(path_documento)
    except OSError as e:
        raise e
    else:
        return True

def converti_pdf_to_pdfA(pdf_originale:str):
    # Configure API key authorization: Apikey
    configuration = cloudmersive_convert_api_client.Configuration()
    configuration.api_key['Apikey'] = 'a88bca51-99b4-4d13-ac94-c3a5c9464820'
    # create an instance of the API class
    api_instance = cloudmersive_convert_api_client.EditPdfApi(cloudmersive_convert_api_client.ApiClient(configuration))
    input_file = pdf_originale # file | Input file to perform the operation on.
    # conformance_level = 'conformance_level_example' # str | Optional: Select the conformance level for PDF/A - specify '1b' for PDF/A-1b or specify '2b' for PDF/A-2b; default is PDF/A-1b (optional)
    try:
        # Convert a PDF file to PDF/A
        api_response = api_instance.edit_pdf_convert_to_pdf_a(input_file)
        pdfA=open(pdf_originale,'wb')
        pdfA.write(api_response)
        pdfA.close()
        # print(type(api_response))
        # pprint(api_response)
    except ApiException as e:
        print("Exception when calling EditPdfApi->edit_pdf_convert_to_pdf_a: %s\n" % e)
