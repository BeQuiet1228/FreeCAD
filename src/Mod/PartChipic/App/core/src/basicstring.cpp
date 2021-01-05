#include "../basicstring.h"
#include <sstream>
namespace PM3
{
void deSpace(std::string &in0)
{
	std::string out;
	std::string in = in0;// .simplified();
    int len = in.length();
    for (int i=0;i<len;i++)
    {
        if (in[i] != ' ')
        {
            out+=in.at(i);
        }
    }
    in0 = out;
}
std::string getOutOBJName(std::string in)
{
	std::string out;
	int len = in.length();
	for (int i = len - 1; i>= 0; i--)
	{
		if (in[i] == '.')
		{
			for (int j = 0; j <= i; j++)
				out += in[j];
			out += "obj";
		}
	}
	return out;
}
std::vector<std::string> split(std::string strtem, char a)
{
	std::vector<std::string> strvec;

	std::string::size_type pos1, pos2;
	pos2 = strtem.find(a);
	pos1 = 0;
	while (std::string::npos != pos2)
	{
		strvec.push_back(strtem.substr(pos1, pos2 - pos1));

		pos1 = pos2 + 1;
		pos2 = strtem.find(a, pos1);
	}
	strvec.push_back(strtem.substr(pos1));
	return strvec;
}

std::string QStringToStdString(std::string ref)
{
    return std::string(ref);

}

std::string StdStringToQString(std::string ref)
{
	return ref;
}

std::string convertToString(int x)
{
	std::ostringstream o;
	if (o << x)
		return o.str();
	// 这儿进行一些错误处理...
	return "conversion error";

}

std::string convertToStringd(double x)
{
	std::ostringstream o;
	if (o << x)
		return o.str();
	// 这儿进行一些错误处理...
	return "conversion error";

}

std::string getStringFromFloat(float f)
{
	std::ostringstream buffer;
	buffer << f;
	return buffer.str();
}


std::string replace_str(std::string &strBig, const std::string &strsrc, const std::string &strdst)
{
	std::string::size_type pos = 0;
	std::string::size_type srclen = strsrc.size();
	std::string::size_type dstlen = strdst.size();

	while ((pos = strBig.find(strsrc, pos)) != std::string::npos)
	{
		strBig.replace(pos, srclen, strdst);
		pos += dstlen;
	}
	return strBig;
}
}
