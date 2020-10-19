#pragma once
#include <QWidget>
#include <memory>
struct VariateData;
namespace Ui {
	class VariateIteamWidget_UI;
} // namespace Ui
class VariateItemWidget:public QWidget{

public:
	VariateItemWidget(QWidget *parent = 0);
	~VariateItemWidget();
	//ÉèÖÃÊı¾İ
	void setData(std::shared_ptr<VariateData> data);
private:
	Ui::VariateIteamWidget_UI *ui;
};