import time
from typing import Callable, Optional


class RuntimeCounter:
    def __init__(self, description: Optional[str] = None):
        self._description = description

    def __call__(self, method: Callable):
        def wrapper(instance, *args, **kwargs):
            if self._description is not None:
                print(self._description)

            st = time.perf_counter()
            method_result = method(instance, *args, **kwargs)
            et = time.perf_counter()
            print(f"runtime : {round((et - st), 2)}s\n\n")

            return method_result

        return wrapper

