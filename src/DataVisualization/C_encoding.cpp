#include "C_encoding.h"
#include <QString>
#include <QColor>
#include <QTextCodec>
/**
* @brief GetEncodingstr 获取响应的编码的字符串
* @param const char* str 原始编码的字符串
* @param unsigned int type 需要转换的编码类型
* @return QString
*/
QString GetEncodingstr(const char* str, unsigned int type)
{
	switch (type)
	{
	case ENCODING_GB2312:
	{
		QTextCodec *gbk = QTextCodec::codecForName("gb2312");
		return gbk->toUnicode(str);
	}
	case ENCODING_UTF8:
	{
		QTextCodec* utf8 = QTextCodec::codecForName("UTF-8");
		return utf8->toUnicode(str);
	}
	}
}

QString QColorToQstring(QColor& color)
{
	QRgb mRgb = qRgb(color.red(), color.green(), color.blue());
	QColor mColor = QColor(mRgb);
	QString mRgbStr = QString::number(mRgb, 16);
	return mRgbStr;
}
QColor QStringToQColor(QString colorstr)
{
	QColor color2(colorstr.toUInt(NULL, 16));
	return color2;
}