import copy, collections
from dynamof import builder as ab
from dynamof import runners
from dynamof.utils import new_id


Operation = collections.namedtuple("Operation", [
    "description",
    "runner"
])


def create(table_name, hash_key, allow_existing=False):
    description = dict(
        TableName=table_name,
        KeySchema=ab.build_key_schema(hash_key),
        AttributeDefinitions=ab.build_attribute_definitions([hash_key]),
        ProvisionedThroughput=ab.build_provisioned_throughput()
    )
    return Operation(description, runners.create(
        allow_existing=allow_existing
    ))


def find(table_name, key):
    description = dict(
        TableName=table_name,
        Key=ab.build_value_type_tree(key)
    )
    return Operation(description, runners.find())


def add(table_name, item, auto_inc=False):
    attributes = copy.deepcopy(item)
    if auto_inc is True:
        attributes['id'] = new_id()
    description = dict(
        TableName=table_name,
        Item=ab.build_value_type_tree(attributes)
    )
    return Operation(description, runners.add())


def update(table_name, key, attributes):
    description = dict(
        TableName=table_name,
        Key=ab.build_value_type_tree(key),
        ConditionExpression=ab.build_condition_expression(key),
        UpdateExpression=ab.build_update_expression(attributes),
        ExpressionAttributeValues=ab.build_expression_attribute_values({**key, **attributes})
    )
    return Operation(description, runners.update())


def delete(table_name, key):
    description = dict(
        TableName=table_name,
        Key=ab.build_value_type_tree(key),
        ConditionExpression=ab.build_condition_expression(key),
        ExpressionAttributeValues=ab.build_expression_attribute_values(key)
    )
    return Operation(description, runners.delete())
