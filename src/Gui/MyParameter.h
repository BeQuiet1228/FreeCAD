#ifndef GUI_MYPARAMETER_H
#define GUI_MYPARAMETER_H
#include "PreCompiled.h"

#include <QDialog>
#include <QTableWidget>
#include <QLineEdit>
#include "FCConfig.h"
#include "SpinBox.h"
//#include "propertyeditor/PropertyEditor.h"

class MyParameter : public QDialog {
	Q_OBJECT

public:
	MyParameter(QWidget* parent = nullptr);
	~MyParameter();

public:
	QTableWidget* tableWidget;
	Gui::IntSpinBox* mySpinBox;
	QLineEdit* le1;
	QLineEdit* le2;
	//Gui::PropertyEditor::PropesrtyEditor* myEidt;


private Q_SLOTS:
	void cellDoubleClicked(int row, int column);
	void textChanged(const QString& text);
};

#endif // GUI_MYPARAMETER_H
