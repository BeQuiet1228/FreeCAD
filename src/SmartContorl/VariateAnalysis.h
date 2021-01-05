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
	std::vector<double> values;
	//获取变量所有的值
	std::vector<QString> getValues();
	//把变量成对的组合起来
	static std::vector<QString> combinationStringForVariates(std::vector<Variate>& variates);
	//把两个变量成对的组合起来
	static void combinationVariates(std::vector<QString>& m3d,Variate& variate);
	//穷举出多个变量的值的所有组合
	static std::vector<QString> makeStringForVariates(std::vector<Variate>& variates);
	//穷举出两组字符串的所有组合
	static std::vector<QString> makeStringForTowVariate(const std::vector<QString> variate1, const std::vector<QString> variate2);

	//添加值
	void addValue(const std::string& t){
		values.push_back(std::stod(t));
	}
	void addValue(const QString& t){
		values.push_back(t.toDouble());
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
