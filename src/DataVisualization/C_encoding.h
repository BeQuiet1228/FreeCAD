#pragma once
#ifndef CHAR_ENCODING_H_
#define CHAR_ENCODING_H_
#include "exportConfig.hpp"


#define	ENCODING_GB2312 0x01u
#define	ENCODING_UTF8	0x02u
#include"qstring.h"
#include"qcolor.h"
EXTERN_C DATA_VISUALIZATION_EXPORT QString  GetEncodingstr(const char*,unsigned int);
EXTERN_C DATA_VISUALIZATION_EXPORT QString  QColorToQstring(QColor&);
EXTERN_C DATA_VISUALIZATION_EXPORT QColor   QStringToQColor(QString colorstr);
#endif