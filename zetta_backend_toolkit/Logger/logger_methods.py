import logging
import inspect

logging.basicConfig(level=logging.DEBUG,  # Establecer el nivel de logging a DEBUG
                    format='%(levelname)s - %(asctime)s - %(message)s',  # Formato del mensaje
                    handlers=[logging.StreamHandler()])  # Enviar los logs a la consola

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def log(func):
    """
    Decorator function that logs the details of a function call, including the function name, module name, arguments, and keyword arguments.
    If the decorated function is asynchronous, it returns an asynchronous wrapper that logs the details and then calls the original function.
    If the decorated function is synchronous, it returns a synchronous wrapper that logs the details and then calls the original function.
    If an exception occurs during the function call, it is logged and re-raised.
    Args:
        func: The function to be decorated.
    Returns:
        The decorated function.
    Raises:
        Exception: If an exception occurs during the function call, it is logged and re-raised.
    """

    async def async_wrapper(*args, **kwargs):
        """
        Wraps an asynchronous function and logs information before and after its execution.
        Parameters:
        - `*args`: Positional arguments to be passed to the wrapped function.
        - `**kwargs`: Keyword arguments to be passed to the wrapped function.
        Returns:
        The result of the wrapped function.
        Raises:
        Any exception raised by the wrapped function.
        """

        try:
            logger.debug(f"----")
            logger.debug(f"Calling function: {func.__name__} in module: {func.__module__}")
            logger.debug(f"Arguments: {args}")
            logger.debug(f"Keyword Arguments: {kwargs}")
            #logger.debug(f"----")
            result = await func(*args, **kwargs)
            logger.debug(f"Function {func.__name__} returned: {result}")
            return result
        except Exception as exc:
            logger.error(exc)
            raise

    def sync_wrapper(*args, **kwargs):
        """
        Wrapper function that logs the function call, arguments, and result.
        Args:
            *args: Positional arguments passed to the wrapped function.
            **kwargs: Keyword arguments passed to the wrapped function.
        Returns:
            The result of the wrapped function.
        Raises:
            Exception: If an exception occurs during the execution of the wrapped function.
        """

        try:
            logger.debug(f"Calling function: {func.__name__} in module: {func.__module__}")
            logger.debug(f"Arguments: {args}")
            logger.debug(f"Keyword Arguments: {kwargs}")
            result = func(*args, **kwargs)
            logger.debug(f"Function {func.__name__} returned: {result}")
            return result
        except Exception as exc:
            logger.error(exc)
            raise

    if inspect.iscoroutinefunction(func):
        return async_wrapper
    else:
        return sync_wrapper

def log_all_methods(cls):
    """
    Decorator function that logs all methods of a class.
    Args:
        cls: The class to decorate.
    Returns:
        The decorated class with all methods logged.
    """
    
    for name, method in cls.__dict__.items():
        if callable(method):
            setattr(cls, name, log(method))
    return cls
