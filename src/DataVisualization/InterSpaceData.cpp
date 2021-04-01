#include "InterSpaceData.h"

InterspaceData::InterspaceData(Hdf5Data& h5Data, const RunMod& mod /*= SINGLE_THREAD*/)
	:TimeData(h5Data,mod)
{

}

