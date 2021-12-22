# import statements

from PySide import QtGui, QtCore

# UI Class definitions

class CoordinateSystemDialog(QtGui.QDialog):
	""""""
	def __init__(self):
		super(CoordinateSystemDialog, self).__init__()
		self.initUI()
	def initUI(self):
		#
		self.Result = "Cancelled"
		self.CoordinateSystem = 'Rectangular'

		codec = QtCore.QTextCodec.codecForName("utf-8")

		# create our window
		# define window		xLoc,yLoc,xDim,yDim
		self.setGeometry(250, 250, 400, 350)
		self.setWindowTitle(codec.toUnicode("Create New Document"))
		self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
		layout=QtGui.QVBoxLayout()

		# radio buttons
		self.rectangularRadioButton = QtGui.QRadioButton(codec.toUnicode("Cartesian"),self)
		self.rectangularRadioButton.clicked.connect(self.onrectangularRadioButton)
		layout.addWidget(self.rectangularRadioButton)
		self.rectangularRadioButton.setChecked(True)

		#
		self.polarRadioButton = QtGui.QRadioButton(codec.toUnicode("Polar"),self)
		self.polarRadioButton.clicked.connect(self.onpolarRadioButton)
		layout.addWidget(self.polarRadioButton)
		self.cylindricalRadioButton = QtGui.QRadioButton(codec.toUnicode("Cylindrical"),self)
		self.cylindricalRadioButton.clicked.connect(self.oncylindricalRadioButton)
		layout.addWidget(self.cylindricalRadioButton)
		# 3D button
		self.creat3DButton = QtGui.QPushButton(codec.toUnicode('Create 3D Document'), self)
		self.creat3DButton.clicked.connect(self.onCreat3D)
		layout.addWidget(self.creat3DButton)

		# 3D button
		self.creat2DButton = QtGui.QPushButton(codec.toUnicode('Create 2D Document'), self)
		self.creat2DButton.clicked.connect(self.onCreat2D)
		layout.addWidget(self.creat2DButton)

		self.creat3DTextButton = QtGui.QPushButton(codec.toUnicode('Create 3D Text Edit'), self)
		self.creat3DTextButton.clicked.connect(self.onCreat3DTextEdit)
		layout.addWidget(self.creat3DTextButton)

		self.creat2DTextButton = QtGui.QPushButton(codec.toUnicode('Create 2D Text Edit'), self)
		self.creat2DTextButton.clicked.connect(self.onCreat2DTextEdit)
		layout.addWidget(self.creat2DTextButton)

		
		# cancel button
		self.cancelButton = QtGui.QPushButton(codec.toUnicode('Cancel'), self)
		self.cancelButton.clicked.connect(self.onCancel)
		self.cancelButton.setAutoDefault(True)
		layout.addWidget(self.cancelButton)


		self.setLayout(layout)

		self.show()
	
	def onrectangularRadioButton(self):
		self.CoordinateSystem = 'Rectangular'
		self.creat2DButton.setEnabled(True)

	def onpolarRadioButton(self):
		self.CoordinateSystem = 'Polar'
		self.creat2DButton.setEnabled(False)

	def oncylindricalRadioButton(self):
		self.CoordinateSystem = 'Cylindrical'
		self.creat2DButton.setEnabled(True)

	def onCancel(self):
		self.Result			= "Cancelled"
		self.close()
	def onCreat3D(self):
		self.Result			= "3D"
		self.close()

	def onCreat2D(self):
		self.Result = "2D"
		self.close()
	def onCreat3DTextEdit(self):
		self.Result = "3DText"
		self.close()
	def onCreat2DTextEdit(self):
		self.Result = "2DText"
		self.close()

# code ***********************************************************************************
