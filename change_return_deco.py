def square_return(func):
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs) ** 2
    return wrapper


@square_return
def test():
    return 12


test()
