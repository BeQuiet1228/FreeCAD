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


enum param_type { type_int = 0, type_float, type_length, type_angle, type_other, type_error };

class InsertParamDialog;
class DeleteParamDialog;
class DlgChangeNameDialog;

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
	QPushButton* delete_btn;
	QPushButton* change_name_btn;
	QWidget* text_import;
	InsertParamDialog* insert_param_dlg;
	DeleteParamDialog* delete_param_dlg;
	DlgChangeNameDialog* change_name;
	//测试添加手动刷新M3D按钮
	QPushButton* updateM3D_btn;

	int getchangeNum = 1;

	// 与tableWideget相关的函数
public:
	void addNewLine(int row);
	void makeLineEnabled(int row);
	bool isValidWithName(int row);
	bool isValidWithName(const std::string& param_name, int row);
	bool isValidWithName(const std::string& param_name);
	void addEmptyProperty(const QString& name);
	bool changeProperty(param_type _type, const QString& name, const QString& expression);
	void addProperty(param_type _type, const QString& name);
	param_type getPropertyType(const QString& name);
	void setValueToItem(param_type cur_type, const QString& name, int row);

	void cellChangedWithZerothColumn(int row);
	void cellChangedWithFirstColumn(int row);
	std::vector<std::pair<std::string, std::string>> getAllOrderedParam();


	// 与m3d相关
public:
	void createParamM3D();

	//与数据相关
public:
	void updateFromRowToEnd(int row, std::string param_name = "");
	std::vector<std::vector<std::string>> batchProcessing(std::string text);
	void recoveryData();

private Q_SLOTS:
	void cellDoubleClicked(int row, int column);
	void textChanged(const QString& text);
	void importTextInterFace();
	void importText();
	void insertParam();
	void deleteParam();
	void changeParamName();
	void updateM3D();//新增更新M3D按钮函数
	void autoPopChangeDialog();//当用户双击已经定义的参数名时，自动弹出changgeName的对话框
	//void findStringToReplace();//找到对应string替换为相应的string
};


class Ui_Widget
{
public:
	QGridLayout* gridLayout;
	QTextEdit* textEdit;
	QPushButton* pushButton;
	//搭建新的对文本的初步分析
	QTextEdit* textAnalyse;
	QPushButton* analyseButton;
	//QToolButton* replaceButton;

	void setupUi(QWidget* Widget)
	{
		if (Widget->objectName().isEmpty())
			Widget->setObjectName(QString::fromUtf8("Widget"));
		Widget->resize(800, 600);
		gridLayout = new QGridLayout(Widget);
		gridLayout->setObjectName(QString::fromUtf8("gridLayout"));

		//添加全局替换按钮
		/*replaceButton = new QToolButton(Widget);
		replaceButton->setObjectName(QString::fromUtf8("ReplaceParameterName"));
		replaceButton->setText(QString::fromUtf8("ReplaceParameterName"));
		replaceButton->setFixedWidth(140);*/

		//gridLayout->addWidget(replaceButton, 0, 0, 1, 1);

		textEdit = new QTextEdit(Widget);
		textEdit->setObjectName(QString::fromUtf8("textEdit"));
		textEdit->setFontPointSize(10);

		gridLayout->addWidget(textEdit, 1, 0, 1, 1);

		//文本分析框，给用户提示作用
		textAnalyse = new QTextEdit(Widget);
		textAnalyse->setObjectName(QString::fromUtf8("textAnalyse"));
		textAnalyse->setFixedHeight(100);
		textAnalyse->setEnabled(false);
		textAnalyse->setFontPointSize(12);
		textAnalyse->setText(QString::fromUtf8("The invalid parameter variable names are displayed here!"));
		textAnalyse->setFontPointSize(10);
		gridLayout->addWidget(textAnalyse, 2, 0, 1, 1);

		pushButton = new QPushButton(Widget);
		pushButton->setObjectName(QString::fromUtf8("pushButton"));

		gridLayout->addWidget(pushButton, 3, 0, 1, 1);


		retranslateUi(Widget);

		QMetaObject::connectSlotsByName(Widget);
	} // setupUi

	void retranslateUi(QWidget* Widget)
	{
		Widget->setWindowTitle(QCoreApplication::translate("Widget", "Widget", nullptr));
		pushButton->setText(QCoreApplication::translate("Widget", "PushButton", nullptr));
		//replaceButton->setText(QCoreApplication::translate("Widget", "ReplaceParameterName", nullptr));
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
	QToolButton* returnToolBtn();
	void printError(int);//添加外部可访问ui的接口
	void findStringToHilight(std::string);//找到对应string标记为red
	//void replaceString(std::string, std::string, std::string);

	Ui::Widget* ui;
};
#endif // GUI_MYPARAMETER_H
