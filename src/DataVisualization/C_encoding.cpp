#include "C_encoding.h"
#include <QString>
#include <QTextCodec>
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