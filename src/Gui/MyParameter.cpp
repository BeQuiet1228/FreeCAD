
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

    QObject::connect(this->tableWidget, SIGNAL(cellChanged(int, int)), this, SLOT(cellDoubleClicked(int, int)));

    this->addNewLine(0);
    
    
    //this->cellDoubleClicked(0, 0);
    //mySpinBox->setGeometry(QRect(80, 80, 40, 40));
    //mySpinBox->show();
}

MyParameter::~MyParameter()
{
    //delete ui;
    delete tableWidget;
}

//void MyParameter::textChanged(const QString& text){
//    le2->setText(le1->text());
//    DocumentObject* docObj = App::GetApplication().getActiveDocument()->getObject("param");
//    App::ObjectIdentifier p(ObjectIdentifier::parse(docObj, "t1"));
//
//    try {
//        //now handle expression
//        boost::shared_ptr<Expression> expr(ExpressionParser::parse(p.getDocumentObject(), text.toStdString().c_str()));
//
//        if (expr) {
//            std::string error = p.getDocumentObject()->ExpressionEngine.validateExpression(p, expr);
//
//            if (error.size() > 0)
//                throw Base::RuntimeError(error.c_str());
//
//            PropertyQuantity* qprop = Base::freecad_dynamic_cast<PropertyQuantity>(p.getProperty());
//            //impliedUnit = Base::Unit(qprop->getUnit());
//            Base::Unit impliedUnit;
//            if (qprop != 0)
//                impliedUnit = qprop->getUnit();
//            else
//                impliedUnit = Base::Unit();
//
//            std::unique_ptr<Expression> result(expr->eval());
//
//            boost::shared_ptr<App::Expression> expression = expr;
//            //ui->okBtn->setEnabled(true);
//            //ui->msg->clear();
//
//            NumberExpression* n = Base::freecad_dynamic_cast<NumberExpression>(result.get());
//            if (n) {
//                Base::Quantity value = n->getQuantity();
//                if (value.isDimensionless()) {
//                    le3->setText(QString::fromStdString("Number"));
//                }
//                else {
//                    le3->setText(value.getUnit().getTypeString());
//                }
//                if (!value.getUnit().isEmpty() && value.getUnit() != impliedUnit)
//                    throw Base::UnitsMismatchError("Unit mismatch between result and required unit");
//
//                //if (false/*!value.getUnit().isEmpty() && value.getUnit() != impliedUnit*/)
//                //    throw Base::UnitsMismatchError("Unit mismatch between result and required unit");
//                //// 结果和所需单位不匹配
//                //if (value.getUnit() == Base::Unit(0, 0, 0, 0, 0, 0, 0, 0)/* && impliedUnit == Base::Unit(1, 0, 0, 0, 0, 0, 0, 0)*/) {
//                //    value.setValue(value.getValue() * 1.0);
//                //}
//                //value.setUnit(impliedUnit);
//
//                //ui->msg->setText(value.getUserString());
//            }
//            else
//                ;
//            //ui->msg->setText(Base::Tools::fromStdString(result->toString()));
//
//        ////set default palette as we may have read text right now
//        //ui->msg->setPalette(ui->okBtn->palette());
//        }
//    }
//    catch (Base::Exception& e) {
//        le2->setText(QString::fromUtf8(e.what()));
//        le3->clear();
//        //QPalette p(ui->msg->palette());
//        //p.setColor(QPalette::WindowText, Qt::red);
//        //ui->msg->setPalette(p);
//        //ui->okBtn->setDisabled(true);
//    }
//}


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

