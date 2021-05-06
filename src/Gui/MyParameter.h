#ifndef GUI_MYPARAMETER_H
#define GUI_MYPARAMETER_H
#include "PreCompiled.h"

#include <QDialog>
#include <QTableWidget>
#include <QLineEdit>
#include "FCConfig.h"
#include "SpinBox.h"
#include <Base/Unit.h>
#include <CJsonObject.hpp>
//#include "propertyeditor/PropertyEditor.h"


enum param_type {type_int = 0, type_float, type_length, type_angle, type_other, type_error};

class InsertParamDialog;

class MyParameter : public QWidget {
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
	neb::CJsonObject* param_m3d;
	QPushButton* batch_btn;
	QPushButton* insert_btn;
	QWidget* text_import;
	InsertParamDialog* insert_param_dlg;

	//Base::Unit impliedUnit;
	//Gui::PropertyEditor::PropesrtyEditor* myEidt;

// 与tableWideget相关的函数
public:
	void addNewLine(int row);
	void makeLineEnabled(int row);
	bool isValidWithName(int row);
	bool isValidWithName(const std::string& param_name, int row);
	void addEmptyProperty(const QString& name);
	bool changeProperty(param_type _type, const QString& name, const QString& expression);
	void addProperty(param_type _type, const QString& name);
	param_type getPropertyType(const QString& name);
	void setValueToItem(param_type cur_type, const QString& name, int row);

	void cellChangedWithZerothColumn(int row);
	void cellChangedWithFirstColumn(int row);

// 与m3d相关
public:
	void createParamM3D();

//与数据相关
public:
	void updateFromRowToEnd(int row);
	std::vector<std::vector<std::string>> batchProcessing(std::string text);
	void recoveryData();

private Q_SLOTS:
	void cellDoubleClicked(int row, int column);
	void textChanged(const QString& text);
	void importTextInterFace();
	void importText();
	void insertParam();
};


class Ui_Widget
{
public:
	QGridLayout* gridLayout;
	QTextEdit* textEdit;
	QPushButton* pushButton;

	void setupUi(QWidget* Widget)
	{
		if (Widget->objectName().isEmpty())
			Widget->setObjectName(QString::fromUtf8("Widget"));
		Widget->resize(800, 600);
		gridLayout = new QGridLayout(Widget);
		gridLayout->setObjectName(QString::fromUtf8("gridLayout"));
		textEdit = new QTextEdit(Widget);
		textEdit->setObjectName(QString::fromUtf8("textEdit"));

		gridLayout->addWidget(textEdit, 0, 0, 1, 1);

		pushButton = new QPushButton(Widget);
		pushButton->setObjectName(QString::fromUtf8("pushButton"));

		gridLayout->addWidget(pushButton, 1, 0, 1, 1);


		retranslateUi(Widget);

		QMetaObject::connectSlotsByName(Widget);
	} // setupUi

	void retranslateUi(QWidget* Widget)
	{
		Widget->setWindowTitle(QCoreApplication::translate("Widget", "Widget", nullptr));
		pushButton->setText(QCoreApplication::translate("Widget", "PushButton", nullptr));
	} // retranslateUi

};
namespace Ui {
	class Widget : public Ui_Widget {};
} // namespace Ui

QT_BEGIN_NAMESPACE
namespace Ui { class Widget; }
QT_END_NAMESPACE

class Widget : public QWidget
{
	Q_OBJECT

public:
	Widget(QWidget* parent = nullptr);
	~Widget();
	QPushButton* returnBtn();
	QString returnStr();

	Ui::Widget* ui;
};
#endif // GUI_MYPARAMETER_H
