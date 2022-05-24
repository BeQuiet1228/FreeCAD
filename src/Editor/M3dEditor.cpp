#include "M3dEditor.h"
#include "M3dHightLighter.h"
#include <regex>
#include <vector>
#include <QTextIStream>
#include <QTextCursor>
#include <iostream>
#include <QTextDocumentFragment>
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

void M3dEditor::keyPressEvent(QKeyEvent* event)
{
	QTextCursor cursor = this->textCursor();

	//选中时添加或者取消注释
	if (cursor.hasSelection() && event->key() == Qt::Key_Slash)
	{
		selectionAnnotation();
	}
	else
	{
		CodeEditor::keyPressEvent(event);
	}
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

void M3dEditor::gotoLine(const int& num)
{
	auto cursor = this->textCursor();
	int pos = this->document()->findBlockByNumber(num).position();
	cursor.setPosition(pos);
	this->setTextCursor(cursor);
	this->centerCursor();
}

void M3dEditor::selectionAnnotation()
{
	QTextCursor cursor = this->textCursor();
	QString text = cursor.selection().toPlainText();
	QStringList list = text.split("\n");
	bool ok = true;
	//判断是否已经为注释块
	for (auto iter = list.begin(); iter != list.end(); iter++)
	{
		if (iter->size() == 0)
			continue;
		if (iter->at(0) != '!')
		{
			ok = false;
			break;
		}
	}
	//如果已经为注释块，那么取消注释
	//否则增加注释
	QString newText;
	if (ok)
	{
		for (auto iter = list.begin(); iter != list.end(); iter++)
		{
			//如果不是最后一行，则添加换行符
			QString r = '\n';
			if (iter + 1 == list.end())
				r = "";
			if (iter->size() == 0)
			{
				newText += r;
				continue;
			}
			//不取左边的感叹号
			auto temp = iter->right(iter->size() - 1);
			newText += temp + r;
		}
	}
	else {
		for (auto iter = list.begin(); iter != list.end(); iter++)
		{
			//如果不是最后一行，则添加换行符
			QString r = '\n';
			if (iter + 1 == list.end())
				r = "";
			if (iter->size() == 0)
			{
				newText += r;
				continue;
			}
			//在开端位置增加感叹号
			newText += "!" + *iter + r;
		}
	}
	//插入新的文本
	cursor.insertText(newText);
	setTextCursor(cursor);
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
			//行号从1开始
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

M3dCommand::M3dCommand()
{
	cmdType = nullptr;
}

M3dCommand::~M3dCommand()
{
	if(cmdType != nullptr)
		delete cmdType;
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
		//去掉！开头的注释
		static QRegExp regx("!.*");
		int pos = regx.indexIn(iter->str);
		if (pos != -1)
			str += iter->str.remove(pos, iter->str.length() - pos);
		else
			str += iter->str;
	}
	str = str.simplified();

	//去掉z开头的注释
	//这里使用静态主要因为创建rex对象十分消耗时间
	static QRegExp rex("(^|\\s)[zZ](\\s|$)");

	int index = rex.indexIn(str);
	if (index != -1)
		str.remove(index, str.length() - index);

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
		setCommadType(*iter);
		return true;
	}

	return false;
}


/**
* @brief M3dCommand::getStartLine 获取命令的起始行
* @return int
*/
int M3dCommand::getStartLine()
{
	if (cmdType == nullptr)
		return 0;

	for (auto iter = lines.begin(); iter != lines.end(); iter++)
	{
		if (cmdType->regx.indexIn(iter->str) != -1)
			return iter->num;
	}

	return 0;
}

void M3dCommand::setCommadType(const M3dCommandType& type)
{
	if (cmdType != nullptr)
		delete cmdType;
	cmdType = new M3dCommandType(type);
	cmd = cmdType->word;
}

M3dCommandType::M3dCommandType(const QString& w) 
	:regx("(^|\\s)" + w + "(\\s|$|;)"), word(w)
{

}