//void MyParameter::cellDoubleClicked(int row, int column){
//    mySpinBox = new Gui::IntSpinBox(this);
//    //DocumentObject* docObj = App::GetApplication().getActiveDocument()->getObject("param");
//    //App::ObjectIdentifier p(ObjectIdentifier::parse(docObj, "t1"));
//    char* temp_exp = "1";
//    //mySpinBox->bind(p);
//    //mySpinBox->setGeometry(QRect(80, 80, 100, 40));
//
//    le1 = new QLineEdit(this);
//    le1->setGeometry(QRect(80, 0, 200, 40));
//    QObject::connect(le1, SIGNAL(textChanged(const QString&)), this, SLOT(textChanged(const QString&)));
//    //QObject::connect(le1, SIGNAL(textChanged(const QString&)), this, SLOT(typeAnalysis(const QString&)));
//    le2 = new QLineEdit(this);
//    le2->setGeometry(QRect(80, 60, 200, 40));
//
//    le3 = new QLineEdit(this);
//    le3->setGeometry(QRect(80, 120, 200, 40));
//
//    //PropertyQuantity* qprop = Base::freecad_dynamic_cast<PropertyQuantity>(p.getProperty());
//    //Base::Unit unit;
//    //unit = qprop->getUnit();
//    //Gui::Dialog::DlgExpressionInput* box = new Gui::Dialog::DlgExpressionInput(p, docObj->getExpression(p).expression, unit, this);
//    //box->show();
//
//    //now handle expression
//    //docObj->getExpression(p).expression
//    //boost::shared_ptr<Expression> expr(ExpressionParser::parse(docObj, temp_exp));
//    //cell被双击之后的槽函数
//    //Gui::Dialog::DlgExpressionInput* box = new Gui::Dialog::DlgExpressionInput(getPath(), getExpression(), unit, this);
//}
//Gui::Dialog::DlgExpressionInput* box = new Gui::Dialog::DlgExpressionInput(getPath(), getExpression(), unit, this);
//connect(box, SIGNAL(finished(int)), this, SLOT(finishFormulaDialog()));
//box->show();

// 表格内容发生变化时的槽函数
void MyParameter::cellDoubleClicked(int row, int column) {
    if (column == 0) {
        if (isValidWithName(row)) {
            this->makeLineEnabled(row);
            this->addNewLine(row);
            this->addEmptyProperty(tableWidget->item(row, 0)->text());
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
    QString param_name = tableWidget->item(row, 0)->text();
    if (param_name.isEmpty()) {
        return false;
    }
    else {
        return true;
    }
}

//分析表达式_expression的类型
param_type MyParameter::typeAnalysis(const QString& text) {
    DocumentObject* docObj = App::GetApplication().getActiveDocument()->getObject("param");
    App::ObjectIdentifier p(ObjectIdentifier::parse(docObj, "justForAnalysis"));
    try {
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
    item_expression->setFlags(Qt::ItemFlag::NoItemFlags);
    item_value->setFlags(Qt::ItemFlag::NoItemFlags);
    item_type->setFlags(Qt::ItemFlag::NoItemFlags);
    item_description->setFlags(Qt::ItemFlag::NoItemFlags);
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
    tableWidget->item(row, 3)->setFlags(Qt::ItemIsEnabled | Qt::ItemIsEditable | Qt::ItemIsSelectable);
    tableWidget->item(row, 4)->setFlags(Qt::ItemIsEnabled | Qt::ItemIsEditable | Qt::ItemIsSelectable);
}

// 添加一个新的属性
void MyParameter::addEmptyProperty(const QString& name) {
    this->addProperty(param_type::type_float, name);
}

// 修改属性类型以及表达式
bool MyParameter::changeProperty(param_type cur_type, const QString& name, const QString& expression) {
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
    boost::shared_ptr<Expression> expr(ExpressionParser::parse(p.getDocumentObject(), expression.toStdString().c_str()));
    p.getDocumentObject()->setExpression(p, expr);

    if (cur_type == param_type::type_other || cur_type == param_type::type_error) {
        p.setValue("adsasdasd");
    }
    return true;
}

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

void MyParameter::setValueToItem(param_type cur_type, const QString& name, int row) {
    DocumentObject* docObj = App::GetApplication().getActiveDocument()->getObject("param");
    App::ObjectIdentifier p(ObjectIdentifier::parse(docObj, name.toStdString()));
    std::unique_ptr<Expression> result(docObj->getExpression(p).expression->eval());
    NumberExpression* value = Base::freecad_dynamic_cast<NumberExpression>(result.get());
    QString temp = value->getQuantity().getUserString();
    try {
        switch (cur_type) {
        case param_type::type_float:
            tableWidget->item(row, 2)->setText(temp);
            break;
        case param_type::type_angle:
            tableWidget->item(row, 2)->setText(temp);
            break;
        case param_type::type_length:
            tableWidget->item(row, 2)->setText(temp);
            break;
        case param_type::type_other:
            tableWidget->item(row, 2)->setText(temp);
            break;
        case param_type::type_error:
            tableWidget->item(row, 2)->setText(temp);
            break;
        default:
            break;
        }
    }
    catch (const Base::Exception& e) {
        throw Py::RuntimeError(e.what());
    }
}





