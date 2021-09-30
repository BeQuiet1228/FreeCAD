#pragma once
#ifdef _VISUALZATION3D_
#define VISUALZATION3D_EXPORT __declspec(dllexport)
#else
#define VISUALZATION3D_EXPORT __declspec(dllimport)
#endif

#ifndef _VISUALZATION3D_DLL
#define VISUALZATION3D_EXPORT
#endif // !VISUALZATION_DLL
