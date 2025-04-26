from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem, QLineEdit, QListWidget, QLabel, QAbstractItemView, QHeaderView,
    QStyledItemDelegate, QTextEdit, QFileDialog, QMessageBox
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QTextOption

from src.database.connection import get_session
from src.database.repositories.dictionary_repository import DictionaryRepository
from src.pipelines.dictionary_actions import DictionaryImportPipeline, DictionaryExportPipeline
from src.ui.components.buttons import ActionButton
from src.ui.components.progress import ImportProgressDialog
from src.ui.components.pipeline_worker import PipelineWorker


class TextEditDelegate(QStyledItemDelegate):
    def createEditor(self, parent, option, index):
        editor = QTextEdit(parent)
        editor.setWordWrapMode(QTextOption.WordWrap)
        return editor

    def setEditorData(self, editor, index):
        text = index.model().data(index, Qt.EditRole) or ""
        editor.setPlainText(text)

    def setModelData(self, editor, model, index):
        model.setData(index, editor.toPlainText(), Qt.EditRole)

    def updateEditorGeometry(self, editor, option, index):
        editor.setGeometry(option.rect)


class DictionaryView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.df = None
        self.current_mod = None

        main_layout = QHBoxLayout(self)
        left_layout = QVBoxLayout()
        right_layout = QVBoxLayout()

        buttons_layout = QHBoxLayout()
        self.import_button = ActionButton('Import', on_click=self.on_import_clicked)
        self.export_button = ActionButton('Export', on_click=self.on_export_clicked)
        buttons_layout.addWidget(self.import_button)
        buttons_layout.addWidget(self.export_button)
        left_layout.addLayout(buttons_layout)

        self.mods_list = QListWidget()
        self.mods_list.setFixedWidth(200)
        self.mods_list.itemClicked.connect(self.on_mod_selected)
        left_layout.addWidget(self.mods_list)

        filter_layout = QHBoxLayout()
        self.filter_lang1 = QLineEdit()
        self.filter_lang1.setPlaceholderText('Filter Language 1')
        self.filter_lang2 = QLineEdit()
        self.filter_lang2.setPlaceholderText('Filter Language 2')
        self.filter_lang1.textChanged.connect(self.apply_filters)
        self.filter_lang2.textChanged.connect(self.apply_filters)
        filter_layout.addWidget(self.filter_lang1)
        filter_layout.addWidget(self.filter_lang2)
        right_layout.addLayout(filter_layout)

        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(['Text 1', 'Text 2', 'Language 1', 'Language 2', 'UID'])
        self.table.setEditTriggers(QAbstractItemView.AllEditTriggers)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Interactive)
        self.table.verticalHeader().setVisible(False)
        self.table.setWordWrap(True)
        delegate = TextEditDelegate(self.table)
        self.table.setItemDelegateForColumn(0, delegate)
        self.table.setItemDelegateForColumn(1, delegate)
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
        self.table.itemChanged.connect(self.on_cell_edited)
        right_layout.addWidget(self.table)

        main_layout.addLayout(left_layout)
        main_layout.addLayout(right_layout)

        self.load_mods()

    def showEvent(self, event):
        super().showEvent(event)
        self.load_mods()
        if self.current_mod:
            self.load_mod_entries()

    def load_mods(self):
        with get_session() as session:
            mods = DictionaryRepository.get_all_mod_names(session)
        self.mods_list.clear()
        for mod in sorted(mods, key=lambda x: x.lower()):
            self.mods_list.addItem(mod)

    def on_mod_selected(self, item):
        self.current_mod = item.text()
        self.load_mod_entries()

    def load_mod_entries(self):
        with get_session() as session:
            entries = DictionaryRepository.get_entries_by_mod(session, self.current_mod)
        import pandas as pd
        self.df = pd.DataFrame(entries)
        self.populate_table_from_df()

    def populate_table_from_df(self):
        self.table.blockSignals(True)
        df_filtered = self.get_filtered_df()
        self._index_map = df_filtered.index.to_list()
        self.table.setRowCount(len(self._index_map))
        for view_row, orig_idx in enumerate(self._index_map):
            row = df_filtered.loc[orig_idx]
            lang1_item = QTableWidgetItem(str(row['text_language1']))
            lang2_item = QTableWidgetItem(str(row['text_language2']))
            language1_item = QTableWidgetItem(str(row['language1']))
            language2_item = QTableWidgetItem(str(row['language2']))
            uid_item = QTableWidgetItem(str(row['uid']))
            uid_item.setFlags(uid_item.flags() & ~Qt.ItemIsEditable)
            lang1_item.setTextAlignment(Qt.AlignTop)
            lang2_item.setTextAlignment(Qt.AlignTop)
            language1_item.setTextAlignment(Qt.AlignTop)
            language2_item.setTextAlignment(Qt.AlignTop)
            uid_item.setTextAlignment(Qt.AlignTop)
            self.table.setItem(view_row, 0, lang1_item)
            self.table.setItem(view_row, 1, lang2_item)
            self.table.setItem(view_row, 2, language1_item)
            self.table.setItem(view_row, 3, language2_item)
            self.table.setItem(view_row, 4, uid_item)
        self.table.resizeRowsToContents()
        self.table.blockSignals(False)

    def get_filtered_df(self):
        if self.df is None:
            import pandas as pd
            return pd.DataFrame()
        df = self.df
        if self.filter_lang1.text():
            df = df[df['text_language1'].str.contains(self.filter_lang1.text(), case=False, na=False)]
        if self.filter_lang2.text():
            df = df[df['text_language2'].str.contains(self.filter_lang2.text(), case=False, na=False)]
        return df

    def apply_filters(self):
        self.populate_table_from_df()

    def on_cell_edited(self, item):
        view_row = item.row()
        col = item.column()
        if not hasattr(self, '_index_map') or self.df is None or col == 4:
            return
        real_row = self._index_map[view_row]
        new_value = item.text()
        if col == 0:
            self.df.at[real_row, 'text_language1'] = new_value
        elif col == 1:
            self.df.at[real_row, 'text_language2'] = new_value
        elif col == 2:
            self.df.at[real_row, 'language1'] = new_value
        elif col == 3:
            self.df.at[real_row, 'language2'] = new_value

        uid = self.df.at[real_row, 'uid']
        text1 = self.df.at[real_row, 'text_language1']
        text2 = self.df.at[real_row, 'text_language2']
        language1 = self.df.at[real_row, 'language1']
        language2 = self.df.at[real_row, 'language2']
        with get_session() as session:
            DictionaryRepository.upsert_translation(
                session=session,
                source_language=language1,
                target_language=language2,
                source_text=text1,
                target_text=text2,
                uid=uid,
                mod_name=self.current_mod,
            )

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.table.setColumnWidth(0, 550)
        self.table.setColumnWidth(1, 550)
        self.table.setColumnWidth(2, 90)
        self.table.setColumnWidth(3, 90)
        self.table.setColumnWidth(4, 150)

    def on_import_clicked(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            'Import Dictionary',
            '',
            'CSV/Excel Files (*.csv *.xlsx);;CSV Files (*.csv);;Excel Files (*.xlsx)'
        )
        if file_path:
            self.progress_dialog = ImportProgressDialog(window_text='Importing Dictionary', text='Importing dictionary...')
            pipeline = DictionaryImportPipeline(file_path=file_path)
            self.worker = PipelineWorker(pipeline)
            self.worker.finished.connect(self.on_import_finished)
            self.worker.error.connect(self.on_import_error)
            self.worker.start()
            self.progress_dialog.exec()

    def on_import_finished(self):
        self.progress_dialog.accept()
        self.load_mods()

    def on_import_error(self, tb_str):
        self.progress_dialog.reject()
        QMessageBox.critical(self, 'Import error', tb_str)

    def on_export_clicked(self):
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            'Exportar Dicionário',
            '',
            'CSV Files (*.csv);;Excel Files (*.xlsx)'
        )
        if file_path:
            self.progress_dialog = ImportProgressDialog(window_text='Exporting dictionary', text='Exporting dictionary')
            pipeline = DictionaryExportPipeline(file_path)
            self.worker = PipelineWorker(pipeline)
            self.worker.finished.connect(self.on_export_finished)
            self.worker.error.connect(self.on_export_error)
            self.worker.start()
            self.progress_dialog.exec()

    def on_export_finished(self):
        self.progress_dialog.accept()
        QMessageBox.information(self, 'Dictionary Export', 'Export finished!')

    def on_export_error(self, tb_str):
        self.progress_dialog.reject()
        QMessageBox.critical(self, 'Error on export', tb_str)
    