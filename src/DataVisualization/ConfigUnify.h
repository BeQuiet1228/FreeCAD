#pragma once
#include "exportConfig.hpp"
#include "QColor"
class QPushButton;
class QComboBox;
namespace DV
{
	class DATA_VISUALIZATION_EXPORT ConfigUnify
	{
	public:
		ConfigUnify() = default;
		virtual ~ConfigUnify() {}
	public:
		/*
			读取配置
		*/
		virtual void loadConfig() {}
		/*
			保存配置
		*/
		virtual void saveConfig() {}
	protected:
		/*
			一些派生类通用的方法
		*/
		void SetAllreRenderer(QPushButton* button);
		QColor setButtonColor(QPushButton* button);
		QColor setButtonColor(QPushButton* button, std::string color);
		QColor setButtonColor(QPushButton* button, QColor color);
		std::string getButtonColorstr(QPushButton* button);
		QColor getButtonColor(QPushButton* button);
		void toComboxIndex(QComboBox* combox, QString& str);
	};
}
#define SETPERPORE(a,b)\
	connect((a),SIGNAL(clicked()),this,SLOT(b));\
	SetAllreRenderer(a);