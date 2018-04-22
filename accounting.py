#!/usr/bin/env python3
"""
Accounting for XFZ.

Authors: caobinbin(caobinbin@live.com)
Date:    2017/10/03

TODO:
feature: import elong, elong does not have room type.
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

    translator = QtCore.QTranslator(app)
    if translator.load('qt_' + locale, ':/') and app.installTranslator(translator):
        logging.info('system translation loaded')

    translator = QtCore.QTranslator(app)
    if translator.load('languages_' + locale, ':/') and app.installTranslator(translator):
        logging.info('app translation loaded')
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
