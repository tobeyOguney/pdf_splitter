# -*- coding: utf-8 -*-
"""
Created on Fri Sep 14 07:55:50 2018

@author: Tobey Oguney
"""

# -*- coding: utf-8 -*-
"""
Created on Wed Sep 12 16:55:30 2018

@author: Tobey Oguney
"""

import os
import sys
import main

# Modules required for GUI
import PyQt5
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from backend import interpret_query

dirname = os.path.dirname(PyQt5.__file__)
plugin_path = os.path.join(dirname, 'plugins', 'platforms')
os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = plugin_path

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(QWidget, self).__init__(parent)
        self.m_ui = main.Ui_MainWindow()
        self.m_ui.setupUi(self)

        self.page_range = dict()

        self.m_ui.file_list.setSelectionMode(QAbstractItemView.ExtendedSelection)

        self.m_ui.pin.pressed.connect(self.pin_file)
        self.m_ui.unpin.pressed.connect(self.unpin_file)
        self.m_ui.file_list.currentItemChanged.connect(self.set_page_range)
        self.m_ui.page_edit.textChanged.connect(self.update_page_range)
        self.m_ui.split_button.pressed.connect(self.split_file)
        self.m_ui.up.pressed.connect(self.move_up)
        self.m_ui.down.pressed.connect(self.move_down)

    def pin_file(self):
        self.file_urls = QFileDialog.getOpenFileNames(
            self, 'Choose PDF file(s)', os.path.expanduser('~'),
            "PDFs (*.pdf)")[0]

        items = []
        for index in range(self.m_ui.file_list.count()):
            items.append(self.m_ui.file_list.item(index))

        labels = [i.text() for i in items]

        for url in self.file_urls:
            if url not in labels:
                self.m_ui.file_list.addItem(url)
                self.page_range[url] = ''

        if not items and len(self.file_urls):
            self.m_ui.file_list.setCurrentRow(0)

    def unpin_file(self):
        listItems=self.m_ui.file_list.selectedItems()
        if not listItems: return
        if self.m_ui.file_list.count() == 1:
            self.m_ui.file_list.clear()
            return
        order = list()
        for item in listItems:
            del self.page_range[item.text()]
            order.append(self.m_ui.file_list.row(item))
            self.m_ui.file_list.takeItem(self.m_ui.file_list.row(item))

        if min(order) == self.m_ui.file_list.count(): index = self.m_ui.file_list.count() - 1
        else: index = min(order)

        self.m_ui.file_list.setCurrentRow(index)

    def set_page_range(self, item):
        if self.m_ui.file_list.count() == 1: return
        self.m_ui.page_edit.setText(self.page_range[item.text()])

    def update_page_range(self, string):
        self.page_range[self.m_ui.file_list.currentItem().text()] = string

    def split_file(self):
        message = 'Split!'
        filename = QFileDialog.getSaveFileName(self, 'Save File', os.path.expanduser('~'),
                                              "PDFs (*.pdf)")[0]
        items = []
        for index in range(self.m_ui.file_list.count()):
            items.append(self.m_ui.file_list.item(index))

        labels = [i.text() for i in items]

        try: interpret_query(labels, self.page_range, filename)
        except Exception as e:
            if filename in str(e):
                message = 'Failed: the file is in use!'

        self.m_ui.statusbar.showMessage(message, 3000)

    def move_up(self):
        if self.m_ui.file_list.currentRow() == 0:
            return
        currentRow = self.m_ui.file_list.currentRow()
        currentItem = self.m_ui.file_list.takeItem(currentRow)
        self.m_ui.file_list.insertItem(currentRow - 1, currentItem)

        self.m_ui.file_list.setCurrentRow(currentRow - 1)

    def move_down(self):
        if self.m_ui.file_list.currentRow() == self.m_ui.file_list.count():
            return
        currentRow = self.m_ui.file_list.currentRow()
        currentItem = self.m_ui.file_list.takeItem(currentRow)
        self.m_ui.file_list.insertItem(currentRow + 1, currentItem)

        self.m_ui.file_list.setCurrentRow(currentRow + 1)

if __name__ == "__main__":
    QApplication.setAttribute(Qt.AA_Use96Dpi)
    app = QApplication(sys.argv)
    form = MainWindow()
    form.show()
    app.exec_()
