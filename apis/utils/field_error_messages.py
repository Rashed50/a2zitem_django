def get_field_error_messages(field_name, field_type='default'):
    # Common base messages for all field types
    base_messages = {
        'required' : f'{field_name} is required.',
        'null'     : f'{field_name} cannot be null.',
        'blank'    : f'{field_name} cannot be blank.',
        'invalid'  : f'Invalid {field_name.lower()} value.'
    }
    
    # Field type specific additional messages
    type_specific = {
        'PrimaryKeyRelated': {
            'does_not_exist': f'{field_name} does not exist.',
            'incorrect_type': f'{field_name} must be a valid ID.'
        },
        'CharField': {
            'max_length': f'{field_name} cannot exceed {{max_length}} characters.',
            'min_length': f'{field_name} must be at least {{min_length}} characters.'
        },
        'EmailField': {
            'invalid': f'Enter a valid {field_name.lower()} address.'
        },
        'IntegerField': {
            'max_value': f'{field_name} cannot be greater than {{max_value}}.',
            'min_value': f'{field_name} cannot be less than {{min_value}}.'
        },
        'DecimalField': {
            'max_value' : f'{field_name} cannot be greater than {{max_value}}.',
            'min_value' : f'{field_name} cannot be less than {{min_value}}.',
            'max_digits': f'{field_name} cannot have more than {{max_digits}} digits.',
            'max_decimal_places': f'{field_name} cannot have more than {{max_decimal_places}} decimal places.',
            'max_whole_digits'  : f'{field_name} cannot have more than {{max_whole_digits}} whole digits.'
        },
        'DateField': {
            'invalid': f'Enter a valid {field_name.lower()} date.'
        },
        'DateTimeField': {
            'invalid': f'Enter a valid {field_name.lower()} date/time.'
        },
        'BooleanField': {
            'invalid': f'{field_name} must be either true or false.'
        },
        'ChoiceField': {
            'invalid_choice': f'Invalid {field_name.lower()} selection.'
        },
        'FileField': {
            'invalid': f'Invalid {field_name.lower()} file.',
            'empty': f'{field_name} file cannot be empty.',
            'max_length': f'{field_name} file name too long.'
        },
        'ImageField': {
            'invalid_image': f'Upload a valid {field_name.lower()} image.'
        },
        'URLField': {
            'invalid': f'Enter a valid {field_name.lower()} URL.'
        },
        'UUIDField': {
            'invalid': f'Enter a valid {field_name.lower()} UUID.'
        },
        'ListField': {
            'empty': f'{field_name} cannot be empty.',
            'invalid': f'Invalid {field_name.lower()} list.'
        },
        'DictField': {
            'empty': f'{field_name} cannot be empty.',
            'invalid': f'Invalid {field_name.lower()} dictionary.'
        },
        'JSONField': {
            'invalid': f'Invalid {field_name.lower()} JSON data.'
        },
        'default': {}
    }
    
    # Merge base messages with type specific messages
    return {**base_messages, **type_specific.get(field_type, {})}


