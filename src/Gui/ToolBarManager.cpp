/***************************************************************************
 *   Copyright (c) 2005 Werner Mayer <wmayer[at]users.sourceforge.net>     *
 *                                                                         *
 *   This file is part of the FreeCAD CAx development system.              *
 *                                                                         *
 *   This library is free software; you can redistribute it and/or         *
 *   modify it under the terms of the GNU Library General Public           *
 *   License as published by the Free Software Foundation; either          *
 *   version 2 of the License, or (at your option) any later version.      *
 *                                                                         *
 *   This library  is distributed in the hope that it will be useful,      *
 *   but WITHOUT ANY WARRANTY; without even the implied warranty of        *
 *   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         *
 *   GNU Library General Public License for more details.                  *
 *                                                                         *
 *   You should have received a copy of the GNU Library General Public     *
 *   License along with this library; see the file COPYING.LIB. If not,    *
 *   write to the Free Software Foundation, Inc., 59 Temple Place,         *
 *   Suite 330, Boston, MA  02111-1307, USA                                *
 *                                                                         *
 ***************************************************************************/


#include "PreCompiled.h"
#ifndef _PreComp_
# include <QApplication>
# include <QAction>
# include <QToolBar>
# include <QToolButton>
#endif

#include "ToolBarManager.h"
#include "MainWindow.h"
#include "Application.h"
#include "Command.h"
#include "Widgets.h"
#include <qaction.h>

#include "qwidgetaction.h"
#include "MainWindowDef.h"
#include "TabWidgetInterface.hpp"
#include <QToolButton>
#include "Command.h"
#include "Action.h"

using namespace Gui;

ToolBarItem::ToolBarItem()
{
	
}

ToolBarItem::ToolBarItem(ToolBarItem* item)
{
    if ( item )
        item->appendItem(this);
}

ToolBarItem::~ToolBarItem()
{
    clear();
}

void ToolBarItem::setCommand(const std::string& name)
{
    _name = name;
}

std::string ToolBarItem::command() const
{
    return _name;
}

bool ToolBarItem::hasItems() const
{
    return _items.count() > 0;
}

ToolBarItem* ToolBarItem::findItem(const std::string& name)
{
    if ( _name == name ) {
        return this;
    } else {
        for ( QList<ToolBarItem*>::ConstIterator it = _items.begin(); it != _items.end(); ++it ) {
            if ( (*it)->_name == name ) {
                return *it;
            }
        }
    }

    return 0;
}

ToolBarItem* ToolBarItem::copy() const
{
    ToolBarItem* root = new ToolBarItem;
    root->setCommand( command() );

    QList<ToolBarItem*> items = getItems();
    for ( QList<ToolBarItem*>::ConstIterator it = items.begin(); it != items.end(); ++it ) {
        root->appendItem( (*it)->copy() );
    }

    return root;
}

uint ToolBarItem::count() const
{
    return _items.count();
}

void ToolBarItem::appendItem(ToolBarItem* item)
{
    _items.push_back( item );
}

bool ToolBarItem::insertItem( ToolBarItem* before, ToolBarItem* item)
{
    int pos = _items.indexOf(before);
    if (pos != -1) {
        _items.insert(pos, item);
        return true;
    } else
        return false;
}

void ToolBarItem::removeItem(ToolBarItem* item)
{
    int pos = _items.indexOf(item);
    if (pos != -1)
        _items.removeAt(pos);
}

void ToolBarItem::clear()
{
    for ( QList<ToolBarItem*>::Iterator it = _items.begin(); it != _items.end(); ++it ) {
        delete *it;
    }

    _items.clear();
}

ToolBarItem& ToolBarItem::operator << (ToolBarItem* item)
{
    appendItem(item);
    return *this;
}

ToolBarItem& ToolBarItem::operator << (const std::string& command)
{
    ToolBarItem* item = new ToolBarItem(this);
    item->setCommand(command);
    return *this;
}

QList<ToolBarItem*> ToolBarItem::getItems() const
{
    return _items;
}

// -----------------------------------------------------------

ToolBarManager* ToolBarManager::_instance=0;

ToolBarManager* ToolBarManager::getInstance()
{
    if ( !_instance )
        _instance = new ToolBarManager;
    return _instance;
}

void ToolBarManager::destruct()
{
    delete _instance;
    _instance = 0;
}

ToolBarManager::ToolBarManager()
{
}

ToolBarManager::~ToolBarManager()
{
}

