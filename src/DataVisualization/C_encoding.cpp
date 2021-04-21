#include "C_encoding.h"
#include <QString>
#include <QTextCodec>
QString GetEncodingstr(QString str, unsigned int type)
{
	QString res;
	switch (type)
	{
	case ENCODING_GB2312:
	{

		QTextCodec *gbk = QTextCodec::codecForName("GB18030");
		res=gbk->toUnicode(str.toLocal8Bit());

	}
	case ENCODING_UTF8:
	{
		QTextCodec *utf8 = QTextCodec::codecForName("UTF-8");
		res = utf8->toUnicode(str.toUtf8());
	}
	}
	return res;
}