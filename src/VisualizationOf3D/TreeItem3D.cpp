#include "TreeItem3D.h"
#include "Widget3D.h"
TreeItem3D::TreeItem3D():TreeItem(){}
TreeItem3D::TreeItem3D(const QString& text): TreeItem(text){}
TreeItem3D::TreeItem3D(const QIcon& icon, const QString& text):TreeItem(icon,text){}
TreeItem3D::TreeItem3D(int rows, int columns):TreeItem(rows,columns) {}
TreeItem3D::~TreeItem3D() {
	if (nullptr != parentWidget)
	{
		Widget3D* temp = dynamic_cast<Widget3D*>(parentWidget);
		temp->clearItem(this);
	}
}
void TreeItem3D::initUI() {
	pID = 3;
	parentWidget = nullptr;
}
void TreeItem3D::setParent(QWidget* parent)
{
	parentWidget = parent;
}
