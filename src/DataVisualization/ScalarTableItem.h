#pragma once
#include "QTableWidgetItem"
namespace DV
{
	class ScalarTableItem :public QTableWidgetItem
	{
	public:
		ScalarTableItem(double val,int type = Type);
		explicit ScalarTableItem(const QString& text, double val, int type = Type);
		explicit ScalarTableItem(const QIcon& icon, const QString& text, double val, int type = Type);
		ScalarTableItem(const ScalarTableItem& other);
		~ScalarTableItem();
	public:
		void setValue(double);
		double& getValue();
	private:
		double scalarValue;
	};
}