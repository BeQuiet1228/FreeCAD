#pragma once
#ifdef _DATA_VISUALIZATION_
#define DATA_VISUALIZATION_EXPORT __declspec(dllexport)
#else
#define DATA_VISUALIZATION_EXPORT   __declspec(dllimport)
#endif 

#ifndef DATA_VISUALIZATIONG_DLL
#define DATA_VISUALIZATION_EXPORT  
#endif