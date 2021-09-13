#pragma once
#include <memory>
#include "VariateItemWidget.h"
struct VariateData;
class VariateitemDialog :public VariateItemWidget
{
	Q_OBJECT
public :
	VariateitemDialog(QWidget* parent=nullptr);
	~VariateitemDialog();
	//…Ë÷√
	void setData(std::shared_ptr<VariateData> data);
	void initUi();
};