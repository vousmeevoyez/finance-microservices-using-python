"""
    BNI E-Collection Helper
    ________________________
"""
import json


def rdl_extract_error(obj):
    """ extract error from BNI Response format """
    error_message = ""

    if isinstance(obj.original_exception, dict):
        for key, value in obj.original_exception.items():
            for key, value in value.items():
                if key == "errorMessage":
                    error_message = value
                elif key == "responseMessage":
                    error_message = value
                # end if
        # end for
    # end if
    return error_message


def extract_error(obj):
    try:
        key = obj.original_exception["response"]
        error = rdl_extract_error(obj)
    except:
        error = obj.message
    return error
