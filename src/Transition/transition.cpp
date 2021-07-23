#include "transition.h"
#include <QTextCodec>
QString gbkStdstringToQstring(const std::string& str)
{
	QTextCodec* pCodec = QTextCodec::codecForName("gb2312");
	if (!pCodec) return "";

	QString qstr = pCodec->toUnicode(str.c_str(), str.length());
	return qstr;
}

/**
* @brief MessageTransition::utf8StdstringToGbkStdstring
* @param const std::string & str
* @return std::string
*/
std::string utf8StdstringToGbkSdstring(const std::string& str)
{
	auto gbk = QTextCodec::codecForName("gb2312");

	QString temp = QString::fromUtf8(str.c_str());
	std::string ret = gbk->fromUnicode(temp).data();
	return ret;
}
