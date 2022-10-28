"""

    """

def return_not_special_variables_of_class(cls) :
    return {x : y for x , y in cls.__dict__.items() if not x.startswith('__')}
