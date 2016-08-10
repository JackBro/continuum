# -*- coding: utf-8 -*-
"""
    This file is part of the continuum IDA PRO plugin (see zyantific.com).

    The MIT License (MIT)

    Copyright (c) 2016 Joel Hoener <athre0z@zyantific.com>

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:
    The above copyright notice and this permission notice shall be included in all
    copies or substantial portions of the Software.
    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
    SOFTWARE.
"""
from __future__ import absolute_import, print_function, division

import os
from PyQt5 import uic
from PyQt5.QtWidgets import QFileDialog, QListWidgetItem


ui_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'ui')
Ui_ProjectCreationDialog, ProjectCreationDialogBase = uic.loadUiType(
    os.path.join(ui_dir, 'ProjectCreationDialog.ui')
)


class ProjectCreationDialog(ProjectCreationDialogBase):
    def __init__(self):
        super(ProjectCreationDialog, self).__init__()

        self._ui = Ui_ProjectCreationDialog()
        self._ui.setupUi(self)

        self._ui.browse_project_path.clicked.connect(self._browse_project_path)
        self._ui.project_path.textChanged.connect(self.update_binary_list)
        self._ui.file_patterns.textChanged.connect(self.update_binary_list)

    def _browse_project_path(self):
        path = QFileDialog.getExistingDirectory()
        path = os.path.realpath(path)
        self._ui.project_path.setText(path)

    def update_binary_list(self, *_):
        from . import find_project_files

        binaries = find_project_files(
            self._ui.project_path.text(),
            self._ui.file_patterns.text(),
        )

        self._ui.binary_list.clear()
        for cur_binary in binaries:
            item = QListWidgetItem(cur_binary)
            self._ui.binary_list.addItem(item)