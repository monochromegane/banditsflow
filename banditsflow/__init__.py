from metaflow import FlowSpec, step

class BanditsFlow(FlowSpec): # type: ignore

    @step
    def start(self) -> None:
        self.next(self.end)

    @step
    def end(self) -> None:
        pass
