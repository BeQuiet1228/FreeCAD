
#include "Command.h"
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
#include "time.h"
#include "DlgInsertParamImp.h"
#include "DlgDeleteParamImp.h"
#include "DlgChangeParamNameImp.h"
#include "AboutParameter.h"
#include "dlgchangenamedialog.h"
#include <sstream>


//#include "DlgExpressionInput.h"

//using namespace Gui;
using namespace App;
//using namespace Base;

MyParameter::MyParameter(QWidget* parent) : QWidget(parent) {
    this->param_m3d = new neb::CJsonObject();
    if (this->objectName().isEmpty())
        this->setObjectName(QString::fromUtf8("Dialog"));
    this->resize(800, 600);
    tableWidget = new QTableWidget(this);
    tableWidget->setObjectName(QString::fromUtf8("tableWidget"));
    tableWidget->setGeometry(QRect(100, 500, 800, 800));
    //tableWidget->horizontalHeader().setStretchLastSection(true);
    tableWidget->setColumnCount(5);
    QStringList headerLabels = (QStringList() << QString::fromStdString("name")
        << QString::fromStdString("expression")
        << QString::fromStdString("value")
        << QString::fromStdString("type")
        << QString::fromStdString("description"));
    tableWidget->setHorizontalHeaderLabels(headerLabels);
    tableWidget->horizontalHeader()->setResizeMode(QHeaderView::Stretch);
    this->recoveryData();

    //右键属性菜单
    tableWidget->setContextMenuPolicy(Qt::CustomContextMenu);
    QObject::connect(this->tableWidget, SIGNAL(customContextMenuRequested(const QPoint&)), this, SLOT(slotCustomContextMenu(QPoint)));

    QObject::connect(this->tableWidget, SIGNAL(cellChanged(int, int)), this, SLOT(cellDoubleClicked(int, int)));
    //QObject::connect(this, SIGNAL(visibilityChanged(bool)), this, SLOT(updateM3D()));

    this->addNewLine(0);

    gl = new QGridLayout(this);
    gl->setObjectName(QString::fromUtf8("gridLayout"));
    vbl = new QVBoxLayout();
    vbl->setObjectName(QString::fromUtf8("verticalLayout"));

    vbl->addWidget(tableWidget);
    gl->addLayout(vbl, 0, 0, 1, 2);

    batch_btn = new QPushButton(this);
    batch_btn->setObjectName(QString::fromUtf8("batch_btn"));
    batch_btn->setText(QString::fromUtf8("batch processing"));
    QObject::connect(this->batch_btn, SIGNAL(clicked(bool)), this, SLOT(importTextInterFace()));

    insert_btn = new QPushButton(this);
    insert_btn->setObjectName(QString::fromUtf8("insert_btn"));
    insert_btn->setText(QString::fromUtf8("insert param"));
    QObject::connect(this->insert_btn, SIGNAL(clicked(bool)), this, SLOT(insertParam()));

    delete_btn = new QPushButton(this);
    delete_btn->setObjectName(QString::fromUtf8("delete_btn"));
    delete_btn->setText(QString::fromUtf8("delete param"));
    QObject::connect(this->delete_btn, SIGNAL(clicked(bool)), this, SLOT(deleteParam()));

    change_name_btn = new QPushButton(this);
    change_name_btn->setObjectName(QString::fromUtf8("change_name_btn"));
    change_name_btn->setText(QString::fromUtf8("change param name"));
    QObject::connect(this->change_name_btn, SIGNAL(clicked(bool)), this, SLOT(changeParamName()));

    updateM3D_btn = new QPushButton(this);
    updateM3D_btn->setObjectName(QString::fromUtf8("updateM3D_btn"));
    updateM3D_btn->setText(QString::fromUtf8("OK"));
    QObject::connect(this->updateM3D_btn, SIGNAL(clicked(bool)), this, SLOT(updateM3D()));

    gl->addWidget(batch_btn, 1, 0, 1, 1);
    gl->addWidget(insert_btn, 1, 1, 1, 1);
    gl->addWidget(change_name_btn, 2, 0, 1, 1);
    gl->addWidget(delete_btn, 2, 1, 1, 1);

    gl->addWidget(updateM3D_btn, 3, 0, 1, 2);
}

