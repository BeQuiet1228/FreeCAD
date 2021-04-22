#pragma once
#ifndef CHAR_ENCODING_H_
#define CHAR_ENCODING_H_
#include "exportConfig.hpp"
#ifdef  _cplusplus
#define EXTERN_C extern "C"
#else
#define EXTERN_C
#endif

#define	ENCODING_GB2312 0x01u
#define	ENCODING_UTF8	0x02u

class QString;
QString EXTERN_C DATA_VISUALIZATION_EXPORT GetEncodingstr(const char*,unsigned int);
#endif