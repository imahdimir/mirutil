"""

    """

def return_not_special_variables_of_class(cls) :
    return [x for x in cls.__dict__.keys() if not x.startswith('__')]