MyParameter::~MyParameter()
{
    //delete ui;
    delete tableWidget;
}

void MyParameter::textChanged(const QString& text) {
    param_type _type = this->typeAnalysis(text); //  表达式的类型
    switch (_type) {
    case param_type::type_float:
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
    clock_t startTime, endTime;
    this->tableWidget->blockSignals(true);
    if (column == 0) {
        //startTime = std::clock();
        this->cellChangedWithZerothColumn(row);
        //endTime = std::clock();
        //std::cerr << "column:0  ::" << (double)(endTime - startTime) / CLOCKS_PER_SEC << ";\n";
    }
    else if (column == 1) {
        //startTime = std::clock();
        this->cellChangedWithFirstColumn(row);
        //endTime = std::clock();
        //std::cerr << "column:1  ::" << (double)(endTime - startTime) / CLOCKS_PER_SEC << ";\n";
    }
    if (column < 2) {
        this->createParamM3D();
    }
    this->tableWidget->blockSignals(false);
}

// 第零列数据发生变化时
void MyParameter::cellChangedWithZerothColumn(int row) {
    if (!this->isValidWithName(row)) {
        return;
    }
    if (row == tableWidget->rowCount() - 1) {
        this->makeLineEnabled(row);
        this->addNewLine(row);
        this->addEmptyProperty(tableWidget->item(row, 0)->text());
        if (tableWidget->item(row, 0)->flags() != Qt::ItemIsSelectable | Qt::ItemIsEnabled) {
            tableWidget->item(row, 0)->setFlags(Qt::ItemIsSelectable | Qt::ItemIsEnabled);
        }
        this->tableWidget->item(row, 1)->setText(QString::fromUtf8("0"));
        this->cellChangedWithFirstColumn(row);
    }
    else if (row >= 0 && row < tableWidget->rowCount() - 1) {
        this->makeLineEnabled(row);
        this->addEmptyProperty(tableWidget->item(row, 0)->text());
        if (tableWidget->item(row, 0)->flags() != Qt::ItemIsSelectable | Qt::ItemIsEnabled) {
            tableWidget->item(row, 0)->setFlags(Qt::ItemIsSelectable | Qt::ItemIsEnabled);
        }
        this->tableWidget->item(row, 1)->setText(QString::fromUtf8("0"));
        this->cellChangedWithFirstColumn(row);
    }
}

// 第一列数据发生变化时
void MyParameter::cellChangedWithFirstColumn(int row) {
    QString name = tableWidget->item(row, 0)->text();
    QString expression = tableWidget->item(row, 1)->text();
    param_type _type = typeAnalysis(expression);
    if (this->changeProperty(_type, name, expression)) {
        this->setValueToItem(_type, name, row);
    }
    this->updateFromRowToEnd(row);
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

bool MyParameter::isValidWithName(const std::string& param_name, int row) {
    bool res = false;
    std::regex r("^[A-Za-z]\\w*$");
    //bool temp1 = !param_name.empty();
    //bool temp2 = std::regex_match(param_name, r);
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

// 变量名有效性验证
bool MyParameter::isValidWithName(const std::string& param_name) {
    bool res = false;
    std::regex r("^[A-Za-z]\\w*$");
    if ((!param_name.empty()) && (std::regex_match(param_name, r))) {
        res = true;
    }
    return res;
}


//分析表达式_expression的类型
param_type MyParameter::typeAnalysis(const QString& text) {
    DocumentObject* docObj = App::GetApplication().getActiveDocument()->getObject("Param");
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
    if (tableWidget->item(row, 1))
        tableWidget->item(row, 1)->setFlags(Qt::ItemIsEnabled | Qt::ItemIsEditable | Qt::ItemIsSelectable);
    if (tableWidget->item(row, 3))
        tableWidget->item(row, 3)->setFlags(Qt::ItemIsEnabled | Qt::ItemIsSelectable);
    if (tableWidget->item(row, 4))
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
    DocumentObject* docObj = App::GetApplication().getActiveDocument()->getObject("Param");
    if (old_type != cur_type) {
        // 移除当前属性，添加对应类型的属性
        // 移除当前属性时，是否应该考虑该属性是否发被调用过
        App::Property* prop = docObj->getPropertyByName(name.toStdString().c_str());
        if (prop) {
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
    DocumentObject* docObj = App::GetApplication().getActiveDocument()->getObject("Param");
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
    DocumentObject* docObj = App::GetApplication().getActiveDocument()->getObject("Param");
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
    DocumentObject* docObj = App::GetApplication().getActiveDocument()->getObject("Param");
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

// m3d
void MyParameter::createParamM3D() {
    int row = this->tableWidget->rowCount();
    if (row <= 0) {
        return;
    }
    std::vector<std::string> param_name;
    std::vector<std::string> param_expression;
    std::string _m3d;
    for (int i = 0; i < row - 1; ++i) {
        if (this->tableWidget->item(i, 0) && this->tableWidget->item(i, 1)) {
            param_name.push_back(this->tableWidget->item(i, 0)->text().toStdString());
            param_expression.push_back(this->tableWidget->item(i, 1)->text().toStdString());
        }
        else {
            return;
        }
    }
    if (param_name.size() != 0 && param_name.size() == param_expression.size()) {
        for (int i = 0; i < param_name.size(); ++i) {
            _m3d = _m3d + std::string(param_name[i] + " = " + param_expression[i] + ";\n\n");
        }
    }
    else {
        _m3d = "";
    }
    App::GetApplication().getActiveDocument()->Company.setValue(_m3d);
}

// 更新数据
void MyParameter::updateFromRowToEnd(int row, std::string param_name) {
    int max_row = this->tableWidget->rowCount();
    QString cur_row_name;
    if (param_name.empty()) {
        cur_row_name = tableWidget->item(row, 0)->text();    // 当前行表达式的名字
    }
    else {
        cur_row_name = QString::fromStdString(param_name);
    }
    //auto iii = findLinkWithParam(cur_row_name.toStdString(), getAllOrderedParam(), std::string());
    std::vector<std::string> changed_param = std::vector<std::string>();    // 所有修改的变量
    changed_param.push_back(cur_row_name.toStdString());
    for (int i = row + 1; i < max_row - 1; ++i) {
        bool flag_continue = true;
        QString name = tableWidget->item(i, 0)->text();
        QString expression = tableWidget->item(i, 1)->text();
        for (const auto& i : changed_param) {
            if (expression.toStdString().find(i) != std::string::npos) {
                flag_continue = false;
                break;
            }
        }
        if (flag_continue) {
            continue;
        }
        param_type _type = typeAnalysis(expression);
        if (this->changeProperty(_type, name, expression)) {
            this->setValueToItem(_type, name, i);
        }
        changed_param.push_back(name.toStdString());
    }
}

// 批量处理
std::vector<std::vector<std::string>> MyParameter::batchProcessing(std::string text) {
    std::regex annotation("[!|！][^\\n]*");
    std::regex space("\\s");
    text = std::regex_replace(text, annotation, "");
    text = std::regex_replace(text, space, "");
    size_t num = text.size();
    std::string name;
    std::string expression;
    int count = 0;
    std::vector<std::vector<std::string>> res;
    bool flag_isName = true;
    for (int i = 0; i < num; ++i) {
        if (text[i] == ';') {
            res.push_back(std::vector<std::string>({ name, expression }));
            name.clear();
            expression.clear();
            flag_isName = true;
            ++count;
        }
        else if (text[i] == '=') {
            flag_isName = false;
        }
        else {
            if (flag_isName) {
                name.push_back(text[i]);
            }
            else {
                expression.push_back(text[i]);
            }
        }
    }
    return res;
}

void MyParameter::importTextInterFace() {
    text_import = new Widget();
    text_import->show();
    QObject::connect(dynamic_cast<Widget*>(text_import)->returnBtn(), SIGNAL(clicked(bool)),
        this, SLOT(importText()));
    QObject::connect(dynamic_cast<Widget*>(text_import)->returnReplaceBtn(), SIGNAL(triggered()),
        this, SLOT(findStringToReplace()));
}

//void MyParameter::importText() {
//    clock_t startTime, endTime;
//    text_import->close();
//    startTime = clock();
//    std::vector<std::vector<std::string>> p = this->batchProcessing(dynamic_cast<Widget*>(text_import)->returnStr().toStdString());
//    endTime = clock();
//    std::cerr << (double)(endTime - startTime) / CLOCKS_PER_SEC << std::endl;
//    int cur_row = this->tableWidget->rowCount();
//    double all = 0;
//    for (int i = 0; i < p.size(); ++i) {
//        int cur_row = this->tableWidget->rowCount();
//        startTime = clock();
//        while(!this->isValidWithName(p[i][0]))
//        {
//            std::string str = p[i][0];
//            DlgChangeNameDialog* change_name = new DlgChangeNameDialog(str);
//            change_name->exec();
//            std::string temp = p[i][0];
//            if (this->isValidWithName(change_name->getName().toStdString()))
//            {
//                p[i][0] = change_name->getName().toStdString();
//                for (int i = 0; i < p.size(); i++)
//                {
//                    if (findWholeWordsOnly(p[i][1], temp))
//                    {
//                        p[i][1] = std::regex_replace(p[i][1], std::regex("\\b" + temp + "\\b"), change_name->getName().toStdString());
//                    }
//                }
//            }
//            delete change_name;
//        }
//
//        if (this->isValidWithName(p[i][0]))
//        {
//            std::string temp = p[i][0];
//            while (!isValidWithName(temp, cur_row - 1)) {
//                temp = temp + "1";
//            }
//            this->tableWidget->item(cur_row - 1, 0)->setText(QString::fromStdString(temp));
//            this->tableWidget->item(cur_row - 1, 1)->setText(QString::fromStdString(p[i][1]));
//        }
//        endTime = clock();
//        all = all + (double)(endTime - startTime) / CLOCKS_PER_SEC;
//        std::cerr << p[i][0]  << " :\t" << (double)(endTime - startTime) / CLOCKS_PER_SEC << std::endl;
//    }
//    std::cerr << all << std::endl;
//}

//暂时用来更改功能而单独copy的importText，源代码在上方
void MyParameter::importText() {
    clock_t startTime, endTime;
    startTime = clock();
    std::vector<std::vector<std::string>> p = this->batchProcessing(dynamic_cast<Widget*>(text_import)->returnStr().toStdString());
    endTime = clock();
    std::cerr << (double)(endTime - startTime) / CLOCKS_PER_SEC << std::endl;
    int cur_row = this->tableWidget->rowCount();
    double all = 0;

    int now = 0;
    while (now < p.size())
    {
        if (!this->isValidWithName(p[now][0])) {
            dynamic_cast<Widget*>(text_import)->findStringToHilight(p[now][0]);
            dynamic_cast<Widget*>(text_import)->printError(now);
            return;
        }
        ++now;
    }

    for (int i = 0; i < p.size(); ++i) {
        int cur_row = this->tableWidget->rowCount();
        startTime = clock();

        if (this->isValidWithName(p[i][0]))
        {
            std::string temp = p[i][0];
            while (!isValidWithName(temp, cur_row - 1)) {
                temp = temp + "1";
            }
            this->tableWidget->item(cur_row - 1, 0)->setText(QString::fromStdString(temp));
            this->tableWidget->item(cur_row - 1, 1)->setText(QString::fromStdString(p[i][1]));
        }
        endTime = clock();
        all = all + (double)(endTime - startTime) / CLOCKS_PER_SEC;
        std::cerr << p[i][0] << " :\t" << (double)(endTime - startTime) / CLOCKS_PER_SEC << std::endl;
    }
    text_import->close();
    std::cerr << all << std::endl;
}

void MyParameter::recoveryData() {
    std::string text = App::GetApplication().getActiveDocument()->Company.getStrValue();
    if (text.empty()) {
        return;
    }
    std::vector<std::vector<std::string>> p = this->batchProcessing(text);
    for (int i = 0; i < p.size(); ++i) {
        this->addNewLine(i);
        this->tableWidget->item(i, 0)->setText(QString::fromStdString(p[i][0]));
        this->makeLineEnabled(i);
        this->tableWidget->item(i, 1)->setText(QString::fromStdString(p[i][1]));
    }
    // 更新结果
    int max_row = this->tableWidget->rowCount();
    for (int i = 0; i < max_row; ++i) {
        QString name = tableWidget->item(i, 0)->text();
        QString expression = tableWidget->item(i, 1)->text();
        param_type _type = typeAnalysis(expression);
        if (this->changeProperty(_type, name, expression)) {
            this->setValueToItem(_type, name, i);
        }
    }
}

//插入变量
void MyParameter::insertParam() {
    this->insert_param_dlg = new InsertParamDialog();
    this->insert_param_dlg->slotSpinBox(getNum);
    this->insert_param_dlg->exec();
    QString name = this->insert_param_dlg->getName();
    int row = this->insert_param_dlg->getRow();
    if (!this->isValidWithName(name.toStdString(), row)) {
        // 变量名无效，无法插入变量，将错误信息反馈给用户
        return;
    }
    if (row >= 0 && row <= this->tableWidget->rowCount() - 1) {
        row = row + this->insertDirection;
        this->tableWidget->insertRow(row);
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
        this->tableWidget->blockSignals(true);
        tableWidget->setItem(row, 0, item_name);
        tableWidget->setItem(row, 1, item_expression);
        tableWidget->setItem(row, 2, item_value);
        tableWidget->setItem(row, 3, item_type);
        tableWidget->setItem(row, 4, item_description);
        this->tableWidget->blockSignals(false);

        tableWidget->item(row, 0)->setText(name);
    }
    delete this->insert_param_dlg;
}

// 删除变量
void MyParameter::deleteParam() {
    int row = this->tableWidget->rowCount();
    std::vector<std::string> allParamName = std::vector<std::string>();
    for (int i = 0; i < row - 1; ++i) {
        allParamName.push_back(this->tableWidget->item(i, 0)->text().toStdString());
    }
    this->delete_param_dlg = new DeleteParamDialog(this->getAllOrderedParam());
    this->delete_param_dlg->deleteSb_row(getNum);
    this->delete_param_dlg->inputAllParamName(allParamName);
    this->delete_param_dlg->inputAllOrderedParam(this->getAllOrderedParam());
    this->delete_param_dlg->exec();
    // 判断输入的变量是否有效并且需要删除
    if (this->delete_param_dlg->isNeedToDelete && this->delete_param_dlg->isDeleted()) {
        std::string delete_param = this->delete_param_dlg->getParamName();
        int p_row = 0;  // param row
        for (int i = 0; i < allParamName.size(); ++i) {
            if (delete_param == allParamName[i]) {
                p_row = i;
                break;
            }
        }
        this->tableWidget->blockSignals(true);
        this->tableWidget->removeRow(p_row);
        this->tableWidget->blockSignals(false);
        DocumentObject* docObj = App::GetApplication().getActiveDocument()->getObject("Param");
        docObj->removeDynamicProperty(delete_param.c_str());
        this->updateFromRowToEnd(p_row - 1, delete_param);
    }
    delete this->delete_param_dlg;
}

// 获取当前变量，顺序按照用户定义的顺序
std::vector<std::pair<std::string, std::string>> MyParameter::getAllOrderedParam() {
    std::vector<std::pair<std::string, std::string>> res;
    int max_row = this->tableWidget->rowCount();
    for (int i = 0; i < max_row - 1; ++i) {
        std::string name = tableWidget->item(i, 0)->text().toStdString();
        std::string expression = tableWidget->item(i, 1)->text().toStdString();
        res.push_back(std::make_pair(name, expression));
    }
    return res;
}

// 修改变量名
void MyParameter::changeParamName() {
    std::vector<std::pair<std::string, std::string>> apo = this->getAllOrderedParam();  // 所有有序的变量名
    ChangeParamNameDialog* dlg_cpn = new ChangeParamNameDialog(apo);
    dlg_cpn->changeSb_row(getNum);
    dlg_cpn->exec();
    std::string new_name = dlg_cpn->new_name;
    if (new_name.empty()) return;
    int change_row = dlg_cpn->change_row;
    std::string old_name = this->tableWidget->item(change_row, 0)->text().toStdString();
    std::string expression = this->tableWidget->item(change_row, 1)->text().toStdString();

    /*int max_row = this->tableWidget->rowCount();
    std::vector<std::string> temp;
    for (int i = 0; i < max_row - 1; i++)
    {
        QString af_expression = tableWidget->item(i, 1)->text();
        if(findWholeWordsOnly(af_expression.toStdString(), old_name));
        {
            std::string str=std::regex_replace(af_expression.toStdString(), std::regex("\\b" + old_name + "\\b"), new_name);
            QTableWidgetItem* item_expression = new QTableWidgetItem();
            tableWidget->setItem(i, 1, item_expression);
            tableWidget->item(i, 1)->setText(QString::fromStdString(str));
        }
    }*/

    if (new_name.empty() || (!this->isValidWithName(new_name, change_row))) {
        return;
    }
    // 删除当前变量
    this->tableWidget->blockSignals(true);
    this->tableWidget->removeRow(change_row);
    this->tableWidget->blockSignals(false);
    DocumentObject* docObj = App::GetApplication().getActiveDocument()->getObject("Param");
    docObj->removeDynamicProperty(old_name.c_str());
    this->updateFromRowToEnd(change_row - 1, old_name);
    // 添加新的变量
    this->tableWidget->insertRow(change_row);
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
    this->tableWidget->blockSignals(true);
    tableWidget->setItem(change_row, 0, item_name);
    tableWidget->setItem(change_row, 1, item_expression);
    tableWidget->setItem(change_row, 2, item_value);
    tableWidget->setItem(change_row, 3, item_type);
    tableWidget->setItem(change_row, 4, item_description);
    this->tableWidget->blockSignals(false);
    tableWidget->item(change_row, 0)->setText(QString::fromStdString(new_name));
    tableWidget->item(change_row, 1)->setText(QString::fromStdString(expression));

    delete dlg_cpn;
}

//更新M3D，提供用户手动按钮更新
void MyParameter::updateM3D() {
    if (GetApplication().getActiveDocument()->classID == 2) {
        Base::InterpreterSingleton python;
        python.runString("FreeCADGui.runCommand('Refresh_3D')");
        python.runString("FreeCADGui.runCommand('UpdateBooleanCommand_3D')");
        python.runString("FreeCADGui.runCommand('CreateM3D_new')");
    }
    else if (GetApplication().getActiveDocument()->classID == 3) {
        Base::InterpreterSingleton python;
        python.runString("FreeCADGui.runCommand('CreateM2D')");
    }
}

//为文本框增添替换功能
void MyParameter::findStringToReplace() {
    replace_name = new DlgChangeNameDialog();
    QTextCursor cursor = dynamic_cast<Widget*>(text_import)->ui->textEdit->textCursor();
    cursor.movePosition(QTextCursor::Start);
    dynamic_cast<Widget*>(text_import)->ui->textEdit->setTextCursor(cursor);
    //replace_name->setModal(true);//锁定当前窗口可用，其余不能点击
    replace_name->setWindowFlags(Qt::Widget | Qt::WindowStaysOnTopHint);
    replace_name->show();
    replaceBtnisEnable(0);
    QObject::connect(replace_name->returnAllreplaceBtn(), SIGNAL(clicked(bool)),
        this, SLOT(replaceAllString()));
    QObject::connect(replace_name->returnReplaceBtn(), SIGNAL(clicked(bool)),
        this, SLOT(replaceOneString()));
    QObject::connect(replace_name->returnLastBtn(), SIGNAL(clicked(bool)),
        this, SLOT(findLastFromLastName()));
    QObject::connect(replace_name->returnNextBtn(), SIGNAL(clicked(bool)),
        this, SLOT(findNextFromLastName()));
    QObject::connect(replace_name->returnCloseBtn(), SIGNAL(clicked(bool)),
        this, SLOT(closeReplaceDlg()));
}

//在TextEdit为myparameter提供replaceString的接口
void MyParameter::replaceAllString() {
    QTextCursor cursor = dynamic_cast<Widget*>(text_import)->ui->textEdit->textCursor();
    cursor.movePosition(QTextCursor::End);
    dynamic_cast<Widget*>(text_import)->ui->textEdit->setTextCursor(cursor);//移动光标到文本末尾
    this->lastName = dynamic_cast<DlgChangeNameDialog*>(replace_name)->getLastName().toStdString();
    this->afterName = dynamic_cast<DlgChangeNameDialog*>(replace_name)->getAfterName().toStdString();

    while (dynamic_cast<Widget*>(text_import)->ui->textEdit->find(QString::fromStdString(lastName), 
        QTextDocument::FindBackward | QTextDocument::FindCaseSensitively)) {//查找后一个并且区分大小写
        dynamic_cast<Widget*>(text_import)->ui->textEdit->insertPlainText(QString::fromUtf8(afterName.c_str()));
    }
    cursor.movePosition(QTextCursor::End);
    dynamic_cast<Widget*>(text_import)->ui->textEdit->setTextCursor(cursor);
}

//在TextEdit为myparameter提供replaceOneString的接口
void MyParameter::replaceOneString() {
    QTextCursor cursor = dynamic_cast<Widget*>(text_import)->ui->textEdit->textCursor();
    this->afterName = dynamic_cast<DlgChangeNameDialog*>(replace_name)->getAfterName().toStdString();
    if (this->lastName == cursor.selectedText().toStdString()) {
        dynamic_cast<Widget*>(text_import)->ui->textEdit->insertPlainText(QString::fromUtf8(this->afterName.c_str()));
        replaceBtnisEnable(0);
    }
}

//找到对话框内填入的string，标记为高亮
void MyParameter::findLastFromLastName() {
    this->lastName = dynamic_cast<DlgChangeNameDialog*>(replace_name)->getLastName().toStdString();

    if (dynamic_cast<Widget*>(text_import)->ui->textEdit->find(QString::fromStdString(this->lastName), QTextDocument::FindBackward | QTextDocument::FindCaseSensitively)) {//查找后一个
        QPalette palette = dynamic_cast<Widget*>(text_import)->ui->textEdit->palette();// 查找到后高亮显示
        palette.setColor(QPalette::Highlight, palette.color(QPalette::Active, QPalette::Highlight));
        dynamic_cast<Widget*>(text_import)->ui->textEdit->setPalette(palette);
        replaceBtnisEnable(1);
        return;
    }
    replaceBtnisEnable(0);
    QTextCursor cursor = dynamic_cast<Widget*>(text_import)->ui->textEdit->textCursor();
    cursor.movePosition(QTextCursor::Start);
    dynamic_cast<Widget*>(text_import)->ui->textEdit->setTextCursor(cursor);//移动光标到文本末尾
}

void MyParameter::findNextFromLastName() {
    this->lastName = dynamic_cast<DlgChangeNameDialog*>(replace_name)->getLastName().toStdString();

    if (dynamic_cast<Widget*>(text_import)->ui->textEdit->find(QString::fromStdString(this->lastName), QTextDocument::FindCaseSensitively)) {//查找后一个
        QPalette palette = dynamic_cast<Widget*>(text_import)->ui->textEdit->palette();// 查找到后高亮显示
        palette.setColor(QPalette::Highlight, palette.color(QPalette::Active, QPalette::Highlight));
        dynamic_cast<Widget*>(text_import)->ui->textEdit->setPalette(palette);
        replaceBtnisEnable(1);//找到对应string打开替换按钮
        return;
    }
    replaceBtnisEnable(0);
    QTextCursor cursor = dynamic_cast<Widget*>(text_import)->ui->textEdit->textCursor();
    cursor.movePosition(QTextCursor::Start);
    dynamic_cast<Widget*>(text_import)->ui->textEdit->setTextCursor(cursor);//移动光标到文本末尾
}

//替换按钮的显示和隐藏，默认为隐藏
void MyParameter::replaceBtnisEnable(bool isfind) {
    if (isfind) 
        replace_name->returnReplaceBtn()->setEnabled(true);
    else
        replace_name->returnReplaceBtn()->setEnabled(false);
}


void MyParameter::closeReplaceDlg(){
    delete replace_name;
}

//为tableWidget的右键增添菜单栏
void MyParameter::slotCustomContextMenu(const QPoint pos) {
    //获取到当前的row和col
    int row = this->tableWidget->currentItem()->row();
    int col = this->tableWidget->currentItem()->column();
    if (col == 0 && row < this->tableWidget->rowCount() - 1) {
        this->getNum = row + 1;

        //先为菜单栏添加需要的菜单选项
        QMenu* dock_menu = new QMenu(this->tableWidget);
        QAction* change_act = new QAction(QString::fromUtf8("Change Para"), this->tableWidget);
        QAction* delete_act = new QAction(QString::fromUtf8("Delete Para"), this->tableWidget);
        QMenu* insert_act = new QMenu(QString::fromUtf8("Insert Para"), this->tableWidget);
        QAction* insert_child1 = new QAction(QString::fromUtf8("Up into"), this->tableWidget);
        QAction* insert_child2 = new QAction(QString::fromUtf8("Down into"), this->tableWidget);

        dock_menu->addAction(change_act);
        dock_menu->addAction(delete_act);
        dock_menu->addMenu(insert_act);
        insert_act->addAction(insert_child1);
        insert_act->addAction(insert_child2);

        dock_menu->move(cursor().pos());
        dock_menu->show();

        connect(change_act, SIGNAL(triggered()), SLOT(changeParamName()));
        connect(delete_act, SIGNAL(triggered()), SLOT(deleteParam()));
        connect(insert_child1, SIGNAL(triggered()), SLOT(insertParaDirectionToUp()));//向上行数减一
        connect(insert_child2, SIGNAL(triggered()), SLOT(insertParaDirectionToDown()));//向下行数不变
    }
}

//用户选中向上插入参数
void MyParameter::insertParaDirectionToUp() {
    this->insertDirection = -1;
    this->insertParam();
}

//用户选中向下插入参数
void MyParameter::insertParaDirectionToDown() {
    this->insertDirection = 0;
    this->insertParam();
}


Widget::Widget(QWidget* parent)
    : QWidget(parent)
    , ui(new Ui::Widget)
{
    ui->setupUi(this);
    ui->pushButton;
}

Widget::~Widget()
{
    delete ui;
}

QPushButton* Widget::returnBtn() {
    return this->ui->pushButton;
}

//test_zz为replaceAll增加控件
QAction* Widget::returnReplaceBtn() {
    return this->ui->replaceAction;
}

QString Widget::returnStr() {
    return this->ui->textEdit->toPlainText();
}

void Widget::printError(int i) {
    const char* hintText = "Invalid parameter name:\n";
    std::string errorTextString = "\tparameter numbered: ";
    std::stringstream ss;//将int类型转为string
    std::string num;
    ss << i + 1;
    ss >> num;
    errorTextString += num + " is invalid.";

    const char* errorText = errorTextString.c_str();
    this->ui->textAnalyse->setText(QString::fromUtf8(hintText));
    this->ui->textAnalyse->append(QString::fromUtf8(errorText));
    /*
    将hintText颜色变红
    */
    QTextCursor cursor = ui->textAnalyse->textCursor();
    cursor.select(QTextCursor::LineUnderCursor);
    QTextCharFormat fmt;
    fmt.setForeground(QColor(Qt::red));
    cursor.mergeCharFormat(fmt);
}

void Widget::findStringToHilight(std::string findText) {
    /*
    每次查找获取当前光标位置，再将其移动至文本最后
    最后调用函数find
    */
    QTextCursor cursor = ui->textEdit->textCursor();
    cursor.movePosition(QTextCursor::End);
    ui->textEdit->setTextCursor(cursor);
    if (ui->textEdit->find(QString::fromStdString(findText), QTextDocument::FindBackward | QTextDocument::FindCaseSensitively)) {//查找后一个
        QPalette palette = ui->textEdit->palette();// 查找到后高亮显示
        palette.setColor(QPalette::Highlight, palette.color(QPalette::Active, QPalette::Highlight));
        ui->textEdit->setPalette(palette);
    }
}

