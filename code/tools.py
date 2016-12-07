import warnings
import functools

init_weight = 5E-2
r_seed = 666

# Data format #


def str_2_value(str_value):
    try:
        return int(str_value)
    except ValueError:
        return float(str_value)


def general_max(x):
    if check_type(x, 'list') or check_type(x, 'set'):
        if len(x) > 0:
            return max(x)
    else:
        return x


def general_len(x):
    if check_type(x, 'list') or check_type(x, 'set'):
        return len(x)
    else:
        return 1


def as_array(x):
    if check_type(x, 'list'):
        return x
    else:
        return [x]


def check_type(data, dtype):
    dtype_name = type(data).__name__.lower()
    if dtype == 'int':
        return 'int' in dtype_name
    elif dtype == 'float':
        return 'float' in dtype_name
    elif dtype == 'str':
        return 'str' in dtype_name
    elif dtype == 'tuple':
        return 'tuple' in dtype_name
    elif dtype == 'list':
        return 'list' in dtype_name or 'array' in dtype_name or 'tuple' in dtype_name
    elif dtype == 'set':
        return 'set' in dtype_name
    elif dtype == 'dict':
        return 'map' in dtype_name or 'dict' in dtype_name
    elif dtype == 'agg':
        return 'set' in dtype_name or 'tuple' in dtype_name or \
               'list' in dtype_name or 'array' in dtype_name or \
               'dict' in dtype_name
    elif dtype == 'none':
        return data == 'None' or data == 'none' or data is None
    elif dtype == 'data':
        return 'data' in dtype_name


def is_int(data):
    return check_type(data, 'int')


def is_float(data):
    return check_type(data, 'float')


def is_val(data):
    return is_int(data) or is_float(data)


def is_str(data):
    return check_type(data, 'str')


def is_list(data):
    return check_type(data, 'list')


def is_set(data):
    return check_type(data, 'set')


def is_dict(data):
    return check_type(data, 'dict')


def is_none(data):
    return check_type(data, 'none')


def is_agg(data):
    return check_type(data, 'agg')


def is_data(data):
    return check_type(data, 'data')


# system tools #

def deprecated(func):
    """This is a decorator which can be used to mark functions
    as deprecated. It will result in a warning being emmitted
    when the function is used."""
    @functools.wraps(func)
    def new_func(*args, **kwargs):
        warnings.simplefilter('always', DeprecationWarning) #turn off filter
        warnings.warn("Call to deprecated function {}.".format(func.__name__), category=DeprecationWarning, stacklevel=2)
        warnings.simplefilter('default', DeprecationWarning) #reset filter
        return func(*args, **kwargs)
    return new_func
