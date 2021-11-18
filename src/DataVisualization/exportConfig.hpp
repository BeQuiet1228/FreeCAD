#pragma once
#ifdef _DATA_VISUALIZATION_
#define DATA_VISUALIZATION_EXPORT __declspec(dllexport)
#else
#define DATA_VISUALIZATION_EXPORT   __declspec(dllimport)
#endif 

#ifndef DATA_VISUALIZATIONG_DLL
#define DATA_VISUALIZATION_EXPORT  
#endif

#ifdef  __cplusplus
#define EXTERN_C extern "C"
#else
#define EXTERN_C
#endif