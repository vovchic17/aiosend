from threading import Thread


class PropagatingThread(Thread):
    """
    A custom thread class that propagates exceptions to the parent thread.

    This class extends the Thread class and overrides the run() method to catch
    and propagate any exceptions that occur during the thread's execution.
    """

    def run(self) -> None:
        """
        Override the run method of the Thread class.

        This method catches any exceptions that occur
        during the thread's execution.
        """
        self._exc: Exception | None = None
        try:
            self.ret = self._target(*self._args, **self._kwargs)  # type: ignore[attr-defined]
        except Exception as e:  # noqa: BLE001
            self._exc = e

    def join(self, timeout: float | None = None) -> None:
        """
        Override the join method of the Thread class.

        This method joins the thread and propagates any exceptions
        that occurred during the thread's execution.
        """
        super().join(timeout=timeout)
        if self._exc is not None:
            raise self._exc
