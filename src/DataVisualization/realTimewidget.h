#pragma once
#ifndef REALTIME_WIDGET_H_
#define REALTIME_WIDGET_H_
#include <QWidget>
namespace Ui
{
	class realTimewidget;
}
class realTimewidget :public QWidget
{
	Q_OBJECT
public:
	explicit realTimewidget(QWidget* parent = nullptr);
	~realTimewidget();
private:
	Ui::realTimewidget *ui;
};
#endif