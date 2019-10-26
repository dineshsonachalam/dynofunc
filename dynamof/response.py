
from boto3.dynamodb.types import TypeDeserializer

from dynamof.core.utils import strip_Decimals


def destructure_type_tree(data):

    if data is None:
        return None

    # Using `strip_Decimals` here to patch an
    # undesireable behavior with dynamo where
    # it takes in number types but always returns
    # Decimal class type.
    # https://github.com/boto/boto3/issues/369

    return {
        k: strip_Decimals(TypeDeserializer().deserialize(v)) for k, v in data.items()
    }

get_data = lambda type_tree: destructure_type_tree(type_tree)
get_retries = lambda response: response.get('ResponseMetadata', {}).get('RetryAttempts', None)
get_success = lambda response: response.get('ResponseMetadata', {}).get('HTTPStatusCode', 0) == 200
get_count = lambda response: response.get('Count', None)
get_scanned_count = lambda response: response.get('ScannedCount', None)


def create_response(response, skipped=False):

    return {
        'table_already_existed': response is None and skipped is True,
        'retries': get_retries(response or {}),
        'success': get_success(response or {}),
        'raw': response
    }


def find_response(response):

    return {
        'item': get_data(response.get('Item', {})),
        'retries': get_retries(response),
        'success': get_success(response),
        'raw': response
    }


def add_response(response):

    return {
        'item': get_data(response.get('Attributes', {})),
        'retries': get_retries(response),
        'success': get_success(response),
        'raw': response
    }


def update_response(response):

    return {
        'item': get_data(response.get('Attributes', {})),
        'retries': get_retries(response),
        'success': get_success(response),
        'raw': response
    }


def query_response(response):

    return {
        'items': [get_data(type_tree) for type_tree in response.get('Items', [])],
        'count': get_count(response),
        'scanned_count': get_scanned_count(response),
        'retries': get_retries(response),
        'success': get_success(response),
        'raw': response
    }


def delete_response(response):

    return {
        'retries': get_retries(response),
        'success': get_success(response),
        'raw': response
    }
