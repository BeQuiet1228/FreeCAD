#pragma once

#pragma once
#ifdef _DATA_VISUALIZATION_3D
#define DATA_VISUALIZATION_3D_EXPORT __declspec(dllexport)
#else
#define DATA_VISUALIZATION_3D_EXPORT   __declspec(dllimport)
#endif 