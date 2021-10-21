#include "TreeItem3D.h"
#include "Widget3D.h"
TreeItem3D::TreeItem3D():TreeItem(){
		pID = 3;
		parentWidget = nullptr;
}
TreeItem3D::TreeItem3D(const QString& text): TreeItem(text){
	pID = 3;
	parentWidget = nullptr;
}
TreeItem3D::TreeItem3D(const QIcon& icon, const QString& text):TreeItem(icon,text){
	pID = 3;
	parentWidget = nullptr;
}
TreeItem3D::TreeItem3D(int rows, int columns):TreeItem(rows,columns) {
	pID = 3;
	parentWidget = nullptr;
}
TreeItem3D::~TreeItem3D() {
	if (nullptr != parentWidget)
	{
		Widget3D* temp = dynamic_cast<Widget3D*>(parentWidget);
		if(nullptr!=temp)
			temp->clearItem(this);
	}
}
/**
* @brief TreeItem3D::setParent …Ë÷√∏∏Ω⁄µ„
* @param QWidget * parent
* @return void
*/
void TreeItem3D::setParent(QWidget* parent)
{
	parentWidget = parent;
}
