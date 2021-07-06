#include "AxisLable.h"
#include <QLineEdit>
#include <QValidator>
#include <QRegExpValidator>
#include <QGridLayout>
#include <QLabel>
#include <QCloseEvent>
AxisLable::AxisLable(QWidget* parent) :QDialog(parent)
{
	initUI();
}
AxisLable::~AxisLable()
{

}
void AxisLable::initUI()
{
	//最小值
	QRegExp rx("^(-?|\\d)(\\d+)?(\\.\\d+)?$");
	QValidator * validator = new QRegExpValidator(rx, this);
	minLineedit = new QLineEdit();
	minLineedit->setValidator(validator);
	minLineedit->setObjectName("minLineEdit");
	minLineedit->setStyleSheet(
		"QLineEdit#minLineEdit{"
		"color:blue;"
		"border:1px solid #0000ff;"
		"border-radius:6px;"
		"}");
	minLineedit->setAlignment(Qt::AlignCenter);
	//最大值
	maxLineedit = new QLineEdit();
	maxLineedit->setValidator(validator);
	maxLineedit->setObjectName("maxLineEdit");
	maxLineedit->setStyleSheet(
		"QLineEdit#maxLineEdit{"
		"color:red;"
		"border:1px solid #ff0000;"
		"border-radius:6px;"
		"}"
		);
	maxLineedit->setAlignment(Qt::AlignCenter);
	//刻度
	AxisUnitedit = new QLineEdit();
	AxisUnitedit->setObjectName("axisunitEdit");
	AxisUnitedit->setStyleSheet(
		"QLineEdit#axisunitEdit{"
		"color:black;"
		"border:1px solid #000000;"
		"border-radius:6px;"
		"}"
		);
	AxisUnitedit->setAlignment(Qt::AlignCenter);
	mQGridLayout = new QGridLayout(this);
	QLabel* lable1 = new QLabel(this);
	lable1->setText("minLineedit:");
	mQGridLayout->addWidget(lable1, 0, 0);
	mQGridLayout->addWidget(minLineedit,0,1);
	QLabel* label2 = new QLabel(this);
	label2->setText("maxLineedit:");
	mQGridLayout->addWidget(label2, 1, 0);
	mQGridLayout->addWidget(maxLineedit,1,1);
	QLabel* label3 = new QLabel(this);
	label3->setText("AxisUnitedit:");
	//mQGridLayout->addWidget(label3, 2, 0);
	//mQGridLayout->addWidget(AxisUnitedit,2,1);
}
void AxisLable::setMinval(QString str){
	minLineedit->setText(str);
}
void AxisLable::setMaxval(QString str){
	maxLineedit->setText(str);
}
void AxisLable::setAxisUnitval(QString str){
	AxisUnitedit->setText(str);
}
double AxisLable::getMinval(){
	QString minval = minLineedit->text();
	return (minval.toDouble());
}
double AxisLable::getMaxval(){
	QString maxval = maxLineedit->text();
	return (maxval.toDouble());
}
QString AxisLable::getAxisUnitval(){
	return AxisUnitedit->text();
}
void AxisLable::closeEvent(QCloseEvent * e)
{
	emit signalCloseEvent();
	e->ignore();
}
#include "moc_AxisLable.cpp"