
#include "MyParameter.h"
#include "FCConfig.h"
#include <App/Expression.h>
#include <App/Document.h>
#include <App/Application.h>
#include <App/DocumentObject.h>
#include <App/ObjectIdentifier.h>
#include <App/PropertyUnits.h>
#include <Base/BaseClass.h>
#include <Base/Unit.h>
#include <DlgExpressionInput.h>

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
    tableWidget->setGeometry(QRect(40, 40, 40, 40));
    
    
    this->cellDoubleClicked(0, 0);
    //mySpinBox->setGeometry(QRect(80, 80, 40, 40));
    //mySpinBox->show();
}

MyParameter::~MyParameter()
{
    //delete ui;
    delete tableWidget;
}

void MyParameter::textChanged(const QString& text){
    le2->setText(le1->text());
    DocumentObject* docObj = App::GetApplication().getActiveDocument()->getObject("param");
    App::ObjectIdentifier p(ObjectIdentifier::parse(docObj, "t1"));

    try {
        //now handle expression
        boost::shared_ptr<Expression> expr(ExpressionParser::parse(p.getDocumentObject(), text.toStdString().c_str()));

        if (expr) {
            std::string error = p.getDocumentObject()->ExpressionEngine.validateExpression(p, expr);

            if (error.size() > 0)
                throw Base::RuntimeError(error.c_str());

            std::unique_ptr<Expression> result(expr->eval());

            boost::shared_ptr<App::Expression> expression = expr;
            //ui->okBtn->setEnabled(true);
            //ui->msg->clear();

            NumberExpression* n = Base::freecad_dynamic_cast<NumberExpression>(result.get());
            if (n) {
                Base::Quantity value = n->getQuantity();

                if (false/*!value.getUnit().isEmpty() && value.getUnit() != impliedUnit*/)
                    throw Base::UnitsMismatchError("Unit mismatch between result and required unit");
                // 结果和所需单位不匹配
                if (value.getUnit() == Base::Unit(0, 0, 0, 0, 0, 0, 0, 0)/* && impliedUnit == Base::Unit(1, 0, 0, 0, 0, 0, 0, 0)*/) {
                    value.setValue(value.getValue() * 1.0);
                }
                //value.setUnit(impliedUnit);

                //ui->msg->setText(value.getUserString());
            }
            else
                ;
            //ui->msg->setText(Base::Tools::fromStdString(result->toString()));

        ////set default palette as we may have read text right now
        //ui->msg->setPalette(ui->okBtn->palette());
        }
    }
    catch (Base::Exception& e) {
        le2->setText(QString::fromUtf8(e.what()));
        //QPalette p(ui->msg->palette());
        //p.setColor(QPalette::WindowText, Qt::red);
        //ui->msg->setPalette(p);
        //ui->okBtn->setDisabled(true);
    }
}

void MyParameter::cellDoubleClicked(int row, int column){
    mySpinBox = new Gui::IntSpinBox(this);
    //DocumentObject* docObj = App::GetApplication().getActiveDocument()->getObject("param");
    //App::ObjectIdentifier p(ObjectIdentifier::parse(docObj, "t1"));
    char* temp_exp = "1";
    //mySpinBox->bind(p);
    //mySpinBox->setGeometry(QRect(80, 80, 100, 40));

    le1 = new QLineEdit(this);
    le1->setGeometry(QRect(80, 80, 200, 40));
    QObject::connect(le1, SIGNAL(textChanged(const QString&)), this, SLOT(textChanged(const QString&)));
    le2 = new QLineEdit(this);
    le2->setGeometry(QRect(80, 0, 200, 40));

    //PropertyQuantity* qprop = Base::freecad_dynamic_cast<PropertyQuantity>(p.getProperty());
    //Base::Unit unit;
    //unit = qprop->getUnit();
    //Gui::Dialog::DlgExpressionInput* box = new Gui::Dialog::DlgExpressionInput(p, docObj->getExpression(p).expression, unit, this);
    //box->show();

    //now handle expression
    //docObj->getExpression(p).expression
    //boost::shared_ptr<Expression> expr(ExpressionParser::parse(docObj, temp_exp));
    //cell被双击之后的槽函数
    //Gui::Dialog::DlgExpressionInput* box = new Gui::Dialog::DlgExpressionInput(getPath(), getExpression(), unit, this);
}
//Gui::Dialog::DlgExpressionInput* box = new Gui::Dialog::DlgExpressionInput(getPath(), getExpression(), unit, this);
//connect(box, SIGNAL(finished(int)), this, SLOT(finishFormulaDialog()));
//box->show();







