#include "ParticleAdapter.h"
#include "ParticleData.h"
#include "Renderer.h"
#include "C_encoding.h"
#include <QAction>

DV::PartcleAdapter::PartcleAdapter()
{

}

DV::PartcleAdapter::~PartcleAdapter()
{

}

std::list<QAction*> DV::PartcleAdapter::getActions()
{
	std::list<QAction*> acs;
	//如果需要结构图，那么需要返回结构图开关按钮
	if (mainRenderer->getData()->getNeedStructType() == Data::NEED_STRUCT)
	{
		auto tempActions = PlotAdapterNeedStruct::getActions();
		for (QAction* aciton: tempActions)
		{
			acs.push_back(aciton);
		}
	}

	for (QAction* action : actions)
	{
		acs.push_back(action);
	}

	return acs;
}

void DV::PartcleAdapter::actionTrigger(bool)
{
	QAction* aciton = dynamic_cast<QAction*>(sender());
	if (!aciton)
		return;
	int index = 0;
	for (; index < actions.size(); index++)
	{
		if(actions[index] == aciton)
			break;
	}
	if (index >= actions.size())
		return;

	auto data = std::dynamic_pointer_cast<ParticleData>(mainRenderer->getData());
	//记录下渲染范围
	auto xr = data->getXRang();
	auto yr = data->getYRang();

	bool setting = data->getDisplayParticle(index);
	data->setDisplayParticle(index, !setting);
	data->initDiretion();
	data->loadPointHard();

	//恢复之前的渲染范围
	data->setXRang(xr);
	data->setYRang(yr);

	updateAcitonState();
	emit updatePlot();
}

int DV::PartcleAdapter::getParticelTyepSize()
{
	if (!mainRenderer)
		return 0;
	auto data = std::dynamic_pointer_cast<ParticleData>(mainRenderer->getData());
	data->loadPoint();

	return data->typeSize;
}

void DV::PartcleAdapter::initAction()
{
	int typeSize = getParticelTyepSize();
	if (actions.size() == typeSize)
		return;
	for (QAction* action : actions)
	{
		disconnect(action, SIGNAL(triggered(bool)), this, SLOT(actionTrigger(bool)));
	}
	actions.clear();

	for (int i = 0; i < typeSize; i++)
	{
		QAction* action = new QAction(this);
		connect(action, SIGNAL(triggered(bool)), this, SLOT(actionTrigger(bool)));
		actions.push_back(action);
	}
	updateAcitonState();
}

void DV::PartcleAdapter::updateAcitonState()
{
	auto data = std::dynamic_pointer_cast<ParticleData>(mainRenderer->getData());
	data->loadPoint();

	for (int i = 0;i < actions.size();i++)
	{
		QAction* action = actions[i];
		if (data->getDisplayParticle(i))
		{
			action->setIcon(QIcon(":/ActionIcon/contour_image_on.svg"));
			action->setText(GetEncodingstr("粒子%1(开)", ENCODING_GB2312).arg(i));
		}else {
			action->setIcon(QIcon(":/ActionIcon/contour_image_off.svg"));
			action->setText(GetEncodingstr("粒子%1(关)", ENCODING_GB2312).arg(i));
		}
	}
}


#include "moc_ParticleAdapter.cpp"