#include "VariateAnalysis.h"
#include <iostream>
VariateAnalysis::VariateAnalysis()
{

}

VariateAnalysis::~VariateAnalysis()
{

}
std::vector<QString> Variate::makeStringForVariates(std::vector<Variate>& variates)
{
	std::vector<QString> v;
	if (variates.size() == 0)
		return v;
	if (variates.size() <= 1)
		return variates.begin()->getValues();

	auto variate2 = variates.begin();
	auto variate1 = variate2->getValues();
	variate2++;
	for (; variate2 != variates.end(); variate2++)
	{
		variate1 = makeStringForTowVariate(variate1, variate2->getValues());
	}

	return variate1;
}

std::vector<QString> Variate::makeStringForTowVariate(const std::vector<QString> variate1, const std::vector<QString> variate2)
{
	std::vector<QString> variates;

	for (auto n = variate1.begin(); n != variate1.end(); n++)
	{
		for (auto i = variate2.begin(); i != variate2.end(); i++)
		{
			QString  temp = *n + *i;
			variates.push_back(temp);
		}
	}

	return variates;
}

/**
* @brief VariateAnalysis::Variate::getValues
* @return std::vector<std::string> 返回的每一项时 a = 1;/n 这种形式
*/
std::vector<QString> Variate::getValues()
{
	std::vector<QString> v;
	for (auto i = this->values.begin(); i != this->values.end(); i++)
	{
		QString temp = this->name + " = " + QString::number(*i) + ";\n";
		v.push_back(temp);
	}

	return v;
}

std::vector<QString> Variate::combinationStringForVariates(std::vector<Variate>& variates)
{
	std::vector<QString> m3d;
	auto iter = variates.begin();
	if (iter == variates.end())
		return m3d;
	m3d = iter->getValues();
	iter++;
	for (; iter != variates.end(); iter++)
	{
		combinationVariates(m3d,*iter);
	}

	for (auto i = m3d.begin(); i != m3d.end(); i++)
		std::cerr << i->toStdString();
	return m3d;
}

void Variate::combinationVariates(std::vector<QString>& m3d,Variate& variate)
{
	auto m3dIter = m3d.begin();
	std::vector<QString> values = variate.getValues();
	auto valueIter = values.begin();

	for (; (m3dIter != m3d.end()) && (valueIter != values.end()); 
		m3dIter++, valueIter++)
	{
		*m3dIter += *valueIter;
	}

}

/**
* @brief VariateAnalysis::analysisTextToVariate 将文本解析为变量的形式
* @param const QString & text
* @return std::vector<Variate>
*/
std::vector<Variate> VariateAnalysis::analysisTextToVariate(const QString& text)
{
	QString str = text;
	str = str.remove(QString("\n"), Qt::CaseInsensitive);
	auto list = text.split(";");

	std::vector<Variate> variates;

	for (auto i = list.begin(); i != list.end(); i++)
	{
		if (i->isNull())
			continue;
		variates.push_back(analysisOneVariate(*i));
	}
	return variates;
}

/**
* @brief VariateAnalysis::analysisOneVariate 将一行字符串解析为一个变量  
* @param const QString & str
* @return Variate
*/
Variate VariateAnalysis::analysisOneVariate(const QString& str)
{
	//用等号将文本分割为值和名字
	auto  list = str.split("=");
	if (list.size() != 2)
		throw str;
	Variate variate;
	variate.name = list.at(0);
	auto temp = list.at(1);
	//移除分号
	temp = temp.remove(";");
	list = temp.split(",");

	for (auto i = list.begin(); i != list.end(); i++)
	{
		variate.values.push_back(i->toDouble());
	}

	return variate;
}
