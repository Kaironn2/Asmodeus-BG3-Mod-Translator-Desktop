from pathlib import Path

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
)
from PySide6.QtCore import Qt

from src.ui.components.drag_drop import DragDropWidget
from src.ui.components.language_combobox import LanguageComboBox
from src.ui.components.labeled_line_edit import LabeledLineEdit
from src.ui.components.error_dialog import show_error_popup
from src.ui.components.pipeline_worker import PipelineWorker
from src.ui.components.translation_progress import TranslationProgressTable, TranslationProgressBar

from src.config.config_manager import ConfigManager
from src.database.connection import get_session
from src.database.repositories.language_repository import LanguageRepository
from src.pipelines.deepl_translation import DeepLTranslationPipeline


class DeepLView(QWidget):
    def __init__(self, parent=None):
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
        self.drag_drop = DragDropWidget(
            accepted_extensions=['.zip', '.pak', '.xml'], 
            description_text='Drag and drop a ZIP,\n PAK or XML file here\nor click to select a file'
        )
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

        self.openai_key_input = LabeledLineEdit('OpenAI API Key', password=True)
        right_layout.addWidget(self.openai_key_input)
        self.openai_key_input.setText(ConfigManager.load_openai_key())

        self.mod_name_input = LabeledLineEdit('Mod Name')
        right_layout.addWidget(self.mod_name_input)

        self.author_input = LabeledLineEdit('Author Name')
        right_layout.addWidget(self.author_input)
        self.author_input.setText(ConfigManager.load_author())

        right_widget = QWidget()
        right_widget.setLayout(right_layout)

        lang_row = QHBoxLayout()

        self.source_lang_combo = LanguageComboBox(cache='source')
        self.target_lang_combo = LanguageComboBox(cache='target')

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
        bottom_row_layout = QVBoxLayout(bottom_row_widget)
        bottom_row_layout.setContentsMargins(0, 0, 0, 0)
        bottom_row_layout.setSpacing(8)

        self.progress_table = TranslationProgressTable()
        bottom_row_layout.addWidget(self.progress_table)

        self.progress_bar = TranslationProgressBar()
        bottom_row_layout.addWidget(self.progress_bar)
    
        main_layout.addWidget(top_row_widget)
        main_layout.addWidget(bottom_row_widget)

    def on_file_dropped(self, file_path):
        self.file_path = file_path

    def validate_path(self):
        self.file_path = self.path_input.text()

    def on_finished_translation(self):
        self.mod_name_input.clear()
        self.drag_drop.reset()

    def on_start_translation(self):
        self.progress_table.setRowCount(0)
        ConfigManager.save_openai_key(self.openai_key_input.text())
        ConfigManager.save_last_languages(
            self.source_lang_combo.currentText(),
            self.target_lang_combo.currentText()
        )
        ConfigManager.save_author(self.author_input.text())
        source_lang = self.source_lang_combo.currentText()
        target_lang = self.target_lang_combo.currentText()
        mod_name = self.mod_name_input.text()
        author = self.author_input.text()
        description = f'{mod_name} ptbr translation'

        with get_session() as session:
            source_lang_code = LanguageRepository.find_language_by_name(session=session, name=source_lang)
            target_lang_code = LanguageRepository.find_language_by_name(session=session, name=target_lang)

            openai_translation_pipeline = DeepLTranslationPipeline(
                deepl_api_key=ConfigManager.load_deepl_key(),
                mod_name=mod_name,
                session=session,
                source_language=source_lang_code,
                target_language=target_lang_code,
                author=author,
                description=description,
                mod_path=Path(self.file_path),
            )

            self.worker = PipelineWorker(openai_translation_pipeline)
            self.worker.finished.connect(self.on_finished_translation)
            self.worker.error.connect(self.show_worker_error) 
            self.worker.progress_row.connect(self.update_progress_table)
            self.worker.progress_value.connect(self.progress_bar.set_progress)
            self.worker.start()

    def show_worker_error(self, tb_str):
        show_error_popup(tb_str, self)

    def update_progress_table(self, index, source_text, target_text):
        self.progress_table.update_row(index, source_text, target_text)
