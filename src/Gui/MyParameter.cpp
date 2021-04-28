
#include "MyParameter.h"
#include "FCConfig.h"
#include <App/Expression.h>
#include <App/Document.h>
#include <App/Application.h>
#include <App/DocumentObject.h>
#include <App/ObjectIdentifier.h>
#include <App/PropertyUnits.h>
#include <Base/BaseClass.h>
#include <DlgExpressionInput.h>
#include <QString.h>
#include <regex>

//#include "DlgExpressionInput.h"

//using namespace Gui;
using namespace App;
//using namespace Base;

MyParameter::MyParameter(QWidget* parent) : QDialog(parent){
    if (this->objectName().isEmpty())
        this->setObjectName(QString::fromUtf8("Dialog"));
    this->resize(800, 600);
    tableWidget = new QTableWidget(this);
    tableWidget->setObjectName(QString::fromUtf8("tableWidget"));
    tableWidget->setGeometry(QRect(0, 0, 800, 800));
    //tableWidget->horizontalHeader().setStretchLastSection(true);
    tableWidget->setColumnCount(5);
    QStringList headerLabels = (QStringList() << QString::fromStdString("name") 
                                              << QString::fromStdString("expression")
                                              << QString::fromStdString("value")
                                              << QString::fromStdString("type")
                                              << QString::fromStdString("description"));
    tableWidget->setHorizontalHeaderLabels(headerLabels);
    tableWidget->horizontalHeader()->setResizeMode(QHeaderView::Stretch);

    QObject::connect(this->tableWidget, SIGNAL(cellChanged(int, int)), this, SLOT(cellDoubleClicked(int, int)));

    this->addNewLine(0);

    gl = new QGridLayout(this);
    gl->setObjectName(QString::fromUtf8("gridLayout"));
    vbl = new QVBoxLayout();
    vbl->setObjectName(QString::fromUtf8("verticalLayout"));

    vbl->addWidget(tableWidget);
    gl->addLayout(vbl, 0, 0, 1, 1);
}

MyParameter::~MyParameter()
{
    //delete ui;
    delete tableWidget;
}

void MyParameter::textChanged(const QString& text) {
   param_type _type = this->typeAnalysis(text); //  表达式的类型
   switch (_type) {
   case param_type::type_float :
       le3->setText(QString::fromStdString("Number"));
       break;
   case param_type::type_angle:
       le3->setText(QString::fromStdString("Angle"));
       break;
   case param_type::type_length:
       le3->setText(QString::fromStdString("Length"));
       break;
   case param_type::type_other:
       le3->setText(QString::fromStdString("Other"));
       break;
   case param_type::type_error:
       le3->setText(QString::fromStdString("Error"));
       break;
   default:
       break;
   }
}

// 表格内容发生变化时的槽函数
void MyParameter::cellDoubleClicked(int row, int column) {
    if (column == 0) {
        if (isValidWithName(row) && row == tableWidget->rowCount() - 1) {
            this->makeLineEnabled(row);
            this->addNewLine(row);
            this->addEmptyProperty(tableWidget->item(row, 0)->text());
            if (tableWidget->item(row, 0)->flags() != Qt::ItemIsSelectable | Qt::ItemIsEnabled) {
                tableWidget->item(row, 0)->setFlags(Qt::ItemIsSelectable | Qt::ItemIsEnabled);
            }
        }
    }
    else if (column == 1){
        QString name = tableWidget->item(row, 0)->text();
        QString expression = tableWidget->item(row, 1)->text();
        param_type _type = typeAnalysis(expression);
        if (this->changeProperty(_type, name, expression)) {
            this->setValueToItem(_type, name, row);
        }    
    }
}

// 判断该行变量名是否符合规范
bool MyParameter::isValidWithName(int row) {
    bool res = false;
    std::string param_name = tableWidget->item(row, 0)->text().toStdString();
    std::regex r("^[A-Za-z]\\w*$");
    bool temp1 = !param_name.empty();
    bool temp2 = std::regex_match(param_name, r);
    if ((!param_name.empty()) && (std::regex_match(param_name, r))) {
        std::set<std::string> name_set;
        for (int i = 0; i <= row - 1; ++i) {
            name_set.insert(tableWidget->item(i, 0)->text().toStdString());
        }
        if (name_set.find(param_name) == name_set.end()) {
            res = true;
        }
    }
    return res;
}