void ToolBarManager::setup(ToolBarItem* toolBarItems)
{
	if (!toolBarItems)
		return; // empty menu bar
	
#ifdef _PICGUI_
	/*
	测试 toobaritems
	*/
	auto its = toolBarItems->getItems();
	for (auto i = its.begin(); i != its.end(); i++)
	{
		std::cerr << "---------" << (*i)->command() << "--------" << std::endl;
		auto iits = (*i)->getItems();
		for (auto ii = iits.begin(); ii != iits.end(); ii++)
		{
			std::cerr << "++++++++" << (*ii)->command() << "++++++++" << std::endl;
		}
	}
	CommandManager& cmdManager = Application::Instance->commandManager();
	auto mainwindow = MainWindow::getInstance();
	auto tabWidget = mainwindow->mainWindowDef->tabWidgetInterface;
	tabWidget->clearAllAction();
	auto groupItems = toolBarItems->getItems();
	for(auto group = groupItems.begin();group!= groupItems.end();group++)
	{
		auto cmds = (*group)->getItems();
		for(auto cmdItem = cmds.begin();cmdItem != cmds.end();cmdItem++)
		{
			auto cmd = cmdManager.getCommandByName((*cmdItem)->command().c_str());
			if (!cmd)
				continue;
			auto action = cmdManager.creatAction(cmd);
			auto qAction = action->getQAction();
			QString tabName = QString::fromLocal8Bit("其他");
			if ((*group)->command() == "File")
			{
				tabName = QString::fromLocal8Bit("开始");
				mainwindow->mainWindowDef->addTitleShortcutAction(qAction);
			}
			else if ((*group)->command() == "_2d"
				|| ((*group)->command() == "_3dCommon")
				|| ((*group)->command() == "_3dSpecil") || ((*group)->command() == "_3dComplex")){
				tabName = QString::fromLocal8Bit("建模");
			}
			else if ((*group)->command() == "comboundary" || (*group)->command() == "emit"
					|| (*group)->command() == "observe"){
				tabName = QString::fromLocal8Bit("物理设置");
			}
			if (tabWidget->hasAction(qAction))
				continue;
			tabWidget->addAction(
				tabName, QString::fromLocal8Bit((*group)->command().c_str()), qAction);	
		}
	}
#else
	saveState();
	this->toolbarNames.clear();

	int max_width = getMainWindow()->width();
	// int top_width = 0;

	ParameterGrp::handle hPref = App::GetApplication().GetUserParameter().GetGroup("BaseApp")
		->GetGroup("MainWindow")->GetGroup("Toolbars");
	QList<ToolBarItem*> items = toolBarItems->getItems();
	QList<QToolBar*> toolbars = toolBars();
	for (QList<ToolBarItem*>::ConstIterator it = items.begin(); it != items.end(); ++it) {
		// search for the toolbar
		QString name = QString::fromUtf8((*it)->command().c_str());
		std::cerr << name.toStdString() << std::endl;
		this->toolbarNames << name;
		QToolBar* toolbar = findToolBar(toolbars, name);
		std::string toolbarName = (*it)->command();
		bool visible = hPref->GetBool(toolbarName.c_str(), true);
		bool toolbar_added = false;

		if (!toolbar) {
			if (strcmp(toolbarName.c_str(), "Workbench") == 0){
				toolbar = new WorkbenchToolBar(getMainWindow());//Workbench工具条使用自定义类，方便在QSS中设置样式
				toolbar->setWindowTitle(QApplication::translate("Workbench", toolbarName.c_str()));
				getMainWindow()->addToolBar(toolbar);
			}
			else
				toolbar = getMainWindow()->addToolBar(QApplication::translate("Workbench", toolbarName.c_str())); // i18n
			toolbar->setObjectName(name);
			toolbar->setVisible(visible);
			toolbar_added = true;
		}
		else {
			toolbar->setVisible(visible);
			toolbar->toggleViewAction()->setVisible(true);
			int index = toolbars.indexOf(toolbar);
			toolbars.removeAt(index);
		}

		// setup the toolbar

		setup(*it, toolbar);
		// 工具条不再根据控件宽度自动自动换行
		if (toolbar_added && toolbar->objectName() == QString::fromUtf8("View")) {
			// if (top_width > 0 && getMainWindow()->toolBarBreak(toolbar))
			//     top_width = 0;
			// // the width() of a toolbar doesn't return useful results so we estimate
			// // its size by the number of buttons and the icon size
			// QList<QToolButton*> btns = toolbar->findChildren<QToolButton*>();
			// top_width += (btns.size() * toolbar->iconSize().width());
			// if (top_width > max_width) {
			//     top_width = 0;
			getMainWindow()->insertToolBarBreak(toolbar);
		}
	}

	// hide all unneeded toolbars
	for (QList<QToolBar*>::Iterator it = toolbars.begin(); it != toolbars.end(); ++it) {
		// make sure that the main window has the focus when hiding the toolbar with
		// the combo box inside
		QWidget *fw = QApplication::focusWidget();
		while (fw &&  !fw->isWindow()) {
			if (fw == *it) {
				getMainWindow()->setFocus();
				break;
			}
			fw = fw->parentWidget();
		}
		// ignore toolbars which do not belong to the previously active workbench
		QByteArray toolbarName = (*it)->objectName().toUtf8();
		if (!(*it)->toggleViewAction()->isVisible())
			continue;
		hPref->SetBool(toolbarName.constData(), (*it)->isVisible());
		(*it)->hide();
		(*it)->toggleViewAction()->setVisible(false);
	}
#endif // _PICGUI_
    
}

