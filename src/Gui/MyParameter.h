#ifndef GUI_MYPARAMETER_H
#define GUI_MYPARAMETER_H
#include "PreCompiled.h"

#include <unordered_map>
#include <QDialog>
#include <QTableWidget>
#include <QLineEdit>
#include "FCConfig.h"
#include "SpinBox.h"
#include <Base/Unit.h>
#include <CJsonObject.hpp>
#include <qmenubar.h>
#include <qmenu.h>
#include <map>
//#include "propertyeditor/PropertyEditor.h"

static QDockWidget* MyparamDockWidget;

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

	int getNum = 1;//存储当前所在行数
	int insertDirection = 0;//0代表insert下一行，-1代表insert上一行
	DlgChangeNameDialog* replace_name;

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

private:
	/*
	* FreeCAD中使用的默认单位不能用于变量名使用
	* 这里先初始化一个单位字符列表
	*/
	std::map<std::string, int> unitMap;
	void initUnit();
	bool isUnit(const std::string& parName);
	void showNameErorrDailog(const std::string& parName);
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
	void findStringToReplace();//找到对应string替换为相应的string
	void slotCustomContextMenu(QPoint);//dockWidget的右键菜单的创建
	void insertParaDirectionToUp();//向上insertParameter
	void insertParaDirectionToDown();//向下insertParameter
	//以下为新增的replace的slot函数
	void replaceAllString();
	void replaceOneString();
	void findLastFromLastName();
	void findNextFromLastName();
	void closeReplaceDlg();
	void copyParam();
	

public:
	//属性用于替换功能
	std::string lastName;
	std::string afterName;
	std::vector<QTextCursor> cursorLocation;
	void replaceBtnisEnable(bool);

public:
	//存储初始参数列表信息
	std::unordered_map<std::string, std::string> paramValueMap;
	QString getValueFromName(param_type cur_type, const QString& name);
	void setTypeToItem(param_type cur_type, int row);
	bool isBooleanFresh();
	std::vector<std::string> updateParamValueMap();		//只更新map时可不接受返回值
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
	//增添菜单栏功能
	QMenuBar* mBar;
	QMenu* fileMenu;
	QAction* replaceAction;

	void setupUi(QWidget* Widget)
	{
		if (Widget->objectName().isEmpty())
			Widget->setObjectName(QString::fromUtf8("Widget"));
		Widget->resize(800, 600);
		gridLayout = new QGridLayout(Widget);
		gridLayout->setObjectName(QString::fromUtf8("gridLayout"));

		//添加菜单栏
		mBar = new QMenuBar;
		fileMenu = new QMenu(Widget);
		replaceAction = new QAction(Widget);
		mBar->setAutoFillBackground(0);
		fileMenu->setObjectName(QString::fromUtf8("File"));
		fileMenu->addAction(replaceAction);
		mBar->addMenu(fileMenu);


		gridLayout->addWidget(mBar, 0, 0, 1, 1);

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
		fileMenu->setTitle(QCoreApplication::translate("Widget", "File Menu", nullptr));
		replaceAction->setText(QCoreApplication::translate("Widget", "Replace", nullptr));
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
	QAction* returnReplaceBtn();
	void printError(int);//添加外部可访问ui的接口
	void findStringToHilight(std::string);//找到对应string标记为red

	Ui::Widget* ui;
};
#endif // GUI_MYPARAMETER_H
