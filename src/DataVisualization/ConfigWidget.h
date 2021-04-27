#pragma once
#ifndef CONFIG_WIDGET_H_
#define CONFIG_WIDGET_H_
#include <QWidget>
#include <QModelIndex>
#include <QStandardItemModel>
#include <map>
namespace Ui{
	class ConfigWidget;
}
class ConfigWidget:public QWidget
{
	Q_OBJECT
public:
	explicit ConfigWidget(QWidget* panter = nullptr);
	~ConfigWidget();
protected:
	void initUI();
public Q_SLOTS:
	void on_doubleclick(const QModelIndex& modindex);
private:
	QStandardItemModel *goodsModel;
	std::map <QStandardItem*,int> mapview;
private:
	Ui::ConfigWidget *ui;
};
#endif