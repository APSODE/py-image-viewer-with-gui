import time
from typing import Callable


class RuntimeCounter:
    def __init__(self):
        pass

    def __call__(self, method: Callable):
        def wrapper(instance, *args, **kwargs):
            st = time.perf_counter()
            method_result = method(instance, *args, **kwargs)
            et = time.perf_counter()

            print(f"runtime : {round((et - st), 2)}s")

            return method_result

        return wrapper

