"""
Accounting for XFZ.

Authors: caobinbin(caobinbin@live.com)
Date:    2017/10/03

TODO:
feature: undostack
fix: error message
feature: import qunar cash
feature: import elong
feature: insert / delete row
feature: add dummy room
feature: save as
feature: header filter
feature: search

"""


from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import sys
import logging
import logging.config

from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtWidgets

import utils
import main_window


def main():
    """Main entry.
    """
    app = QtWidgets.QApplication(sys.argv)
    # i18n
    locale = QtCore.QLocale.system().name()
    logging.info('locale: {}'.format(locale))
    translator = QtCore.QTranslator()
    if translator.load('languages_' + locale, ':/'):
        app.installTranslator(translator)
    # app info
    app.setOrganizationName('caobinbin')
    app.setOrganizationDomain('binbincao.com')
    app.setApplicationName('Accounting')
    app.setApplicationVersion('1.0.0')
    app.setWindowIcon(QtGui.QIcon(':/app.png'))
    window = main_window.MainWindow()
    window.show()
    app.exec()


if __name__ == '__main__':
    logging.config.dictConfig(utils.log_conf)
    main()
