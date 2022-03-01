#include "structbutton.h"

StructButton::StructButton(QWidget* parent /*= 0*/)
{

}

StructButton::StructButton(const QString& text, QWidget* parent /*= 0*/)
{

}

StructButton::StructButton(const QIcon& icon, const QString& text, QWidget* parent /*= 0*/)
{

}

StructButton::~StructButton()
{

}

void StructButton::setStructType(StructType st, StructTexture stt)
{
	structtype = st;
	structtexture = stt;
}

StructButton::StructType StructButton::GetStructType()
{
	return structtype;
}

StructButton::StructTexture StructButton::GetStructTexture()
{
	return structtexture;
}
