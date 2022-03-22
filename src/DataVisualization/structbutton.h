#pragma once
#include "QPushButton"
class StructButton :public QPushButton
{
public:
	explicit StructButton(QWidget* parent = 0);
	explicit StructButton(const QString& text, QWidget* parent = 0);
	StructButton(const QIcon& icon, const QString& text, QWidget* parent = 0);
	~StructButton();
public:
	enum StructType
	{
		LINE = 0,
		BLACK
	};
	enum StructTexture
	{
		//真空
		VACUO = 0,
		//理想导体
		PERFECTCONDUCTOR = 3,
		//电导新材料
		CONDUCTORNEW = 8,
		//介质
		DIOLECTRIC = 4,
		//电介质和电导
		DIELECTIRANDCONDUCTANCE = 16,
		//磁导率
		PERMEABILITY = 32,
		//
		FREESPACE = 64,
		//
		FOIL = 128,

		//线段
		PORT,
		DRIVER,
		INDUCTOR

	};
	void setStructType(StructType, StructTexture);
	StructType GetStructType();
	StructTexture GetStructTexture();
private:
	StructType structtype;
	StructTexture structtexture;
};