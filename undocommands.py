"""
Preferences dialog.

Authors: caobinbin(caobinbin@baidu.com)
Date:    2017/10/03
"""


from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from PyQt6 import QtCore
from PyQt6 import QtGui
from PyQt6 import QtWidgets


class ResetCommand(QtGui.QUndoCommand):
    """Fill undo command. Modifies the label.
    """

    def __init__(self, owner, text=None, parent=None):
        """Constructor.
        
        Arguments:
            owner {object} -- The command owner.
        
        Keyword Arguments:
            text {str} -- Command text shown in undo stack. (default: {None})
            parent {QtWidgets.QUndoCommand} -- Command parent. (default: {None})
        """
        super(ResetCommand, self).__init__(text, parent)
        self._owner = owner
        self.old_data = None
        self.new_data = None

    def undo(self):
        """Override. Revert the command.
        """
        self._owner.set_data(self.old_data.copy(deep=True))

    def redo(self):
        """Override. Apply the command.
        """
        self._owner.set_data(self.new_data.copy(deep=True))


class EditCommand(QtGui.QUndoCommand):
    """Fill undo command. Modifies the label.
    """

    def __init__(self, owner, text=None, parent=None):
        """Constructor.
        
        Arguments:
            owner {object} -- The command owner.
        
        Keyword Arguments:
            text {str} -- Command text shown in undo stack. (default: {None})
            parent {QtWidgets.QUndoCommand} -- Command parent. (default: {None})
        """
        super(EditCommand, self).__init__(text, parent)
        self._owner = owner
        self.index = None
        self.old_value = None
        self.new_value = None

    def undo(self):
        """Override. Revert the command.
        """
        self._owner.set_value(self.index, self.old_value)

    def redo(self):
        """Override. Apply the command.
        """
        self._owner.set_value(self.index, self.new_value)
