#include <qwidget.h>
#include <QApplication>
#include "Plot.h"
#include <HDF5Reader/hdf5io.h>
#include <memory>
#include "TimeData.h"
#include "structureData.h"
#include "TimeRenderer.h"
#include "StructRenderer.h"
#include <Canvas.h>
#include "RenderTask.h"
#include "RenderThreadManager.h"
#include"Axis.h"
int main(int argc, char *argv[])
{
        QApplication a(argc, argv);
        CanvasItem::registerMetaTye();
		/*QString sPath = QString("./plugin/");
		a.addLibraryPath(sPath);*/

        std::string path = "D:/wandaotongProject/MILO_C_2.h5";
        Hdf5IO io(path);

        io.initHdf5Data();
        auto data = io.hdf5DataList.begin();

       // data +=22;
        Hdf5Data d = *data;
		std::shared_ptr<structureData> _structData(new structureData(d));
        //std::shared_ptr<TimeData> timeData(new TimeData(d));
		StructureRenderer* structureRenderer = new StructureRenderer(_structData);
        //TimeRenderer *timeRenderer = new TimeRenderer(timeData);
        //timeRenderer->dataInit();
        //timeRenderer->setDefaultRang();
		structureRenderer->dataInit();
		structureRenderer->setDefaultRang();
        Plot p;
		std::shared_ptr<Renderer> rd(structureRenderer);
        p.setMainRenderer(rd);
        p.show();

		std::shared_ptr<Renderer> re(structureRenderer);
        RenderTask task(re);

        RenderThreadManager ma;
        ma.addTask(task);
        task.rank = 3;
        ma.addTask(task);
        task.rank = 2;
        ma.addTask(task);
        ma.start();
        return a.exec();
}
