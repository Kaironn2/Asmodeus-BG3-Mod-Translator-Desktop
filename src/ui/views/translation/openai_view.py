from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit, 
    QComboBox
)
from PySide6.QtCore import Qt, QThread, Signal

from src.ui.components.drag_drop import DragDropWidget
from src.ui.components.language_combobox import LanguageComboBox

from src.config.config_manager import load_openai_key, save_openai_key
from src.database.connection import get_session
from src.database.repositories.language_repository import LanguageRepository
from src.pipelines.openai_translation import OpenAITranslationPipeline


class OpenaiPipelineWorker(QThread):
    progress = Signal(str)
    finished = Signal()

    def __init__(self, pipeline):
        super().__init__()
        self.pipeline = pipeline

    def run (self):
        import sys

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
        finally:
            sys.stdout = old_stdout
            self.finished.emit()


class OpenaiView(QWidget):
    def __init__(self, languages, parent=None):
        super().__init__(parent)
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(32, 32, 32, 32)
        main_layout.setSpacing(16)
        
        top_row_widget = QWidget()
        top_row_widget.setFixedHeight(300)
        top_row_layout = QHBoxLayout(top_row_widget)
        top_row_layout.setContentsMargins(0, 0, 0, 0)
        top_row_layout.setSpacing(0)

        left_layout = QVBoxLayout()
        left_layout.setContentsMargins(0, 0, 0, 0)
        left_layout.setSpacing(0)
        self.drag_drop = DragDropWidget()
        self.drag_drop.file_dropped.connect(self.on_file_dropped)
        self.drag_drop.setFixedHeight(240)
        self.drag_drop.setMinimumWidth(240)
        left_layout.addWidget(self.drag_drop, alignment=Qt.AlignTop | Qt.AlignLeft)

        left_widget = QWidget()
        left_widget.setLayout(left_layout)

        right_layout = QVBoxLayout()
        right_layout.setSpacing(20)
        right_layout.setContentsMargins(24, 24, 24, 24)
        right_layout.setAlignment(Qt.AlignTop | Qt.AlignLeft)

        input_row = QHBoxLayout()
        self.path_input = QLineEdit()
        self.path_input.setPlaceholderText('Ex: C:/path/for/file.zip')
        validate_btn = QPushButton('Validate')
        validate_btn.clicked.connect(self.validate_path)
        input_row.addWidget(self.path_input)
        input_row.addWidget(validate_btn)
        right_layout.addLayout(input_row)

        self.openai_key_input = QLineEdit()
        self.openai_key_input.setPlaceholderText('OpenAI API Key')
        self.openai_key_input.setFixedHeight(40)
        self.openai_key_input.setMinimumWidth(240)
        right_layout.addWidget(self.openai_key_input)

        self.openai_key_input.setText(load_openai_key())

        right_widget = QWidget()
        right_widget.setLayout(right_layout)

        lang_row = QHBoxLayout()

        self.source_lang_combo = LanguageComboBox(languages=languages)
        self.target_lang_combo = LanguageComboBox(languages=languages)

        lang_row.addWidget(self.source_lang_combo)
        lang_row.addWidget(self.target_lang_combo)
        lang_row.setAlignment(Qt.AlignHCenter)
        right_layout.addLayout(lang_row)

        self.start_btn = QPushButton('Start Translation')
        self.start_btn.setFixedWidth(180)
        self.start_btn.clicked.connect(self.on_start_translation)
        right_layout.addWidget(self.start_btn, alignment=Qt.AlignHCenter)

        top_row_layout.addWidget(left_widget)
        top_row_layout.addWidget(right_widget)

        bottom_row_widget = QWidget()
        bottom_row_layout = QHBoxLayout(bottom_row_widget)
        bottom_row_layout.setContentsMargins(0, 0, 0, 0)
        bottom_row_layout.setSpacing(0)

        self.progress_text = QTextEdit()
        self.progress_text.setReadOnly(True)
        self.progress_text.setPlaceholderText('Waiting for translation...')
        bottom_row_layout.addWidget(self.progress_text)

        main_layout.addWidget(top_row_widget)
        main_layout.addWidget(bottom_row_widget)

    def on_file_dropped(self, file_path):
        self.file_path = file_path
        self.path_input.setText(file_path)

    def validate_path(self):
        self.file_path = self.path_input.text()

    def on_start_translation(self):
        print('Starting translation...')
        self.progress_text.setPlainText('Starting translation...')

    def on_finished_translation(self):
        self.progress_text.append('Translation finished!')

    def on_start_translation(self):
        save_openai_key(self.openai_key_input.text())
        source_lang = self.source_lang_combo.currentText()
        target_lang = self.target_lang_combo.currentText()
        mod_name = 'Cosmic Sorcery'
        author = 'Kaironn2'
        description = f'{mod_name} ptbr translation'

        with get_session() as session:
            source_lang_code = LanguageRepository.find_language_by_name(session=session, name=source_lang)
            target_lang_code = LanguageRepository.find_language_by_name(session=session, name=target_lang)

            openai_translation_pipeline = OpenAITranslationPipeline(
                mod_name=mod_name,
                session=session,
                source_language=source_lang_code,
                target_language=target_lang_code,
                author=author,
                description=description,
                mod_path=self.file_path,
            )

            self.worker = OpenaiPipelineWorker(openai_translation_pipeline)
            self.worker.progress.connect(self.append_progress)
            self.worker.finished.connect(self.on_finished_translation)
            self.worker.start()

    def append_progress(self, text):
        self.progress_text.append(text)
