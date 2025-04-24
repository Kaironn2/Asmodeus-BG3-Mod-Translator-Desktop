from PySide6.QtCore import QThread, Signal


class PipelineWorker(QThread):
    progress = Signal(str)
    progress_value = Signal(int, int)
    progress_row = Signal(int, str, str)
    finished = Signal()
    error = Signal(str)

    def __init__(self, pipeline):
        super().__init__()
        self.pipeline = pipeline

    def run(self):
        import sys

        self.pipeline.progress_row = self.progress_row
        self.pipeline.progress_value = self.progress_value

        class PrintCatcher:
            def __init__(self, signal):
                self.signal = signal
            def write(self, message):
                self.signal.emit(message.strip())
            def flush(self):
                pass

        old_stdout = sys.stdout
        sys.stdout = PrintCatcher(self.progress)
        try:
            self.pipeline.run()
        except Exception:
            import traceback
            error_message = traceback.format_exc()
            self.error.emit(error_message)
        finally:
            sys.stdout = old_stdout
            self.finished.emit()