//分析表达式_expression的类型
param_type MyParameter::typeAnalysis(const QString& text) {
    DocumentObject* docObj = App::GetApplication().getActiveDocument()->getObject("param");
    App::ObjectIdentifier p(ObjectIdentifier::parse(docObj, "justForAnalysis"));
    try {
        this->error_message.clear();    // 每次分析表达式类型都先清空error_message
        //now handle expression
        boost::shared_ptr<Expression> expr(ExpressionParser::parse(p.getDocumentObject(), text.toStdString().c_str()));

        if (expr) {
            std::string error = p.getDocumentObject()->ExpressionEngine.validateExpression(p, expr);

            if (error.size() > 0)
                throw Base::RuntimeError(error.c_str());

            PropertyQuantity* qprop = Base::freecad_dynamic_cast<PropertyQuantity>(p.getProperty());
            Base::Unit _type;

            std::unique_ptr<Expression> result(expr->eval());

            boost::shared_ptr<App::Expression> expression = expr;

            NumberExpression* n = Base::freecad_dynamic_cast<NumberExpression>(result.get());
            if (n) {
                Base::Quantity value = n->getQuantity();
                if (value.isDimensionless()) {
                    return param_type::type_float;
                }
                else {
                    _type = value.getUnit();
                    if (_type == Base::Unit::Length) {
                        return param_type::type_length;
                    }
                    else if (_type == Base::Unit::Angle) {
                        return param_type::type_angle;
                    }
                    else {
                        return param_type::type_other;
                    }
                }
            }
            else {
                //ui->msg->setText(Base::Tools::fromStdString(result->toString()));
                return param_type::type_error;
            }
        }
    }
    catch (Base::Exception& e) {
        this->error_message = e.what();
        return param_type::type_error;
    }
}

/************************************************** 与控件相关代码 ******************************************************************/

// 添加新的一行
void MyParameter::addNewLine(int row) {
    int current_row = tableWidget->rowCount();
    tableWidget->setRowCount(current_row + 1);
    // 创建新的item对象
    QTableWidgetItem* item_name = new QTableWidgetItem();

    QTableWidgetItem* item_expression = new QTableWidgetItem();
    QTableWidgetItem* item_value = new QTableWidgetItem();
    QTableWidgetItem* item_type = new QTableWidgetItem();
    QTableWidgetItem* item_description = new QTableWidgetItem();
    // 使新建行无法编辑
    item_expression->setFlags(Qt::ItemIsSelectable | Qt::ItemIsEnabled);
    item_value->setFlags(Qt::ItemIsSelectable | Qt::ItemIsEnabled);
    item_type->setFlags(Qt::ItemIsSelectable | Qt::ItemIsEnabled);
    item_description->setFlags(Qt::ItemIsSelectable | Qt::ItemIsEnabled);
    // 将item添加到tableWidget
    tableWidget->setItem(current_row, 0, item_name);
    tableWidget->setItem(current_row, 1, item_expression);
    tableWidget->setItem(current_row, 2, item_value);
    tableWidget->setItem(current_row, 3, item_type);
    tableWidget->setItem(current_row, 4, item_description);
}

// 使第row行可以编辑
void MyParameter::makeLineEnabled(int row) {
    tableWidget->item(row, 1)->setFlags(Qt::ItemIsEnabled | Qt::ItemIsEditable | Qt::ItemIsSelectable);
    tableWidget->item(row, 3)->setFlags(Qt::ItemIsEnabled | Qt::ItemIsSelectable);
    tableWidget->item(row, 4)->setFlags(Qt::ItemIsEnabled | Qt::ItemIsEditable | Qt::ItemIsSelectable);
}

// 添加一个空的属性，主要应用与添加新变量的时候
void MyParameter::addEmptyProperty(const QString& name) {
    this->addProperty(param_type::type_float, name);
}

