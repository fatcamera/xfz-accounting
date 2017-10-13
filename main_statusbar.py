"""
Status bar in main window.

Authors: caobinbin(caobinbin@baidu.com)
Date:    2017/10/03
"""


from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtWidgets

import utils


class MainStatusBar(QtWidgets.QStatusBar):
    """Status bar in main window.
    """

    def __init__(self, parent=None):
        """Constructor.
        
        Keyword Arguments:
            parent {QtWidgets.QWidget} -- Widget parent. (default: {None})
        """
        super(MainStatusBar, self).__init__(parent)
        self._stat_label = QtWidgets.QLabel(self)
        self._stat_label.setIndent(10)
        self._transfer_label = QtWidgets.QLabel(self)
        self._transfer_label.setIndent(10)
        self.addPermanentWidget(self._stat_label)
        self.addPermanentWidget(self._transfer_label)

    def set_stat(self, rooms, income, expense, share, yanyan):
        self._stat_label.setText(
            QtCore.QCoreApplication.translate(
                'MainStatusBar',
                'Room Nights: {}, Income: {:.2f}, Expense: {:.2f}, Profit: {:.2f}').format(
                rooms, income, expense, income - expense))
        self._transfer_label.setText(
            QtCore.QCoreApplication.translate(
                'MainStatusBar',
                "Yanyan's Income: {:.2f}, Neighbour's Share: {:.2f}").format(yanyan, share))
