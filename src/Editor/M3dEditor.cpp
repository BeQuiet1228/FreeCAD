#include "M3dEditor.h"
#include "M3dHightLighter.h"
#include <regex>
#include <vector>
#include <QTextIStream>
M3dEditor::M3dEditor(QWidget* parent /*= 0*/)
	:CodeEditor(parent)
{
	M3dHightLighter* highLighter = new M3dHightLighter(this->document()); 
	QFont f("Microsoft YaHei");
	f.setPointSize(12);
	this->setFont(f);

}

M3dEditor::~M3dEditor()
{


}

/**
* @brief M3dEditor::getCmds 获取命令集合
* @return Cmds
*/
Cmds M3dEditor::getCmds()
{
	analysis.setText(this->toPlainText());
	return analysis.analysisText();
}

M3dCommadAnalysis::M3dCommadAnalysis()
{
	//载入命令类型配置
	QFile file("./codeEditConfig/CommandType.txt");
	if (file.open(QIODevice::ReadOnly | QIODevice::WriteOnly))
	{
		QTextStream stream(&file);
		while (!stream.atEnd()) {
			QString line = stream.readLine();

			M3dCommandType type(line);
			this->types.push_back(type);
		}
	}
}

std::list<M3dCommand> M3dCommadAnalysis::analysisText()
{
	Cmds cmds = slicingCmd();
	for (auto iter = cmds.begin(); iter != cmds.end();)
	{
		if (iter->initCmdType(types))
		{
			iter++;
			continue;
		}
		iter = cmds.erase(iter);
	}


	return cmds;
}

/**
* @brief M3dCommadAnalysis::slicingCmd 将文本切割为一条一条的命令 
* @return Cmds
*/
Cmds M3dCommadAnalysis::slicingCmd()
{
	QString temp = this->text;

	//使用换行符切割
	QStringList list = temp.split("\n");

	Cmds cmds;

	/*
		遍历每一行。使用分号分割命令。
	*/
	M3dCommand tempCmd;
	for (int i = 0; i < list.size(); i++)
	{
		temp = list.at(i);
		//如果行内不含分号，则继续往下寻找
		if (temp.indexOf(";") == -1)
		{
			M3dLine line;
			line.str = temp;
			line.num = i;
			tempCmd.lines.push_back(line);
			continue;
		}
		
		//如果含有分号则切割字符
		auto listCmd = temp.split(";");
		auto iter = listCmd.begin();
		while (iter != listCmd.end())
		{
			M3dLine line;
			line.str = *iter;
			line.num = i;
			tempCmd.lines.push_back(line);
			iter++;
			if (iter != listCmd.end())
			{
				tempCmd.simplified();
				cmds.push_back(tempCmd);
				tempCmd.clear();
			}
		}
	}

	return cmds;
}

/**
* @brief M3dCommand::clear 清理对象
* @return void
*/
void M3dCommand::clear()
{
	cmd = "";
	lines.clear();
}

/**
* @brief M3dCommand::simplified 去多余空格 注释
* @return QString
*/
QString M3dCommand::simplified()
{
	QString str;
	for (auto iter = lines.begin(); iter != lines.end(); iter++)
	{
		str += iter->str;
	}
	str = str.simplified();

	//注释的正则表达式
	//这里使用静态主要因为创建rex对象十分消耗时间
	static std::vector<QRegExp> annotationRexs = { QRegExp("!.*"),QRegExp("(^|\\s)[zZ](\\s|$)") };

	//去掉命令中的注释
	for (auto iter = annotationRexs.begin(); iter != annotationRexs.end(); iter++)
	{
		int index = iter->indexIn(str);
		if(index == -1)
			continue;
		str.remove(index, str.length() - index);
	}

	this->text = str;
	return str;
}


/**
* @brief M3dCommand::initCmdType 初始化命令的类型 这里主要输入所有命令类型进行匹配。在调用此函数之前必须先simplified()
* @param std::list<M3dCommandType> types 所有的命令类型
* @return bool
*/
bool M3dCommand::initCmdType(std::list<M3dCommandType> types)
{
	for (auto iter = types.begin(); iter != types.end(); iter++)
	{
		if(iter->regx.indexIn(this->text) == -1)
			continue;
		cmd = iter->word;
		return true;
	}

	return false;
}


M3dCommandType::M3dCommandType(const QString& w) 
	:regx("(^|\\s)" + w + "(\\s|$|;)"), word(w)
{

}
