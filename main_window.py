"""
Main window.

Authors: caobinbin(caobinbin@baidu.com)
Date:    2017/10/03
"""


from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import sys
import os.path
import platform
import logging
import traceback

from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtWidgets

import utils
import resources
import main_statusbar
import data_panel
import month_picker


class MainWindow(QtWidgets.QMainWindow):
    """Main window.
    """

    def __init__(self, parent=None):
        """Constructor.
    
        Keyword Arguments:
            parent {QtWidgets.QWidget} -- Widget parent. (default: {None})
        """
        super(MainWindow, self).__init__(parent)
        # data
        self._settings = QtCore.QSettings()
        self._undo_stack = QtWidgets.QUndoStack(self)
        self._filename = None
        # ui
        self._create_widgets()
        self._create_actions()
        self._load_settings()
        self.setWindowTitle(QtWidgets.QApplication.instance().applicationName())

    def _create_widgets(self):
        """Create widgets.
        """
        # data panel
        self._data_model = data_panel.DataTableModel(self)
        self._data_view = data_panel.DataTableView()
        self._data_view.setModel(self._data_model)
        self._data_view.setItemDelegate(data_panel.EditDelegate(self))
        self._data_view.resizeColumnsToContents()
        self._data_model.modelReset.connect(self._data_view.resizeColumnsToContents)
        self._data_model.modelReset.connect(
            lambda : self.statusBar().set_stat(*(self._data_model.stat())))
        self._data_model.dataChanged.connect(
            lambda : self.statusBar().set_stat(*(self._data_model.stat())))
        self.setCentralWidget(self._data_view)
        # status bar
        self.setStatusBar(main_statusbar.MainStatusBar(self))

    def _create_actions(self):
        """Create actions, menubar, toolbar.
        """
        # actions
        open_action = QtWidgets.QAction(
            QtCore.QCoreApplication.translate('MainWindow', '&Open'), self)
        open_action.setShortcut(QtGui.QKeySequence.Open)
        open_action.setIcon(QtGui.QIcon(':/open.png'))
        open_action.setToolTip(
            QtCore.QCoreApplication.translate('MainWindow', 'Open Bill'))
        open_action.triggered.connect(self.on_open_action_triggered)

        new_action = QtWidgets.QAction(
            QtCore.QCoreApplication.translate('MainWindow', '&New'), self)
        new_action.setShortcut(QtGui.QKeySequence.New)
        new_action.setIcon(QtGui.QIcon(':/new.png'))
        new_action.setToolTip(
            QtCore.QCoreApplication.translate('MainWindow', 'New Bill'))
        new_action.triggered.connect(self.on_new_action_triggered)

        import_action = QtWidgets.QAction(
            QtCore.QCoreApplication.translate('MainWindow', '&Import'), self)
        import_action.setIcon(QtGui.QIcon(':/import.png'))
        import_action.setToolTip(
            QtCore.QCoreApplication.translate('MainWindow', 'Import Web Bill'))
        import_action.triggered.connect(self.on_import_action_triggered)

        save_action = QtWidgets.QAction(
            QtCore.QCoreApplication.translate('MainWindow', '&Save'), self)
        save_action.setShortcut(QtGui.QKeySequence.Save)
        save_action.setIcon(QtGui.QIcon(':/save.png'))
        save_action.setToolTip(
            QtCore.QCoreApplication.translate('MainWindow', 'Save Bill'))
        #save_action.setEnabled(False)
        #self._undo_stack.cleanChanged.connect(
        #    lambda clean: save_action.setEnabled(not clean))
        save_action.triggered.connect(self.on_save_action_triggered)

        exit_action = QtWidgets.QAction(
            QtCore.QCoreApplication.translate('MainWindow', 'E&xit'), self)
        exit_action.setShortcut(QtGui.QKeySequence.Quit)
        exit_action.setIcon(QtGui.QIcon(':/exit.png'))
        exit_action.setToolTip(QtCore.QCoreApplication.translate('MainWindow', 'Exit'))
        exit_action.triggered.connect(self.close)

        undo_action = self._undo_stack.createUndoAction(
            self, QtCore.QCoreApplication.translate('MainWindow', '&Undo'))
        undo_action.setShortcut(QtGui.QKeySequence.Undo)
        undo_action.setIcon(QtGui.QIcon(':/undo.png'))

        redo_action = self._undo_stack.createRedoAction(
            self, QtCore.QCoreApplication.translate('MainWindow', '&Redo'))
        redo_action.setShortcut(QtGui.QKeySequence.Redo)
        redo_action.setIcon(QtGui.QIcon(':/redo.png'))

        documentation_action = QtWidgets.QAction(
            QtCore.QCoreApplication.translate('MainWindow', '&Documentation'), self)
        documentation_action.setShortcut(QtGui.QKeySequence.HelpContents)
        documentation_action.setIcon(QtGui.QIcon(':/documentation.png'))
        documentation_action.setToolTip(
            QtCore.QCoreApplication.translate('MainWindow', 'Open Documentation'))
        documentation_action.triggered.connect(self.on_documentation_action_triggered)
        documentation_action.setEnabled(False)

        about_action = QtWidgets.QAction(
            QtCore.QCoreApplication.translate('MainWindow', '&About {}').format(
                QtWidgets.QApplication.instance().applicationName()), self)
        about_action.setIcon(QtGui.QIcon(':/app.png'))
        about_action.triggered.connect(self.on_about_action_triggered)

        # menu
        menu = self.menuBar().addMenu(QtCore.QCoreApplication.translate('MainWindow', '&File'))
        menu.addAction(new_action)
        menu.addAction(open_action)
        menu.addAction(save_action)
        menu.addSeparator()
        menu.addAction(exit_action)

        menu = self.menuBar().addMenu(QtCore.QCoreApplication.translate('MainWindow', '&Edit'))
        menu.addAction(undo_action)
        menu.addAction(redo_action)
        menu.addSeparator()
        menu.addAction(import_action)

        menu = self.menuBar().addMenu(QtCore.QCoreApplication.translate('MainWindow', '&Help'))
        menu.addAction(documentation_action)
        menu.addAction(about_action)

        # toolbar
        toolbar = self.addToolBar(QtCore.QCoreApplication.translate('MainWindow', 'File Toolbar'))
        toolbar.setObjectName('FileToolBar')
        toolbar.addAction(new_action)
        toolbar.addAction(open_action)
        toolbar.addAction(save_action)
        
        toolbar = self.addToolBar(QtCore.QCoreApplication.translate('MainWindow', 'Edit Toolbar'))
        toolbar.setObjectName('EditToolBar')
        toolbar.addAction(undo_action)
        toolbar.addAction(redo_action)
        toolbar.addSeparator()
        toolbar.addAction(import_action)

    def _load_settings(self):
        """Load application settings on startup.
        """
        # load main window geometry
        geometry = self._settings.value('MainWindow/Geometry')
        if geometry is not None:
            self.restoreGeometry(geometry)
        state = self._settings.value('MainWindow/State')
        if state is not None:
            self.restoreState(state)

    def _check_clean(self):
        """Check if all changes are saved.
        
        Returns:
            bool -- True if current instance is clean, False otherwise.
        """
        ret = False
        if self._undo_stack.isClean():
            ret = True
        else:
            action = QtWidgets.QMessageBox.warning(
                self, QtWidgets.QApplication.instance().applicationName(),
                QtCore.QCoreApplication.translate(
                    'MainWindow', 'Save changes before closing?'),
                QtWidgets.QMessageBox.Save
                | QtWidgets.QMessageBox.Discard
                | QtWidgets.QMessageBox.Cancel)
            if action == QtWidgets.QMessageBox.Cancel:
                ret = False
            elif action == QtWidgets.QMessageBox.Save:
                ret = self._save_instance()
            else: # QtWidgets.QMessageBox.Discard
                ret = True
        return ret

    def on_open_action_triggered(self, checked):
        """Slot for open list action.
        """
        if self._check_clean():
            last_filename = self._settings.value('File/LastFilename', '')
            filename = QtWidgets.QFileDialog.getOpenFileName(self,
                caption=QtCore.QCoreApplication.translate('MainWindow', 'Open Bill'),
                directory=os.path.dirname(last_filename),
                filter=QtCore.QCoreApplication.translate('MainWindow', 'Bill (*.csv)'))[0]
            if os.path.isfile(filename) and self._data_model.open(filename):
                self._filename = filename

    def on_new_action_triggered(self, checekd):
        """Slot for open label action.
        """
        if self._check_clean():
            dialog = month_picker.MonthPickerDialog(self)
            if dialog.exec() == QtWidgets.QDialog.Accepted:
                self._data_model.new(dialog.year(), dialog.month())
                self._filename = None

    def on_import_action_triggered(self, checked):
        last_filename = self._settings.value('File/LastImport', '')
        filenames = QtWidgets.QFileDialog.getOpenFileNames(self,
            caption=QtCore.QCoreApplication.translate('MainWindow', 'Import Web Bill'),
            directory=os.path.dirname(last_filename),
            filter=QtCore.QCoreApplication.translate('MainWindow', 'Web Bill (*.xls *.xlsx)'))[0]
        if len(filenames) > 0:
            if self._data_model.import_files(filenames):
                self.statusBar().showMessage(
                    QtCore.QCoreApplication.translate('MainWindow', 'Import Successed.'), 3000)
                self._settings.setValue('File/LastImport', filenames[0])
            else:
                self.statusBar().showMessage(
                    QtCore.QCoreApplication.translate('MainWindow', 'Import Failed.'), 3000)

    def on_save_action_triggered(self, checked=False):
        """Save current instance.
        
        Returns:
            bool -- True if save successed, False otherwise.
        """
        if self._filename is None:
            filename = QtWidgets.QFileDialog.getSaveFileName(self,
                caption=QtCore.QCoreApplication.translate('MainWindow', 'Save Bill'),
                directory=os.path.dirname(self._settings.value('File/LastFilename', '')),
                filter=QtCore.QCoreApplication.translate('MainWindow', 'Bill (*.csv)'))[0]
            if len(filename) > 0:
                self._filename = filename
        #
        if self._filename is not None:
            if self._data_model.save(self._filename):
                self.statusBar().showMessage(
                    QtCore.QCoreApplication.translate('MainWindow', 'Save Successed.'), 3000)
                self._settings.setValue('File/LastFilename', self._filename)
                return True
            else:
                self.statusBar().showMessage(
                    QtCore.QCoreApplication.translate('MainWindow', 'Save Failed.'), 3000)
                return False

    @utils.dumpargs
    def closeEvent(self, event):
        """Override. Window close event handler.
        """
        if self._check_clean():
            self._settings.setValue('MainWindow/Geometry', self.saveGeometry())
            self._settings.setValue('MainWindow/State', self.saveState())
        else:
            event.ignore()

    def on_documentation_action_triggered(self, checked):
        """Slot for documentation action.
        """
        pass

    def on_about_action_triggered(self, checked):
        """Slot for about action.
        """
        QtWidgets.QMessageBox.about(
            self, QtCore.QCoreApplication.translate('MainWindow', 'About {}').format(
                QtWidgets.QApplication.instance().applicationName()),
            ('<b>{}</b> v {}'
                '<p>Copyright &copy; 2017 Cao Binbin. All rights reserved.'
                '<p>{}'
                '<p>Python {} - Qt {} - PyQt {} on {}').format(
                    QtWidgets.QApplication.instance().applicationName(),
                    QtWidgets.QApplication.instance().applicationVersion(),
                    QtCore.QCoreApplication.translate(
                        'MainWindow',
                        'This application can be used to do accounting.'),
                    platform.python_version(),
                    QtCore.QT_VERSION_STR,
                    QtCore.PYQT_VERSION_STR,
                    platform.system()))

