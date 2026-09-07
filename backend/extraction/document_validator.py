def validate_output(data, schema):

    validated = {}

    for key in schema.keys():
        validated[key] = data.get(key, "")

    return validated