void ToolBarManager::setup(ToolBarItem* item, QToolBar* toolbar) const
{
    // 根据工具条的objectName设置工具条的显示方式：单行、分组显示
    if (toolbar->objectName() == QString::fromUtf8("File")
        /*|| toolbar->objectName() == QString::fromUtf8("Workbench")*/){
        setup_one_line(item, toolbar);
		auto actions = toolbar->actions();
		auto mw = MainWindow::getInstance();
		for (auto i = actions.begin(); i != actions.end(); i++)
		{
			mw->addTitleAction(*i);
		}
    }
    else if (toolbar->objectName() == QString::fromUtf8("Task Monitor")){
        setup_taskMonitorToolBar(item, toolbar);
	}
	else if (toolbar->objectName() == QString::fromUtf8("ControlPanel"))
	{
		auto sp = QSizePolicy(QSizePolicy::Fixed, QSizePolicy::Fixed);
		/*
		auto mainWindow = MainWindow::getInstance();
		mainWindow->buttonBar->setSizePolicy(sp);
		toolbar->setFixedSize(mainWindow->buttonBar->size());
		mainWindow->buttonBar->setParent(toolbar);
		toolbar->addWidget(mainWindow->buttonBar);
		*/
	}
    else{
        setup_multiple_groups(item, toolbar);
    }
}

// 设置单行工具条
void ToolBarManager::setup_one_line(ToolBarItem* item, QToolBar* toolbar) const
{
    CommandManager& mgr = Application::Instance->commandManager();
    QList<ToolBarItem*> items = item->getItems();
    // 如果工具条在不同工作台显示不同的action，则只更新这些不同的地方
    QList<ToolBarItem*>::ConstIterator it = items.begin();
    QList<QAction*> actions = toolbar->actions();
    QList<QAction*>::ConstIterator ait = actions.begin();
    bool same = true;
    while (it != items.end() && same){
        if (ait != actions.end() && (*it)->command().c_str() == (*ait)->data().toByteArray()){
            ++it;
            ++ait;
        }
        else
            same = false;
    }
    if (ait != actions.end())
        same = false;
    if (same)
        return;
    else{
        while (ait != actions.end()){
            toolbar->removeAction(*ait);
            ++ait;
        }
    }

    for (; it != items.end(); ++it) {
        // search for the action item
        //QAction* action = findAction(actions, QString::fromUtf8((*it)->command().c_str()));
        //if (!action) {
            QAction *action = 0;
            if ((*it)->command() == "Separator") {
                action = toolbar->addSeparator();
            } else {
                // Check if action was added successfully
                if (mgr.addTo((*it)->command().c_str(), toolbar))
                    action = toolbar->actions().last();
            }

            // set the tool button user data
            if (action) action->setData(QString::fromUtf8((*it)->command().c_str()));
        //} else {
        //    // Note: For toolbars we do not remove and readd the actions
        //    // because this causes flicker effects. So, it could happen that the order of 
        //    // buttons doesn't match with the order of commands in the workbench.
        //    int index = actions.indexOf(action);
        //    actions.removeAt(index);
        //}
    }

    //// remove all tool buttons which we don't need for the moment
    //for (QList<QAction*>::Iterator it = actions.begin(); it != actions.end(); ++it) {
    //    toolbar->removeAction(*it);
    //}
}

