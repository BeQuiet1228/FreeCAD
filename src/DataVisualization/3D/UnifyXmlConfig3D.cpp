#include "UnifyXmlConfig3D.h"
DV3D::UnifyXmlConfig3D::ColorF DV3D::UnifyXmlConfig3D::getColors(std::string colorStr)
{
	ColorF colorf;
	int len = colorStr.length();
	unsigned int colorR = 0, colorG = 0, colorB = 0, colorA = 0;
	if (len >= 8)
	{
		colorA = stoi(colorStr.substr(0, 2), 0, 16);
		colorR = stoi(colorStr.substr(2, 2), 0, 16);
		colorG = stoi(colorStr.substr(4, 2), 0, 16);
		colorB = stoi(colorStr.substr(6, 2), 0, 16);
		colorf.a = colorA / 255.0;
		colorf.r = colorR / 255.0;
		colorf.g = colorG / 255.0;
		colorf.b = colorB / 255.0;
	}
	return colorf;
}

std::vector<DV3D::UnifyXmlConfig3D::ColorF> DV3D::UnifyXmlConfig3D::getColors(std::vector<float>& values, std::vector<ColorF>& colors, int black/*=255*/)
{
	std::vector<ColorF> newColors;
	newColors.reserve(black);
	newColors.push_back(colors[0]);
	auto index = 0;
	for (auto i = 1; i < black; ++i)
	{
		/*
			获取值的范围
		*/
		//auto index = 0;
		while (i > values[index++] * black);
		index--;
		auto nextcolor = colors[index];
		auto lastcolor = colors[index - 1];
		auto nextvalue = values[index] * black;
		auto lastvalue = values[index - 1] * black;
		/*
			开始计算颜色值
		*/
		//获取比例
		auto step = (i - lastvalue) / (nextvalue - lastvalue);
		ColorF temp;
		temp.r = (nextcolor.r - lastcolor.r) * step+lastcolor.r;
		temp.g = (nextcolor.g - lastcolor.g) * step+lastcolor.g;
		temp.b = (nextcolor.b - lastcolor.b) * step+lastcolor.b;
		temp.a = (nextcolor.a - lastcolor.a) * step+lastcolor.a;
		newColors.push_back(temp);
	}
	return newColors;
}

