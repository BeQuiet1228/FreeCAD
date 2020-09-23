#pragma once
#include <vector>
#include <QString>
#include <QStringList>
class Variate
{
public:
	Variate(){};
	~Variate(){};
	//变量名
	QString name;
	//变量值
	std::vector<QString> values;
	//获取变量所有的值
	std::vector<QString> getValues();
	//穷举出多个变量的值的所有组合
	static std::vector<QString> makeStringForVariates(std::vector<Variate>& variates);
	//穷举出两组字符串的所有组合
	static std::vector<QString> makeStringForTowVariate(const std::vector<QString> variate1, const std::vector<QString> variate2);

	//添加值
	void addValue(const std::string& t){
		values.push_back(QString::fromLocal8Bit(t.c_str()));
	}
	void addValue(const QString& t){
		values.push_back(t);
	}
};

class VariateAnalysis
{
public:
	VariateAnalysis();
	~VariateAnalysis();

	static std::vector<Variate> analysisTextToVariate(const QString& text);

private:
	//解析一行变量
	static Variate analysisOneVariate(const QString& str);
};
