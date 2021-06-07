#include "DataInformationGetter.h"
#include <QString>
#include <QRegExp>
#include <QStringList>
std::string DataInformationGetter::getObserveObejct(const std::string& head)
{
	QString str = QString::fromStdString(head);
	QStringList sl = str.split("=");
	if (sl.size() < 2)
		return " ";
	str = sl.at(1);
	sl = str.split("-#");
	str = sl.at(0);
	str = str.simplified();

	return str.toStdString();
}

std::string DataInformationGetter::getObserveFace(const std::string& head)
{
	std::string face;
	//匹配观测面
	QRegExp rx("\\(.*\\)");
	QString str = QString::fromStdString(head);
	rx.setMinimal(true);
	QStringList list;
	int pos = 0;

	while ((pos = rx.indexIn(str, pos)) != -1) {
		list << rx.cap(0);
		pos += rx.matchedLength();
	}
	for (auto iter = list.begin(); iter != list.end(); iter++)
	{
		face += iter->toStdString() + "  ";
	}

	return face;
}

std::string DataInformationGetter::getObserveTime(const std::string& head)
{
	//匹配观测面
	QRegExp rx("TIME.*SEC");
	QString str = QString::fromStdString(head);
	rx.setMinimal(true);
	QStringList list;
	int pos = 0;

	while ((pos = rx.indexIn(str, pos)) != -1) {
		list << rx.cap(0);
		pos += rx.matchedLength();
	}
	
	if (list.size() == 0)
		return "";

	str = list.at(0);
	str = str.remove("TIME");
	str = str.remove("SEC");
	str = str.simplified();
	return str.toStdString();
}