// 修改property 
bool MyParameter::changeProperty(param_type cur_type, const QString& name, const QString& expression) {
    //1.如果类型不一致首先修改类型 
    //2.修改表达式的值
    if (expression.isEmpty()) {
        return false;
    }
    param_type old_type = getPropertyType(name);
    DocumentObject* docObj = App::GetApplication().getActiveDocument()->getObject("param");
    if (old_type != cur_type) {
        // 移除当前属性，添加对应类型的属性
        // 移除当前属性时，是否应该考虑该属性是否发被调用过
        App::Property* prop = docObj->getPropertyByName(name.toStdString().c_str());
        if (prop){
            docObj->removeDynamicProperty(name.toStdString().c_str());
        }
        this->addProperty(cur_type, name);
    }
    App::ObjectIdentifier p(ObjectIdentifier::parse(docObj, name.toStdString()));
    if (cur_type == param_type::type_other || cur_type == param_type::type_error) {
        p.setValue(expression.toStdString());
    }
    else {
        boost::shared_ptr<Expression> expr(ExpressionParser::parse(p.getDocumentObject(), expression.toStdString().c_str()));
        p.getDocumentObject()->setExpression(p, expr);
    }
    return true;
}

// 获取名为name的变量的类型
param_type MyParameter::getPropertyType(const QString& name) {
    DocumentObject* docObj = App::GetApplication().getActiveDocument()->getObject("param");
    App::ObjectIdentifier p(ObjectIdentifier::parse(docObj, name.toStdString()));
    std::string type_name = std::string(p.getProperty()->getTypeId().getName());
    if (type_name == "App::PropertyFloat") {
        return param_type::type_float;
    }
    else if (type_name == "App::PropertyAngle") {
        return param_type::type_angle;
    }
    else if (type_name == "App::PropertyDistance") {
        return param_type::type_length;
    }
    else {
        return param_type::type_other;
    }
}

// 添加名为name，类型为_type的property
void MyParameter::addProperty(param_type _type, const QString& name) {
    DocumentObject* docObj = App::GetApplication().getActiveDocument()->getObject("param");
    App::Property* prop = 0;
    try {
        switch (_type) {
        case param_type::type_float:
            prop = docObj->addDynamicProperty("App::PropertyFloat", name.toStdString().c_str());
            break;
        case param_type::type_angle:
            prop = docObj->addDynamicProperty("App::PropertyAngle", name.toStdString().c_str());
            break;
        case param_type::type_length:
            prop = docObj->addDynamicProperty("App::PropertyDistance", name.toStdString().c_str());
            break;
        case param_type::type_other:
            prop = docObj->addDynamicProperty("App::PropertyString", name.toStdString().c_str());
            break;
        case param_type::type_error:
            prop = docObj->addDynamicProperty("App::PropertyString", name.toStdString().c_str());
            break;
        default:
            break;
        }
    }
    catch (const Base::Exception& e) {
        throw Py::RuntimeError(e.what());
    }
    if (!prop) {
        std::stringstream str;
        str << "No property found of type '" << /*sType <<*/ "'" << std::ends;
        //throw Py::Exception(Base::BaseExceptionFreeCADError, str.str());
    }
}

// 将row行变量的值填写到该行的第3列，类型填写到该行的第4列
void MyParameter::setValueToItem(param_type cur_type, const QString& name, int row) {
    DocumentObject* docObj = App::GetApplication().getActiveDocument()->getObject("param");
    App::ObjectIdentifier p(ObjectIdentifier::parse(docObj, name.toStdString()));
    QString temp;
    if (cur_type == param_type::type_float || cur_type == param_type::type_length || cur_type == param_type::type_angle) {
        std::unique_ptr<Expression> result(docObj->getExpression(p).expression->eval());
        NumberExpression* value = Base::freecad_dynamic_cast<NumberExpression>(result.get());
        temp = value->getQuantity().getUserString();
    }
    else {
        App::PropertyString* param_str = dynamic_cast<App::PropertyString*>(p.getProperty());
        temp = QString::fromStdString(std::string(param_str->getValue()));
    }
    tableWidget->item(row, 2)->setText(temp);

    switch (cur_type) {
    case param_type::type_float:
        tableWidget->item(row, 3)->setText(QString::fromUtf8("float"));
        break;
    case param_type::type_angle:
        tableWidget->item(row, 3)->setText(QString::fromUtf8("angle"));
        break;
    case param_type::type_length:
        tableWidget->item(row, 3)->setText(QString::fromUtf8("length"));
        break;
    case param_type::type_other:
        tableWidget->item(row, 3)->setText(QString::fromUtf8("string"));
        break;
    case param_type::type_error:
        if (!this->error_message.empty()) {
            tableWidget->item(row, 3)->setText(QString::fromStdString(this->error_message));
        }
        else {
            tableWidget->item(row, 3)->setText(QString::fromUtf8("string"));
        }
        break;
    default:
        break;
    }
}





