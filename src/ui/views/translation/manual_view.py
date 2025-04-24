from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, QAbstractItemView,
    QFileDialog, QLineEdit, QHeaderView,
)
from PySide6.QtCore import Qt

from src.ui.components.drag_drop import DragDropWidget
from src.ui.components.language_combobox import LanguageComboBox

from src.config.config_manager import ConfigManager
from src.database.connection import get_session
from src.database.repositories.dictionary_repository import DictionaryRepository
from src.database.repositories.language_repository import LanguageRepository
from src.helpers.validators import Validators
from src.parsers.xml_parser import XmlParser
from src.pipelines.manual_translation import ManualTranslationPipeline


class ManualView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.df = None
        self.xml_path = None

        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(32, 32, 32, 32)
        main_layout.setSpacing(16)

        left_layout = QVBoxLayout()
        left_layout.setSpacing(16)

        self.drag_drop = DragDropWidget(
            accepted_extensions=['.zip', '.pak', '.xml'],
            description_text='Drag and drop your\nXML file here\nor click to select a file',
        )
        self.drag_drop.setFixedHeight(240)
        self.drag_drop.setMinimumWidth(240)
        self.drag_drop.file_dropped.connect(self.on_file_dropped)
        left_layout.addWidget(self.drag_drop, alignment=Qt.AlignTop)

        self.source_lang_combo = LanguageComboBox(cache='source')
        self.source_lang_combo.setMinimumWidth(240)
        self.source_lang_combo.setMaximumWidth(240)
        self.target_lang_combo = LanguageComboBox(cache='target')
        self.target_lang_combo.setMinimumWidth(240)
        self.target_lang_combo.setMaximumWidth(240)
        left_layout.addWidget(self.source_lang_combo)
        left_layout.addWidget(self.target_lang_combo)

        self.mod_name_input = QLineEdit()
        self.mod_name_input.setPlaceholderText("Mod Name")
        self.mod_name_input.setMinimumWidth(240)
        self.mod_name_input.setMaximumWidth(240)
        left_layout.addWidget(self.mod_name_input)      

        self.import_btn = QPushButton('Import XML')
        left_layout.addWidget(self.import_btn)
        self.import_btn.clicked.connect(self.import_xml)

        self.export_btn = QPushButton('Export XML')
        left_layout.addWidget(self.export_btn)
        self.export_btn.clicked.connect(self.export_xml)

        left_layout.addStretch(1)
        left_widget = QWidget()
        left_widget.setLayout(left_layout)
        left_widget.setFixedWidth(260)

        right_layout = QVBoxLayout()
        self.table = QTableWidget()
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(['Source Text', 'Target Text'])
        self.table.setEditTriggers(QAbstractItemView.AllEditTriggers)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Interactive)
        self.table.setColumnWidth(0, 500 // 2)
        self.table.setColumnWidth(1, 500 // 2)
        self.table.verticalHeader().setVisible(False)
        self.table.setStyleSheet("""
            QTableWidget {
                background: #2a2a2a;
                color: #fff;
                font-size: 15px;
            }
            QHeaderView::section {
                background: #fff;
                color: #222;
                font-weight: bold;
                border: 1px solid #ddd;
            }
            QTableWidget QTableCornerButton::section {
                background: #2a2a2a;
                border: 1px solid #ddd;
            }
        """)
        right_layout.addWidget(self.table)
        right_widget = QWidget()
        right_widget.setLayout(right_layout)

        main_layout.addWidget(left_widget)
        main_layout.addWidget(right_widget)

        self.table.itemChanged.connect(self.on_cell_edited)

    def on_cell_edited(self, item):
        row = item.row()
        col = item.column()
        if col == 1 and self.df is not None:
            target_text = item.text()
            self.df.at[row, 'text'] = target_text

            source_text = self.df.at[row, 'source_text']
            content_uid = self.df.at[row, 'contentuid']
            mod_name = self.mod_name_input.text()

            with get_session() as session:

                DictionaryRepository.upsert_translation(
                    session=session,
                    source_language=self.source_language_code,
                    target_language=self.target_language_code,
                    source_text=source_text,
                    target_text=target_text,
                    uid=content_uid,
                    mod_name=mod_name,
                )

    def resizeEvent(self, event):
        super().resizeEvent(event)
        table_width = self.table.width() // 2
        self.table.setColumnWidth(0, table_width)
        self.table.setColumnWidth(1, table_width)

    def on_file_dropped(self, file_path):
        self.xml_path = file_path
        self.drag_drop.label.setText(f'File received!')

    def import_xml(self):
        with get_session() as session:
            self.source_language_code = LanguageRepository.find_language_by_name(
                session=session,
                name=self.source_lang_combo.currentText(),
            )
            self.target_language_code = LanguageRepository.find_language_by_name(
                session=session,
                name=self.target_lang_combo.currentText(),
            )

        self.mod_name = self.mod_name_input.text()
        ConfigManager.save_last_languages(
            source_lang=self.source_lang_combo.currentText(),
            target_lang=self.target_lang_combo.currentText(),
        )
        if not self.xml_path:
            return
        pipeline = ManualTranslationPipeline(
            xml_path=self.xml_path,
            mod_name=self.mod_name,
            source_language=self.source_lang_combo.currentText(),
            target_language=self.target_lang_combo.currentText(),
        )
        with get_session() as session:
            self.df = pipeline.run(session=session)
        self.populate_table_from_df()

    def populate_table_from_df(self):
        self.table.blockSignals(True)
        self.table.setRowCount(len(self.df))
        for idx, row in self.df.iterrows():
            source_item = QTableWidgetItem(str(row['source_text']))
            source_item.setFlags(source_item.flags() & ~Qt.ItemIsEditable)
            source_item.setTextAlignment(Qt.AlignTop)
            source_item.setData(Qt.TextWordWrap, True)
            target_item = QTableWidgetItem(str(row['text']))
            target_item.setTextAlignment(Qt.AlignTop)
            target_item.setData(Qt.TextWordWrap, True)
            self.table.setItem(idx, 0, source_item)
            self.table.setItem(idx, 1, target_item)
        self.table.resizeRowsToContents()
        self.table.blockSignals(False)

    def export_xml(self):
        if self.df is not None:
            file_path, _ = QFileDialog.getSaveFileName(
                self,
                'Export XML',
                f'{Validators.validate_mod_name(mod_name=self.mod_name)}_{self.target_language_code}.xml',
                'XML Files (*.xml)'
            )
            if file_path:
                export_df = self.df[['version', 'contentuid', 'text']].copy()
                export_df['text'] = export_df['text'].where(export_df['text'] != '', self.df['source_text'])
                XmlParser.dataframe_to_xml(export_df, file_path)
