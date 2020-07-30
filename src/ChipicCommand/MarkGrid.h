#pragma  once
#include  "CommandObject.h"
class MarkGrid :public CommandObject
{
public:
	MarkGrid();
	~MarkGrid();
public:
	//网格划分对象的名称
	std::string name;
	//网格划分值
	std::string value1, value2, value3;
	//网格划分选项
	bool  check1, check2, check3;
	bool miniMum1, miniMum2, miniMum3;
	bool midMum1, midMum2, midMum3;
	bool maxMum1, maxMum2, maxMum3;
public:
	std::string toCommand() override;
	bool fromCommand(const std::string& command) override;

	//设置网格划分值
	void setValue(const std::string& value1, const std::string& value2, const std::string& value3);

private:
	//生成mini max mid 对应的字段
	std::string makeMidCommand(const bool& mini, const bool& mid, const bool& max);
	//生成一条mark
	std::string makeMark(const std::string& direction,const std::string& value,const bool& mini,const bool& mid,const bool& max);
};