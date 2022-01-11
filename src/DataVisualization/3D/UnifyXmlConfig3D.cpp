#include "UnifyXmlConfig3D.h"
DV3D::UnifyXmlConfig3D::ColorF DV3D::UnifyXmlConfig3D::getColors(std::string colorStr)
{
	ColorF colorf;
	int len = colorStr.length();
	unsigned int colorR = 0, colorG = 0, colorB = 0, colorA = 0;
	if (len>=8)
	{
		colorA = stoi(colorStr.substr(0, 2), 0, 16);
		colorR = stoi(colorStr.substr(2, 2), 0, 16);
		colorG = stoi(colorStr.substr(4, 2), 0, 16);
		colorB = stoi(colorStr.substr(6, 2), 0, 16);
		colorf.a=colorA/255.0;
		colorf.r=colorR/255.0;
		colorf.g=colorG/255.0;
		colorf.b=colorB/255.0;
	}
	return colorf;
}