// 设置分组工具条
void ToolBarManager::setup_multiple_groups(ToolBarItem* item, QToolBar* toolbar) const
{

    CommandManager& mgr = Application::Instance->commandManager();
    QList<ToolBarItem*> items = item->getItems();
    auto widgetActions = toolbar->actions();

    //Workbench工具条只设置一次
    if (toolbar->objectName() == QString::fromUtf8("Workbench"))
        if (widgetActions.count() > 0)
            return;

    //其它工具条：删除原工具条中所有内容，完全重建
    for (auto w : widgetActions){
        if (QWidgetAction *wa = qobject_cast<QWidgetAction*>(w)){
            QLayout* layout = wa->defaultWidget()->layout();
            if (layout){
                while (auto item = layout->takeAt(0)){
                    if (item->widget())
                        item->widget()->setParent(0);
                }
            }
        }
        toolbar->removeAction(w);
        w->setParent(0);
    }


    QList<QWidget*> widgets;
    QMap<QByteArray, std::vector<int>> config;
    config.insert("Default4", { 4, 4, 4 });
    config.insert("Default6", { 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6 });
    config.insert("View", { 1, 6, 2 });
    config.insert("Navigation", { 10 });
    config.insert("3D Modeling", { 7, 6, 8, 8 });
    config.insert("Physics", { 8, 8, 8 });
    config.insert("Timer", { 2 });
    config.insert("Workbench", { 12 });
    config.insert("DynamicDate", { 4 });
	config.insert("NewSettinbgs", { 4 });
    QByteArray toolbarName;
    if (config.keys().indexOf(toolbar->objectName().toUtf8()) != -1){
        toolbarName = toolbar->objectName().toUtf8();
    }
    else{
        if (items.count() <= 6)
            toolbarName = "Default6";//item数小于6，全部放入一个组
        else if (items.count() <= 12)
            toolbarName = "Default4";//item数小于12，每4个分一个组
        else
            toolbarName = "Default6";
    }
    const std::vector<int> &vector = config.value(toolbarName);
    int vector_size = vector.size();

    QList<QGridLayout*> gridLayouts;

    for (int i = 0; i < vector_size; ++i){
        widgets.append(new QWidget(toolbar));
        gridLayouts.append(new QGridLayout(widgets.at(i)));
        gridLayouts.at(i)->setContentsMargins(11, 0, 11, 0);
        gridLayouts.at(i)->setHorizontalSpacing(0);//去掉按钮之间的间距
        gridLayouts.at(i)->setVerticalSpacing(0);
        widgets.at(i)->setLayout(gridLayouts.at(i));
        //toolbar->addWidget(widgets.at(i));
    }

    int row = 0, col = 0;
    int count_item_added = 0;
    int count_layout = 0;
    int count_expected_item = vector.at(count_layout);//当前组和之前组应该有的item总数

    //给Workbench工具条创建一个actionList
    QList<QAction*> *actionList = 0;
    if (toolbar->objectName() == QString::fromUtf8("Workbench"))
        actionList = new QList<QAction*>();

    if (toolbar->objectName() == QString::fromUtf8("DynamicDate")){
        QToolButton* toolButton = 0;
        toolButton = mgr.addToGridLayout(items[0]->command().c_str(), gridLayouts.at(count_layout), row, col, 2, 2);
        toolbar->addWidget(widgets[0]);
        // set the tool button user data
        if (toolButton) toolButton->defaultAction()->setData(QString::fromUtf8(items[0]->command().c_str()));
    }
    else{
        for (QList<ToolBarItem*>::ConstIterator it = items.begin(); it != items.end(); ++it) {
            int maxCol;
            if (vector.at(count_layout) % 2 == 0)
                maxCol = vector.at(count_layout) / 2;//maxCol由上面的vector计算得出，默认是除以2，即两行
            else
                maxCol = (vector.at(count_layout) + 1) / 2;

            QToolButton* toolButton = 0;
            //无视separator设置，每组之间自动插入separator
            if ((*it)->command() == "Separator")
                continue;

            toolButton = mgr.addToGridLayout((*it)->command().c_str(), gridLayouts.at(count_layout), row, col);
            if (toolButton){
                ++count_item_added;
                if (count_item_added < count_expected_item && it != items.end() - 1){
                    if (col < maxCol - 1){
                        ++col;
                    }
                    else{
                        ++row;
                        col = 0;
                    }
                }
                else{
                    if (count_layout != 0)
                        toolbar->addSeparator();//自动添加separator
                    toolbar->addWidget(widgets.at(count_layout));
                    if (count_layout < vector.size() - 1){
                        ++count_layout;
                        count_expected_item += vector.at(count_layout);
                        row = 0;
                        col = 0;
                    }
                }
            }

            // set the tool button user data
            if (toolButton) toolButton->defaultAction()->setData(QString::fromUtf8((*it)->command().c_str()));
            if (actionList)
                actionList->append(toolButton->defaultAction());
        }
    }
    //////////////////////
    //Workbench工具条
    if (toolbar->objectName() == QString::fromUtf8("Workbench")){
        gridLayouts.at(0)->setContentsMargins(0, 0, 0, 0);
        gridLayouts.at(0)->setSpacing(0);

        if (actionList && !getMainWindow()->findChild<QActionGroup*>(QString::fromUtf8("SwitchWorkbenchActionGroup"))){
            QActionGroup *actionGroup = new QActionGroup(Gui::getMainWindow());
            actionGroup->setObjectName(QString::fromUtf8("SwitchWorkbenchActionGroup"));
            actionGroup->setExclusive(true);
            for (auto a : *actionList){
                a->setCheckable(true);
                a->setActionGroup(actionGroup);
            }
        }
    }
    //////////////////////
    //无需remove
}

