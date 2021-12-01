#include "C_encoding.h"
#include <QString>
#include <QColor>
#include <QTextCodec>
namespace DV {
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
			QTextCodec* gbk = QTextCodec::codecForName("gb2312");
			return gbk->toUnicode(str);
		}
		case ENCODING_UTF8:
		{
			QTextCodec* utf8 = QTextCodec::codecForName("UTF-8");
			return utf8->toUnicode(str);
		}
		}
	}

	/**
	* @brief  QColorToQstring  颜色转字符
	* @param  QColor & color
	* @return QT_NAMESPACE::QString
	*/
	QString QColorToQstring(QColor& color)
	{
		return QString().sprintf("%02X%02X%02X%02X", color.alpha(), color.red(), color.green(), color.blue());
	}

	/**
	* @brief  QStringToQColor 字符串转颜色
	* @param  QString colorstr
	* @return QT_NAMESPACE::QColor
	*/
	QColor QStringToQColor(QString colorstr)
	{
		std::string color = colorstr.toStdString();
		unsigned int colorR = 0, colorG = 0, colorB = 0, colorA = 0;
		int len = color.length();
		if (color.length() >= 8)
		{
			colorA = stoi(color.substr(0, 2), 0, 16);
			colorR = stoi(color.substr(2, 2), 0, 16);
			colorG = stoi(color.substr(4, 2), 0, 16);
			colorB = stoi(color.substr(6, 2), 0, 16);
		}
		QColor colorargb(colorR, colorG, colorB, colorA);
		return colorargb;
	}
};
