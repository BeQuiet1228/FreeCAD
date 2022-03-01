from PySide.QtGui import QComboBox, QStyledItemDelegate

class StyledComboBox(QComboBox):
    def __init__(self, parent=None):
        super(StyledComboBox, self).__init__(parent)
        self.setItemDelegate(QStyledItemDelegate(self))