void ToolBarManager::setup_taskMonitorToolBar(ToolBarItem* item, QToolBar* toolbar) const
{
    // Task Monitor工具条的setup函数，有ToolButton和其它控件的混排
    //避免多次setup
    if (toolbar->findChild<QWidget*>(QString::fromUtf8("ReceiveFileWidget")))
        return;

    auto sp = QSizePolicy(QSizePolicy::Fixed, QSizePolicy::Fixed);
    
	/*
	auto mainWindow = MainWindow::getInstance();
	mainWindow->dateBar->setSizePolicy(sp);
	toolbar->setFixedSize(mainWindow->dateBar->size());
	mainWindow->dateBar->setParent(toolbar);
	toolbar->addWidget(mainWindow->dateBar);
	*/


}

void ToolBarManager::saveState() const
{
    ParameterGrp::handle hPref = App::GetApplication().GetUserParameter().GetGroup("BaseApp")
                               ->GetGroup("MainWindow")->GetGroup("Toolbars");

    QList<QToolBar*> toolbars = toolBars();
    for (QStringList::ConstIterator it = this->toolbarNames.begin(); it != this->toolbarNames.end(); ++it) {
        QToolBar* toolbar = findToolBar(toolbars, *it);
        if (toolbar) {
            QByteArray toolbarName = toolbar->objectName().toUtf8();
            hPref->SetBool(toolbarName.constData(), toolbar->isVisible());
        }
    }
}

void ToolBarManager::restoreState() const
{
    ParameterGrp::handle hPref = App::GetApplication().GetUserParameter().GetGroup("BaseApp")
                               ->GetGroup("MainWindow")->GetGroup("Toolbars");

    QList<QToolBar*> toolbars = toolBars();
    for (QStringList::ConstIterator it = this->toolbarNames.begin(); it != this->toolbarNames.end(); ++it) {
        QToolBar* toolbar = findToolBar(toolbars, *it);
        if (toolbar) {
            QByteArray toolbarName = toolbar->objectName().toUtf8();
            toolbar->setVisible(hPref->GetBool(toolbarName.constData(), toolbar->isVisible()));
        }
    }
}

void ToolBarManager::retranslate() const
{
    QList<QToolBar*> toolbars = toolBars();
    for (QList<QToolBar*>::Iterator it = toolbars.begin(); it != toolbars.end(); ++it) {
        QByteArray toolbarName = (*it)->objectName().toUtf8();
        (*it)->setWindowTitle(
            QApplication::translate("Workbench",
                                    (const char*)toolbarName));
    }
}

QToolBar* ToolBarManager::findToolBar(const QList<QToolBar*>& toolbars, const QString& item) const
{
    for (QList<QToolBar*>::ConstIterator it = toolbars.begin(); it != toolbars.end(); ++it) {
        if ((*it)->objectName() == item)
            return *it;
    }

    return 0; // no item with the user data found
}

QAction* ToolBarManager::findAction(const QList<QAction*>& acts, const QString& item) const
{
    for (QList<QAction*>::ConstIterator it = acts.begin(); it != acts.end(); ++it) {
        if ((*it)->data().toString() == item)
            return *it;
    }

    return 0; // no item with the user data found
}

QList<QToolBar*> ToolBarManager::toolBars() const
{
    QWidget* mw = getMainWindow();
    QList<QToolBar*> tb;
    QList<QToolBar*> bars = getMainWindow()->findChildren<QToolBar*>();
    for (QList<QToolBar*>::ConstIterator it = bars.begin(); it != bars.end(); ++it) {
        if ((*it)->parentWidget() == mw)
            tb.push_back(*it);
    }

    return tb;
}
