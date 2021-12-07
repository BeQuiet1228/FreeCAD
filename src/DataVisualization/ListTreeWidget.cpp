#include"ListTreeWidget.h"
#include <map>
#include <vector>
#include <sstream>
#include "C_encoding.h"
#include <QDebug>
namespace DV {
	ListTreeWidget::ListTreeWidget(QWidget* parent) :QWidget(parent)/*, structHeadCount(0)*/
	{
		//初始化TreeView的风格
		m_TreeView = new QTreeView(this);
		m_TreeView->resize(this->size());
		goodsModel = new QStandardItemModel(m_TreeView);
		goodsModel->setRowCount(0);
		goodsModel->setColumnCount(0);
		//goodsModel->setHorizontalHeaderLabels(QStringList() << (QString::fromLocal8Bit("分类")));
		goodsModel->setHorizontalHeaderLabels(QStringList() << GetEncodingstr("分类", ENCODING_GB2312));
		m_TreeView->setModel(goodsModel);
		m_TreeView->setEditTriggers(QAbstractItemView::NoEditTriggers);
		connect(m_TreeView, SIGNAL(doubleClicked(const QModelIndex&)), this, SLOT(on_doubleclick(const QModelIndex&)));
	}
	ListTreeWidget::~ListTreeWidget() {
	}
	/**
	* @brief ListTreeWidget::resizeEvent 窗口大小变化事件
	* @param QResizeEvent * event
	* @return void
	*/
	void ListTreeWidget::resizeEvent(QResizeEvent* event)
	{
		if (m_TreeView)
		{
			m_TreeView->resize(this->size());
		}
	}
	/**
	* @biref ListTreeWidget::on_doubleclick 双击事件
	* @param const QModelIndex &index
	* @return void
	*/
	void ListTreeWidget::on_doubleclick(const QModelIndex& index)
	{
	}
	/**
	* @brief  ListTreeWidget::clear 清除树控件
	* @return void
	*/
	void ListTreeWidget::clear()
	{
		if (goodsModel->hasChildren() > 0)
		{
			goodsModel->removeRows(0, goodsModel->rowCount());
		}
	}
};
#include "moc_ListTreeWidget.cpp"
