#ifndef GUI_MYPARAMETER_H
#define GUI_MYPARAMETER_H
#include "PreCompiled.h"

#include <QDialog>
#include <QTableWidget>
#include <QLineEdit>
#include "FCConfig.h"
#include "SpinBox.h"
#include <Base/Unit.h>
//#include "propertyeditor/PropertyEditor.h"


enum param_type {type_int = 0, type_float, type_length, type_angle, type_other, type_error};

class MyParameter : public QDialog {
	Q_OBJECT

public:
	MyParameter(QWidget* parent = nullptr);
	~MyParameter();

	param_type typeAnalysis(const QString& tex);

public:
	QTableWidget* tableWidget;
	Gui::IntSpinBox* mySpinBox;
	QLineEdit* le1;
	QLineEdit* le2;
	QLineEdit* le3;
	QGridLayout* gl;
	QVBoxLayout* vbl;
	std::string error_message;

	//Base::Unit impliedUnit;
	//Gui::PropertyEditor::PropesrtyEditor* myEidt;

// 与tableWideget相关的函数
public:
	void addNewLine(int row);
	void makeLineEnabled(int row);
	bool isValidWithName(int row);
	void addEmptyProperty(const QString& name);
	bool changeProperty(param_type _type, const QString& name, const QString& expression);
	void addProperty(param_type _type, const QString& name);
	param_type getPropertyType(const QString& name);
	void setValueToItem(param_type cur_type, const QString& name, int row);

private Q_SLOTS:
	void cellDoubleClicked(int row, int column);
	void textChanged(const QString& text);
};

#endif // GUI_MYPARAMETER_H
