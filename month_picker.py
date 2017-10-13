"""
Preferences dialog.

Authors: caobinbin(caobinbin@baidu.com)
Date:    2017/10/03
"""


from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import datetime

from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtWidgets


class MonthPickerDialog(QtWidgets.QDialog):
    """Preferences dialog."""

    def __init__(self, parent=None):
        """Constructor.
        
        Keyword Arguments:
            parent {QtWidgets.QWidget} -- Widget parent. (default: {None})
        """
        super(MonthPickerDialog, self).__init__(parent)
        self.setWindowFlags(QtCore.Qt.Dialog | QtCore.Qt.MSWindowsFixedSizeDialogHint)
        self._year = datetime.date.today().year
        self._month = datetime.date.today().month
        self._create_widgets()
        self.setWindowTitle(QtCore.QCoreApplication.translate('MonthPickerDialog', 'Choose Month'))
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

    def year(self):
        return self._year

    def month(self):
        return self._month

    def set_year(self, year):
        self._year = year

    def set_month(self, month):
        self._month = month

    def _create_widgets(self):
        """Create widgets."""
        content_layout = QtWidgets.QHBoxLayout()
        content_layout.setSpacing(10)

        # year
        spinbox = QtWidgets.QSpinBox()
        spinbox.setRange(2016, 2050)
        spinbox.setSingleStep(1)
        spinbox.setValue(self._year)
        spinbox.valueChanged.connect(lambda value: self.set_year(value))
        content_layout.addWidget(spinbox, 1)

        label = QtWidgets.QLabel(
            QtCore.QCoreApplication.translate('MonthPickerDialog', 'Year'))
        label.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        content_layout.addWidget(label)

        # month
        spinbox = QtWidgets.QSpinBox()
        spinbox.setRange(1, 12)
        spinbox.setSingleStep(1)
        spinbox.setValue(self._month)
        spinbox.valueChanged.connect(lambda value: self.set_month(value))
        content_layout.addWidget(spinbox, 1)

        label = QtWidgets.QLabel(
            QtCore.QCoreApplication.translate('MonthPickerDialog', 'Month'))
        label.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        content_layout.addWidget(label)

        # button box
        buttons = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel)
        buttons.button(QtWidgets.QDialogButtonBox.Ok).setText(
            QtCore.QCoreApplication.translate('QDialogButtonBox', 'OK'))
        buttons.button(QtWidgets.QDialogButtonBox.Cancel).setText(
            QtCore.QCoreApplication.translate('QDialogButtonBox', 'Cancel'))
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)

        # layout
        layout = QtWidgets.QVBoxLayout()
        layout.addLayout(content_layout)
        layout.addWidget(buttons)
        self.setLayout(layout)
