from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton

from src.ui.components.drag_drop import DragDropWidget
from src.ui.components.language_combobox import LanguageComboBox
from src.ui.components.progress import ImportProgressDialog
from src.ui.components.pipeline_worker import PipelineWorker

class CreateDictionaryView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Create Dictionary')
        main_layout = QVBoxLayout(self)

        drag_layout = QHBoxLayout()
        drag_layout.setAlignment(Qt.AlignCenter)
        self.drag1 = DragDropWidget(['.xml'], 'Drag the source\nlanguage file here', droped_text='Source language\nfile received!')
        self.drag1.setMinimumHeight(360)
        self.drag1.setMaximumHeight(360)
        self.drag1.setMinimumWidth(360)
        self.drag1.setMaximumWidth(360)
        self.drag2 = DragDropWidget(['.xml'], 'Drag the target\nlanguage file here', droped_text='Target language\nfile received!')
        self.drag2.setMinimumHeight(360)
        self.drag2.setMaximumHeight(360)
        self.drag2.setMinimumWidth(360)
        self.drag2.setMaximumWidth(360)
        drag_layout.addWidget(self.drag1)
        drag_layout.addSpacing(240)
        drag_layout.addWidget(self.drag2)
        main_layout.addLayout(drag_layout)

        langs_outer_layout = QHBoxLayout()
        langs_outer_layout.setAlignment(Qt.AlignCenter)

        lang1_layout = QVBoxLayout()
        lang1_layout.setAlignment(Qt.AlignCenter)
        lang1_label = QLabel('Source Language:')
        lang1_layout.addWidget(lang1_label, alignment=Qt.AlignCenter)
        self.lang1_combo = LanguageComboBox(cache='source')
        lang1_layout.addWidget(self.lang1_combo)

        lang2_layout = QVBoxLayout()
        lang2_layout.setAlignment(Qt.AlignCenter)
        lang2_label = QLabel('Target Language:')
        lang2_layout.addWidget(lang2_label, alignment=Qt.AlignCenter)
        self.lang2_combo = LanguageComboBox(cache='target')
        lang2_layout.addWidget(self.lang2_combo)

        langs_outer_layout.addLayout(lang1_layout)
        langs_outer_layout.addSpacing(400)
        langs_outer_layout.addLayout(lang2_layout)
        main_layout.addLayout(langs_outer_layout)

        mod_layout = QVBoxLayout()
        mod_layout.setAlignment(Qt.AlignCenter)
        mod_label = QLabel('Mod Name:')
        mod_layout.addWidget(mod_label, alignment=Qt.AlignCenter)
        self.mod_name_input = QLineEdit()
        self.mod_name_input.setMinimumWidth(600)
        self.mod_name_input.setMaximumWidth(800)
        mod_layout.addWidget(self.mod_name_input, alignment=Qt.AlignCenter)
        main_layout.addLayout(mod_layout)

        self.create_btn = QPushButton('Create Dictionary')
        main_layout.addWidget(self.create_btn, alignment=Qt.AlignCenter)
        self.create_btn.clicked.connect(self.on_create_clicked)

        self.file1 = None
        self.file2 = None
        self.drag1.file_dropped.connect(self.set_file1)
        self.drag2.file_dropped.connect(self.set_file2)

    def set_file1(self, path):
        self.file1 = path

    def set_file2(self, path):
        self.file2 = path

    def on_create_clicked(self):
        if not self.file1 or not self.file2:
            from PySide6.QtWidgets import QMessageBox
            QMessageBox.warning(self, 'Warning', 'Please select both language files.')
            return
        if not self.mod_name_input.text():
            from PySide6.QtWidgets import QMessageBox
            QMessageBox.warning(self, 'Warning', 'Mod name cannot be empty.')
            return

        from src.pipelines.dictionary_actions import DictionaryCreationPipeline
        pipeline = DictionaryCreationPipeline(
            source_path=self.file1,
            target_path=self.file2,
            source_language=self.lang1_combo.currentText(),
            target_language=self.lang2_combo.currentText(),
            mod_name=self.mod_name_input.text()
        )
        self.progress_dialog = ImportProgressDialog('Creating dictionary', 'Processing files...')
        self.worker = PipelineWorker(pipeline)
        self.worker.finished.connect(self.progress_dialog.accept)
        self.worker.error.connect(lambda err: self.show_error(err))
        self.worker.start()
        self.progress_dialog.exec()
        
    def show_error(self, tb_str):
        from PySide6.QtWidgets import QMessageBox
        self.progress_dialog.reject()
        QMessageBox.critical(self, 'Error', tb_str)