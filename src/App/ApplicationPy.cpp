/***************************************************************************
 *   (c) Juergen Riegel (juergen.riegel@web.de) 2002                       *
 *                                                                         *
 *   This file is part of the FreeCAD CAx development system.              *
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU Library General Public License (LGPL)   *
 *   as published by the Free Software Foundation; either version 2 of     *
 *   the License, or (at your option) any later version.                   *
 *   for detail see the LICENCE text file.                                 *
 *                                                                         *
 *   FreeCAD is distributed in the hope that it will be useful,            *
 *   but WITHOUT ANY WARRANTY; without even the implied warranty of        *
 *   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         *
 *   GNU Library General Public License for more details.                  *
 *                                                                         *
 *   You should have received a copy of the GNU Library General Public     *
 *   License along with FreeCAD; if not, write to the Free Software        *
 *   Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  *
 *   USA                                                                   *
 *                                                                         *
 *   Juergen Riegel 2002                                                   *
 ***************************************************************************/




#include "PreCompiled.h"

#ifndef _PreComp_
# include <stdexcept>
#endif


#include "Application.h"
#include "Document.h"
#include "DocumentPy.h"
#include "DocumentObserverPython.h"
#include <H5Cpp.h>
#include <H5Fpublic.h>
#include "hdf5io.h"
#include <windows.h>

#include<Gui/Command.h>

// FreeCAD Base header
#include <Base/Interpreter.h>
#include <Base/Exception.h>
#include <Base/Parameter.h>
#include <Base/Console.h>
#include <Base/Factory.h>
#include <Base/FileInfo.h>
#include <Base/UnitsApi.h>
#include<Base/Tools.h>
#include <ctime>
#include "Config.hpp"
#include "NetMsg.hpp"

#include"UserJson.hpp"

#include "Contorl/ContorlInterface.h"
//using Base::GetConsole;
using namespace Base;
using namespace App;





//**************************************************************************
// Python stuff

// Application Methods						// Methods structure
PyMethodDef Application::Methods[] = {
    {"ParamGet",       (PyCFunction) Application::sGetParam,       1,
     "Get parameters by path"},
    {"saveParameter",  (PyCFunction) Application::sSaveParameter,  1,
     "saveParameter(config='User parameter') -> None\n"
     "Save parameter set to file. The default set is 'User parameter'"},
    {"Version",        (PyCFunction) Application::sGetVersion,     1,
     "Print the version to the output."},
    {"ConfigGet",      (PyCFunction) Application::sGetConfig,      1,
     "ConfigGet(string) -- Get the value for the given key."},
    {"ConfigSet",      (PyCFunction) Application::sSetConfig,      1,
     "ConfigSet(string, string) -- Set the given key to the given value."},
    {"ConfigDump",     (PyCFunction) Application::sDumpConfig,     1,
     "Dump the configuration to the output."},
    {"addImportType",  (PyCFunction) Application::sAddImportType,  1,
     "Register filetype for import"},
    {"getImportType",  (PyCFunction) Application::sGetImportType,  1,
     "Get the name of the module that can import the filetype"},
    {"EndingAdd",      (PyCFunction) Application::sAddImportType  ,1, // deprecated
     "deprecated -- use addImportType"},
    {"EndingGet",      (PyCFunction) Application::sGetImportType  ,1, // deprecated
     "deprecated -- use getImportType"},
    {"addExportType",  (PyCFunction) Application::sAddExportType  ,1,
     "Register filetype for export"},
    {"getExportType",  (PyCFunction) Application::sGetExportType  ,1,
     "Get the name of the module that can export the filetype"},
    {"getResourceDir", (PyCFunction) Application::sGetResourceDir  ,1,
     "Get the root directory of all resources"},
    {"getUserAppDataDir", (PyCFunction) Application::sGetUserAppDataDir  ,1,
     "Get the root directory of user settings"},
    {"getUserMacroDir", (PyCFunction) Application::sGetUserMacroDir  ,1,
     "Get the directory of the user's macro directory"},
    {"getHelpDir", (PyCFunction) Application::sGetHelpDir  ,1,
     "Get the directory of the documentation"},
    {"getHomePath",    (PyCFunction) Application::sGetHomePath  ,1,
     "Get the home path, i.e. the parent directory of the executable"},

    {"loadFile",       (PyCFunction) Application::sLoadFile,   1,
     "loadFile(string=filename,[string=module]) -> None\n\n"
     "Loads an arbitrary file by delegating to the given Python module:\n"
     "* If no module is given it will be determined by the file extension.\n"
     "* If more than one module can load a file the first one one will be taken.\n"
     "* If no module exists to load the file an exception will be raised."},
    {"open",   (PyCFunction) Application::sOpenDocument,   1,
     "See openDocument(string)"},
    {"openDocument",   (PyCFunction) Application::sOpenDocument,   1,
     "openDocument(string) -> object\n\n"
     "Create a document and load the project file into the document.\n"
     "The string argument must point to an existing file. If the file doesn't exist\n"
     "or the file cannot be loaded an I/O exception is thrown. In this case the\n"
     "document is kept alive."},
//  {"saveDocument",   (PyCFunction) Application::sSaveDocument,   1,
//   "saveDocument(string) -- Save the document to a file."},
//  {"saveDocumentAs", (PyCFunction) Application::sSaveDocumentAs, 1},
    {"newDocument",    (PyCFunction) Application::sNewDocument,    1,
     "newDocument([string]) -> object\n\n"
     "Create a new document with a given name.\n"
     "The document name must be unique which\n"
     "is checked automatically."},
    {"closeDocument",  (PyCFunction) Application::sCloseDocument,  1,
     "closeDocument(string) -> None\n\n"
     "Close the document with a given name."},
    {"activeDocument", (PyCFunction) Application::sActiveDocument, 1,
     "activeDocument() -> object or None\n\n"
     "Return the active document or None if there is no one."},
    {"setActiveDocument",(PyCFunction) Application::sSetActiveDocument, 1,
     "setActiveDocement(string) -> None\n\n"
     "Set the active document by its name."},
    {"getDocument",    (PyCFunction) Application::sGetDocument,    1,
     "getDocument(string) -> object\n\n"
     "Get a document by its name or raise an exception\n"
     "if there is no document with the given name."},
    {"listDocuments",  (PyCFunction) Application::sListDocuments  ,1,
     "listDocuments() -> list\n\n"
     "Return a list of names of all documents."},
    {"addDocumentObserver",  (PyCFunction) Application::sAddDocObserver  ,1,
     "addDocumentObserver() -> None\n\n"
     "Add an observer to get notified about changes on documents."},
    {"removeDocumentObserver",  (PyCFunction) Application::sRemoveDocObserver  ,1,
     "removeDocumentObserver() -> None\n\n"
     "Remove an added document observer."},
	 { "removeAllDocumentObserver", (PyCFunction)Application::sRemoveAllDocObserver, 1,
	 "removeAllDocumentObserver() -> None\n\n"
	 "Remove all document observer." },
    {"setLogLevel",          (PyCFunction) Application::sSetLogLevel, 1,
     "setLogLevel(tag, level) -- Set the log level for a string tag.\n"
     "'level' can either be string 'Log', 'Msg', 'Wrn', 'Error', or an integer value"},
    {"getLogLevel",          (PyCFunction) Application::sGetLogLevel, 1,
     "getLogLevel(tag) -- Get the log level of a string tag"},
	 //自定义的socket通信
	 { "clientConnect", (PyCFunction)Application::sClientConnect, 1,
	 "clientConnect() -- Connect the server" },
	 { "clientIsEnable", (PyCFunction)Application::sClientIsEnable, 1,
	 "clientIsEnable() -- Check client is enable" },
	 { "clientGetConnectState", (PyCFunction)Application::sClientGetConnectState, 1,
	 "clientGetConnectState() -- Client get connect state" },
	 { "clientGetState", (PyCFunction)Application::sClientGetState, 1,
	 "clientGetState() -- Client get state" },
	 { "clientSendFile", (PyCFunction)Application::sClientSendFile, 1,
	 "clientSendFile(path,name) -- Client Send m3d File" },
	 { "clientRequestReceiveFile", (PyCFunction)Application::sClientRequestReceiveFile, 1,
	 "clientRequestReceiveFile(fileName) -- Client Request Receive File" },
	 { "clientSendIdMsg", (PyCFunction)Application::sClientSendIdMsg, 1,
	 "clientSendMsg(msgId) -- Client send a id command" },
	 /*fubiao*/
	 { "clientLoginMsg", (PyCFunction)Application::sClientLoginMsg, 1,
	 "clientLoginMsg(msgId,password) -- Client send a login command" },

	 { "clientRegisterMsg", (PyCFunction)Application::sClientRegisterMsg, 1,
	 "registerMsg(msgId,password) -- Client send a register command" },
	 /*end*/
	 { "clientGetMsg", (PyCFunction)Application::sClientGetMsg, 1,
	 "clientGetMsg() -- try to get a msg" },
	 { "clientRunFileUseCount", (PyCFunction)Application::sClientRunFileUseCount, 1,
	 "clientRunFileUseCount() -- Run File Use Count" },
	 { "clientGetTransmissionRate", (PyCFunction)Application::sClientGetTransmissionRate, 1,
	 "clientGetTransmissionRate() -- Get transmission rate" },
	 { "clientWorkpath", (PyCFunction)Application::sClientWorkpath, 1,
	 "clientWorkpath() -- Get workpath from config.ini" },
	 { "clientUserDir", (PyCFunction)Application::sClientUserDir, 1,
	 "clientUserDir() -- Get user dir" },
	 { "clientSendWinMsg", (PyCFunction)Application::sClientSendWinMsg, 1,
	 "clientSendMsg(msgId,wParam,lParam) -- Client send a win command" },
	 { "clientClose", (PyCFunction)Application::sClientClose, 1,
	 "clientClose() -- Close the connect" },
	 { "clientGetServerIP", (PyCFunction)Application::sClientGetServerIP, 1,
	 "clientGetServerIP() -- client Get Server IP" },
	 { "clientSetServerIP", (PyCFunction)Application::sClientSetServerIP, 1,
	 "clientSetServerIP() -- client Set Server IP" },
	 { "clientGetWorkpath", (PyCFunction)Application::sClientGetWorkpath, 1,
	 "clientGetWorkpath() -- client Get Workpath" },
	 { "clientSetWorkpath", (PyCFunction)Application::sClientSetWorkpath, 1,
	 "clientSetWorkpath() -- client Set Workpath" },
	 { "setM3dPath", (PyCFunction)Application::sSetM3dpath, 1,
	 "setM3dPath() -- g" },
	 /*用户id和密码*/
	 { "clientSetUserId", (PyCFunction)Application::sClientSetUserId, 1,
	 "clientSetUserId(int) -- Connect the server" },
	 { "clientSetPassword", (PyCFunction)Application::sClientSetPassword, 1,
	 "clientSetPassword(string) -- Connect the server" },
	 { "clientGetUserId", (PyCFunction)Application::sClientGetUserId, 1,
	 "clientGetUserId() -- Connect the server" },
	 { "clientGetPassword", (PyCFunction)Application::sClientGetPassword, 1,
	 "clientGetPassword() -- Connect the server" },
	 /*end*/
	 { "getFigNameInfoListFromH5File", (PyCFunction)Application::sGetFigNameInfoListFromH5File, 1,
	 "getFigNameInfoListFromH5File() -- client Get FigNameInfoList From Hdf5File" },
	 { "getFigDataFromH5File", (PyCFunction)Application::sGetFigDataFromH5File, 1,
	 "getFigDataFromH5File() -- client Get FigData From Hdf5File" },
	 { NULL, NULL, 0, NULL }		/* Sentinel */
	
};


PyObject* Application::sLoadFile(PyObject * /*self*/, PyObject *args,PyObject * /*kwd*/)
{
    char *path, *doc="",*mod="";
    if (!PyArg_ParseTuple(args, "s|ss", &path, &doc, &mod))     // convert args: Python->C
        return 0;                             // NULL triggers exception
    try {
        Base::FileInfo fi(path);
        if (!fi.isFile() || !fi.exists()) {
            PyErr_Format(PyExc_IOError, "File %s doesn't exist.", path);
            return 0;
        }

        std::string module = mod;
        if (module.empty()) {
            std::string ext = fi.extension();
            std::vector<std::string> modules = GetApplication().getImportModules(ext.c_str());
            if (modules.empty()) {
                PyErr_Format(PyExc_IOError, "Filetype %s is not supported.", ext.c_str());
                return 0;
            }
            else {
                module = modules.front();
            }
        }

        std::stringstream str;
        str << "import " << module << std::endl;
        if (fi.hasExtension("FCStd"))
            str << module << ".openDocument('" << path << "')" << std::endl;
        else
            str << module << ".insert('" << path << "','" << doc << "')" << std::endl;
        Base::Interpreter().runString(str.str().c_str());
        Py_Return;
    }
    catch (const Base::Exception& e) {
        PyErr_SetString(PyExc_IOError, e.what());
        return 0;
    }
    catch (const std::exception& e) {
        // might be subclass from zipios
        PyErr_Format(PyExc_IOError, "Invalid project file %s: %s", path, e.what());
        return 0;
    }
}

PyObject* Application::sOpenDocument(PyObject * /*self*/, PyObject *args,PyObject * /*kwd*/)
{
    char* Name;
    if (!PyArg_ParseTuple(args, "et","utf-8",&Name))
        return NULL;
    std::string EncodedName = std::string(Name);
    PyMem_Free(Name);
    try {
		PyObject* doc = GetApplication().openDocument(EncodedName.c_str())->getPyObject();
		//std::string suffix = EncodedName.substr(EncodedName.find_last_of('.'), EncodedName.size());
		//if (stricmp(suffix.c_str(), ".FCStd") == 0)
		//{
		//	Gui::Application::Instance->open(EncodedName.c_str(), "FreeCAD");
		//}
		//else if (stricmp(suffix.c_str(), ".M3D") == 0)
		//{
		//	Gui::Application::Instance->open(EncodedName.c_str(), "importM3D");
		//}
		//else if (stricmp(suffix.c_str(), ".h5") == 0)
		//{
		//	Gui::Application::Instance->open(EncodedName.c_str(), "importHDF5");
		//}
		//else{
		//	std::cout << "can't open" << EncodedName << std::endl;
		//}
		Py_Return;
		//if (doc)
		//{
		//	//std::string suffix = "FCStd";
		//	////判断后缀是不是工程文件，若是加上监听
		//	//bool isSame = EncodedName.compare(EncodedName.size() - suffix.size(), suffix.size(), suffix) == 0;
		//	//if (isSame)
		//	//	Gui::Command::doCommand(
		//	//	Gui::Command::Doc, "import Modeling\nFreeCAD.addDocumentObserver(Modeling.Common.Tools.DocumentTools.DocumentObservers())");
		//	return doc;
		//}
    }
    catch (const Base::Exception& e) {
        PyErr_SetString(PyExc_IOError, e.what());
        return 0L;
    }
    catch (const std::exception& e) {
        // might be subclass from zipios
        PyErr_Format(PyExc_IOError, "Invalid project file %s: %s\n", EncodedName.c_str(), e.what());
        return 0L;
    }
}

PyObject* Application::sNewDocument(PyObject * /*self*/, PyObject *args,PyObject * /*kwd*/)
{
    char *docName = 0;
    char *usrName = 0;
    if (!PyArg_ParseTuple(args, "|etet", "utf-8", &docName, "utf-8", &usrName))
        return NULL;

    PY_TRY {
        App::Document* doc = GetApplication().newDocument(docName, usrName);
        PyMem_Free(docName);
        PyMem_Free(usrName);
        return doc->getPyObject();
    }PY_CATCH;
}

PyObject* Application::sSetActiveDocument(PyObject * /*self*/, PyObject *args,PyObject * /*kwd*/)
{
    char *pstr = 0;
    if (!PyArg_ParseTuple(args, "s", &pstr))     // convert args: Python->C
        return NULL;                             // NULL triggers exception

    try {
        GetApplication().setActiveDocument(pstr);
    }
    catch (const Base::Exception& e) {
        PyErr_SetString(Base::BaseExceptionFreeCADError, e.what());
        return NULL;
    }

    Py_Return;
}

PyObject* Application::sCloseDocument(PyObject * /*self*/, PyObject *args,PyObject * /*kwd*/)
{
    char *pstr = 0;
    if (!PyArg_ParseTuple(args, "s", &pstr))     // convert args: Python->C
        return NULL;                             // NULL triggers exception

    Document* doc = GetApplication().getDocument(pstr);
    if (!doc) {
        PyErr_Format(PyExc_NameError, "Unknown document '%s'", pstr);
        return NULL;
    }
    if (!doc->isClosable()) {
        PyErr_Format(PyExc_RuntimeError, "The document '%s' is not closable for the moment", pstr);
        return NULL;
    }

    if (GetApplication().closeDocument(pstr) == false) {
        PyErr_Format(PyExc_RuntimeError, "Closing the document '%s' failed", pstr);
        return NULL;
    }

    Py_Return;
}

PyObject* Application::sSaveDocument(PyObject * /*self*/, PyObject *args,PyObject * /*kwd*/)
{
    char *pDoc;
    if (!PyArg_ParseTuple(args, "s", &pDoc))     // convert args: Python->C
        return NULL;                             // NULL triggers exception

    Document* doc = GetApplication().getDocument(pDoc);
    if ( doc ) {
        if ( doc->save() == false ) {
            PyErr_Format(Base::BaseExceptionFreeCADError, "Cannot save document '%s'", pDoc);
            return 0L;
        }
    }
    else {
        PyErr_Format(PyExc_NameError, "Unknown document '%s'", pDoc);
        return NULL;
    }

    Py_Return;
}
#if 0
PyObject* Application::sSaveDocumentAs(PyObject * /*self*/, PyObject *args,PyObject * /*kwd*/)
{
    char *pDoc, *pFileName;
    if (!PyArg_ParseTuple(args, "ss", &pDoc, &pFileName))     // convert args: Python->C
        return NULL;                             // NULL triggers exception

    Document* doc = GetApplication().getDocument(pDoc);
    if (doc) {
        doc->saveAs( pFileName );
    }
    else {
        PyErr_Format(PyExc_NameError, "Unknown document '%s'", pDoc);
        return NULL;
    }

    Py_Return;
}
#endif
PyObject* Application::sActiveDocument(PyObject * /*self*/, PyObject *args,PyObject * /*kwd*/)
{
    if (!PyArg_ParseTuple(args, ""))     // convert args: Python->C
        return NULL;                       // NULL triggers exception

    Document* doc = GetApplication().getActiveDocument();
    if (doc) {
        return doc->getPyObject();
    }
    else {
        Py_INCREF(Py_None);
        return Py_None;
    }
}

PyObject* Application::sGetDocument(PyObject * /*self*/, PyObject *args,PyObject * /*kwd*/)
{
    char *pstr=0;
    if (!PyArg_ParseTuple(args, "s", &pstr))     // convert args: Python->C
        return NULL;                             // NULL triggers exception

    Document* doc = GetApplication().getDocument(pstr);
    if ( !doc ) {
        PyErr_Format(PyExc_NameError, "Unknown document '%s'", pstr);
        return 0L;
    }

    return doc->getPyObject();
}

PyObject* Application::sGetParam(PyObject * /*self*/, PyObject *args,PyObject * /*kwd*/)
{
    char *pstr=0;
    if (!PyArg_ParseTuple(args, "s", &pstr))     // convert args: Python->C
        return NULL;                             // NULL triggers exception

    PY_TRY {
        return GetPyObject(GetApplication().GetParameterGroupByPath(pstr));
    }PY_CATCH;
}

PyObject* Application::sSaveParameter(PyObject * /*self*/, PyObject *args,PyObject * /*kwd*/)
{
    char *pstr = "User parameter";
    if (!PyArg_ParseTuple(args, "|s", &pstr))
        return NULL;

    PY_TRY {
        ParameterManager* param = App::GetApplication().GetParameterSet(pstr);
        if (!param) {
            std::stringstream str;
            str << "No parameter set found with name: " << pstr;
            PyErr_SetString(PyExc_ValueError, str.str().c_str());
            return NULL;
        }
        else if (!param->HasSerializer()) {
            std::stringstream str;
            str << "Parameter set cannot be serialized: " << pstr;
            PyErr_SetString(PyExc_RuntimeError, str.str().c_str());
            return NULL;
        }

        param->SaveDocument();
        Py_INCREF(Py_None);
        return Py_None;
    }PY_CATCH;
}


PyObject* Application::sGetConfig(PyObject * /*self*/, PyObject *args,PyObject * /*kwd*/)
{
    char *pstr;

    if (!PyArg_ParseTuple(args, "s", &pstr))     // convert args: Python->C
        return NULL;                             // NULL triggers exception
    const std::map<std::string, std::string>& Map = GetApplication().Config();

    std::map<std::string, std::string>::const_iterator it = Map.find(pstr);
    if (it != Map.end()) {
        return Py_BuildValue("s",it->second.c_str());
    }
    else {
        // do not set an error because this may break existing python code
#if PY_MAJOR_VERSION >= 3
        return PyUnicode_FromString("");
#else
        return PyString_FromString("");
#endif
    }
}

PyObject* Application::sDumpConfig(PyObject * /*self*/, PyObject *args,PyObject * /*kwd*/)
{
    if (!PyArg_ParseTuple(args, "") )    // convert args: Python->C
        return NULL;                             // NULL triggers exception

    PyObject *dict = PyDict_New();
    for (std::map<std::string,std::string>::iterator It= GetApplication()._mConfig.begin();
         It!=GetApplication()._mConfig.end();++It) {
#if PY_MAJOR_VERSION >= 3
        PyDict_SetItemString(dict,It->first.c_str(), PyUnicode_FromString(It->second.c_str()));
#else
        PyDict_SetItemString(dict,It->first.c_str(), PyString_FromString(It->second.c_str()));
#endif
    }
    return dict;
}

PyObject* Application::sSetConfig(PyObject * /*self*/, PyObject *args,PyObject * /*kwd*/)
{
    char *pstr,*pstr2;

    if (!PyArg_ParseTuple(args, "ss", &pstr,&pstr2))  // convert args: Python->C
        return NULL; // NULL triggers exception

    GetApplication()._mConfig[pstr] = pstr2;

    Py_INCREF(Py_None);
    return Py_None;
}

PyObject* Application::sGetVersion(PyObject * /*self*/, PyObject *args,PyObject * /*kwd*/)
{
    if (!PyArg_ParseTuple(args, ""))     // convert args: Python->C
        return NULL; // NULL triggers exception

    Py::List list;
    const std::map<std::string, std::string>& cfg = Application::Config();
    std::map<std::string, std::string>::const_iterator it;

    it = cfg.find("BuildVersionMajor");
    list.append(Py::String(it != cfg.end() ? it->second : ""));

    it = cfg.find("BuildVersionMinor");
    list.append(Py::String(it != cfg.end() ? it->second : ""));

    it = cfg.find("BuildRevision");
    list.append(Py::String(it != cfg.end() ? it->second : ""));

    it = cfg.find("BuildRepositoryURL");
    list.append(Py::String(it != cfg.end() ? it->second : ""));

    it = cfg.find("BuildRevisionDate");
    list.append(Py::String(it != cfg.end() ? it->second : ""));

    it = cfg.find("BuildRevisionBranch");
    if (it != cfg.end())
        list.append(Py::String(it->second));

    it = cfg.find("BuildRevisionHash");
    if (it != cfg.end())
        list.append(Py::String(it->second));

    return Py::new_reference_to(list);
}

PyObject* Application::sAddImportType(PyObject * /*self*/, PyObject *args,PyObject * /*kwd*/)
{
    char *psKey,*psMod;

    if (!PyArg_ParseTuple(args, "ss", &psKey,&psMod))
        return NULL;

    GetApplication().addImportType(psKey,psMod);

    Py_Return;
}

PyObject* Application::sGetImportType(PyObject * /*self*/, PyObject *args,PyObject * /*kwd*/)
{
    char*       psKey=0;

    if (!PyArg_ParseTuple(args, "|s", &psKey))     // convert args: Python->C
        return NULL;                             // NULL triggers exception

    if (psKey) {
        Py::List list;
        std::vector<std::string> modules = GetApplication().getImportModules(psKey);
        for (std::vector<std::string>::iterator it = modules.begin(); it != modules.end(); ++it) {
            list.append(Py::String(*it));
        }

        return Py::new_reference_to(list);
    }
    else {
        Py::Dict dict;
        std::vector<std::string> types = GetApplication().getImportTypes();
        for (std::vector<std::string>::iterator it = types.begin(); it != types.end(); ++it) {
            std::vector<std::string> modules = GetApplication().getImportModules(it->c_str());
            if (modules.empty()) {
                dict.setItem(it->c_str(), Py::None());
            }
            else if (modules.size() == 1) {
                dict.setItem(it->c_str(), Py::String(modules.front()));
            }
            else {
                Py::List list;
                for (std::vector<std::string>::iterator jt = modules.begin(); jt != modules.end(); ++jt) {
                    list.append(Py::String(*jt));
                }
                dict.setItem(it->c_str(), list);
            }
        }

        return Py::new_reference_to(dict);
    }
}

PyObject* Application::sAddExportType(PyObject * /*self*/, PyObject *args,PyObject * /*kwd*/)
{
    char *psKey,*psMod;

    if (!PyArg_ParseTuple(args, "ss", &psKey,&psMod))
        return NULL;

    GetApplication().addExportType(psKey,psMod);

    Py_Return;
}

PyObject* Application::sGetExportType(PyObject * /*self*/, PyObject *args,PyObject * /*kwd*/)
{
    char*       psKey=0;

    if (!PyArg_ParseTuple(args, "|s", &psKey))     // convert args: Python->C
        return NULL;                             // NULL triggers exception

    if (psKey) {
        Py::List list;
        std::vector<std::string> modules = GetApplication().getExportModules(psKey);
        for (std::vector<std::string>::iterator it = modules.begin(); it != modules.end(); ++it) {
            list.append(Py::String(*it));
        }

        return Py::new_reference_to(list);
    }
    else {
        Py::Dict dict;
        std::vector<std::string> types = GetApplication().getExportTypes();
        for (std::vector<std::string>::iterator it = types.begin(); it != types.end(); ++it) {
            std::vector<std::string> modules = GetApplication().getExportModules(it->c_str());
            if (modules.empty()) {
                dict.setItem(it->c_str(), Py::None());
            }
            else if (modules.size() == 1) {
                dict.setItem(it->c_str(), Py::String(modules.front()));
            }
            else {
                Py::List list;
                for (std::vector<std::string>::iterator jt = modules.begin(); jt != modules.end(); ++jt) {
                    list.append(Py::String(*jt));
                }
                dict.setItem(it->c_str(), list);
            }
        }

        return Py::new_reference_to(dict);
    }
}

PyObject* Application::sGetResourceDir(PyObject * /*self*/, PyObject *args,PyObject * /*kwd*/)
{
    if (!PyArg_ParseTuple(args, ""))     // convert args: Python->C
        return NULL;                       // NULL triggers exception

    Py::String datadir(Application::getResourceDir(),"utf-8");
    return Py::new_reference_to(datadir);
}

PyObject* Application::sGetUserAppDataDir(PyObject * /*self*/, PyObject *args,PyObject * /*kwd*/)
{
    if (!PyArg_ParseTuple(args, ""))     // convert args: Python->C
        return NULL;                       // NULL triggers exception

    Py::String user_data_dir(Application::getUserAppDataDir(),"utf-8");
    return Py::new_reference_to(user_data_dir);
}

PyObject* Application::sGetUserMacroDir(PyObject * /*self*/, PyObject *args,PyObject * /*kwd*/)
{
    if (!PyArg_ParseTuple(args, ""))     // convert args: Python->C
        return NULL;                       // NULL triggers exception

    Py::String user_macro_dir(Application::getUserMacroDir(),"utf-8");
    return Py::new_reference_to(user_macro_dir);
}

PyObject* Application::sGetHelpDir(PyObject * /*self*/, PyObject *args,PyObject * /*kwd*/)
{
    if (!PyArg_ParseTuple(args, ""))     // convert args: Python->C
        return NULL;                       // NULL triggers exception

    Py::String user_macro_dir(Application::getHelpDir(),"utf-8");
    return Py::new_reference_to(user_macro_dir);
}

PyObject* Application::sGetHomePath(PyObject * /*self*/, PyObject *args,PyObject * /*kwd*/)
{
    if (!PyArg_ParseTuple(args, ""))     // convert args: Python->C
        return NULL;                       // NULL triggers exception

    Py::String homedir(GetApplication().getHomePath(),"utf-8");
    return Py::new_reference_to(homedir);
}

PyObject* Application::sListDocuments(PyObject * /*self*/, PyObject *args,PyObject * /*kwd*/)
{
    if (!PyArg_ParseTuple(args, ""))     // convert args: Python->C
        return NULL;                       // NULL triggers exception
    PY_TRY {
        PyObject *pDict = PyDict_New();
        PyObject *pKey;
        Base::PyObjectBase* pValue;

        for (std::map<std::string,Document*>::const_iterator It = GetApplication().DocMap.begin();
             It != GetApplication().DocMap.end();++It) {
#if PY_MAJOR_VERSION >= 3
            pKey   = PyUnicode_FromString(It->first.c_str());
#else
            pKey   = PyString_FromString(It->first.c_str());
#endif
            // GetPyObject() increments
            pValue = static_cast<Base::PyObjectBase*>(It->second->getPyObject());
            PyDict_SetItem(pDict, pKey, pValue);
            // now we can decrement again as PyDict_SetItem also has incremented
            pValue->DecRef();
        }

        return pDict;
    } PY_CATCH;
}

PyObject* Application::sAddDocObserver(PyObject * /*self*/, PyObject *args,PyObject * /*kwd*/)
{
    PyObject* o;
    if (!PyArg_ParseTuple(args, "O",&o))
        return NULL;
    PY_TRY {
        DocumentObserverPython::addObserver(Py::Object(o));
        Py_Return;
    } PY_CATCH;
}

PyObject* Application::sRemoveDocObserver(PyObject * /*self*/, PyObject *args,PyObject * /*kwd*/)
{
    PyObject* o;
    if (!PyArg_ParseTuple(args, "O",&o))
        return NULL;
    PY_TRY {
        DocumentObserverPython::removeObserver(Py::Object(o));
        Py_Return;
    } PY_CATCH;
}
PyObject* Application::sRemoveAllDocObserver(PyObject * /*self*/, PyObject *args, PyObject * /*kwd*/)
{
	if (!PyArg_ParseTuple(args, ""))
		return NULL;
	PY_TRY{
		DocumentObserverPython::removeAllObserver();
		Py_Return;
	} PY_CATCH;
}
PyObject *Application::sSetLogLevel(PyObject * /*self*/, PyObject *args, PyObject * /*kwd*/)
{
    char *tag;
    PyObject *pcObj;
    if (!PyArg_ParseTuple(args, "sO", &tag, &pcObj))
        return NULL;
    PY_TRY{
        int l;
#if PY_MAJOR_VERSION < 3
        if (PyString_Check(pcObj)) {
            const char *pstr = PyString_AsString(pcObj);
#else
        if (PyUnicode_Check(pcObj)) {
            const char *pstr = PyUnicode_AsUTF8(pcObj);
#endif
            if(strcmp(pstr,"Log") == 0)
                l = FC_LOGLEVEL_LOG;
            else if(strcmp(pstr,"Warning") == 0)
                l = FC_LOGLEVEL_WARN;
            else if(strcmp(pstr,"Message") == 0)
                l = FC_LOGLEVEL_MSG;
            else if(strcmp(pstr,"Error") == 0)
                l = FC_LOGLEVEL_ERR;
            else if(strcmp(pstr,"Trace") == 0)
                l = FC_LOGLEVEL_TRACE;
            else if(strcmp(pstr,"Default") == 0)
                l = FC_LOGLEVEL_DEFAULT;
            else {
                Py_Error(Base::BaseExceptionFreeCADError,
                        "Unknown Log Level (use 'Default', 'Error', 'Warning', 'Message', 'Log', 'Trace' or an integer)");
                return NULL;
            }
        }else 
            l = PyLong_AsLong(pcObj);
        GetApplication().GetParameterGroupByPath("User parameter:BaseApp/LogLevels")->SetInt(tag,l);
        if(strcmp(tag,"Default") == 0) {
#ifndef FC_DEBUG
            if(l>=0) Base::Console().SetDefaultLogLevel(l);
#endif
        }else if(strcmp(tag,"DebugDefault") == 0) {
#ifdef FC_DEBUG
            if(l>=0) Base::Console().SetDefaultLogLevel(l);
#endif
        }else
            *Base::Console().GetLogLevel(tag) = l;
        Py_INCREF(Py_None);
        return Py_None;
    }PY_CATCH;
}

PyObject *Application::sGetLogLevel(PyObject * /*self*/, PyObject *args, PyObject * /*kwd*/)
{
    char *tag;
    if (!PyArg_ParseTuple(args, "s", &tag))
        return NULL;

    PY_TRY{
        int l = -1;
        if(strcmp(tag,"Default")==0) {
#ifdef FC_DEBUG
            l = _pcUserParamMngr->GetGroup("BaseApp/LogLevels")->GetInt(tag,-1);
#endif
        }else if(strcmp(tag,"DebugDefault")==0) {
#ifndef FC_DEBUG
            l = _pcUserParamMngr->GetGroup("BaseApp/LogLevels")->GetInt(tag,-1);
#endif
        }else{
            int *pl = Base::Console().GetLogLevel(tag,false);
            l = pl?*pl:-1;
        }
        // For performance reason, we only output integer value
        return Py_BuildValue("i",Base::Console().LogLevel(l));

        // switch(l) {
        // case FC_LOGLEVEL_LOG:
        //     return Py_BuildValue("s","Log");
        // case FC_LOGLEVEL_WARN:
        //     return Py_BuildValue("s","Warning");
        // case FC_LOGLEVEL_ERR:
        //     return Py_BuildValue("s","Error");
        // case FC_LOGLEVEL_MSG:
        //     return Py_BuildValue("s","Message");
        // case FC_LOGLEVEL_TRACE:
        //     return Py_BuildValue("s","Trace");
        // default:
        //     return Py_BuildValue("i",l);
        // }
    } PY_CATCH;
}
//utf8转gbk
static std::string UTF8ToGBK(const char* strUTF8)
{
	int len = MultiByteToWideChar(CP_UTF8, 0, strUTF8, -1, NULL, 0);
	wchar_t* wszGBK = new wchar_t[len + 1];
	memset(wszGBK, 0, len * 2 + 2);
	MultiByteToWideChar(CP_UTF8, 0, strUTF8, -1, wszGBK, len);
	len = WideCharToMultiByte(CP_ACP, 0, wszGBK, -1, NULL, 0, NULL, NULL);
	char* szGBK = new char[len + 1];
	memset(szGBK, 0, len + 1);
	WideCharToMultiByte(CP_ACP, 0, wszGBK, -1, szGBK, len, NULL, NULL);
	std::string strTemp(szGBK);

	if (wszGBK) delete[] wszGBK;
	if (szGBK) delete[] szGBK;

	return strTemp;
}

std:: string GbkToUtf8(const char *src_str)
{
	int len = MultiByteToWideChar(CP_ACP, 0, src_str, -1, NULL, 0);
	wchar_t* wstr = new wchar_t[len + 1];
	memset(wstr, 0, len + 1);
	MultiByteToWideChar(CP_ACP, 0, src_str, -1, wstr, len);
	len = WideCharToMultiByte(CP_UTF8, 0, wstr, -1, NULL, 0, NULL, NULL);
	char* str = new char[len + 1];
	memset(str, 0, len + 1);
	WideCharToMultiByte(CP_UTF8, 0, wstr, -1, str, len, NULL, NULL);
	std::string strTemp = str;
	if (wstr) delete[] wstr;
	if (str) delete[] str;
	return strTemp;
}


//客户端连接
PyObject *Application::sClientConnect(PyObject *self, PyObject *args, PyObject *kwd)
{
	if (!GetApplication().m_netServer)
	{
		using namespace PicNet;
		try
		{
			//初始化配置文件
			Singleton<PicNet::Config>::Instance(Config::GetProgramDir() + "\\config.ini");
			std::string workpath = "";
			if (!GetApplication().m_workpath.empty()){
				workpath = GetApplication().m_workpath + "\\File\\";
			}
			else{
				workpath = std::string(ConfigSingleton::GetInstance()->Get<std::string>("workpath") + "\\File\\");
			}
			//std::string 
			workpath = UTF8ToGBK(workpath.c_str());
			std::string ip=GetApplication().m_serverIP;
			if (ip.empty()){
				ip = ConfigSingleton::GetInstance()->Get<std::string>("ip");
			}
			//std::string ip = ConfigSingleton::GetInstance()->Get<std::string>("ip");
			int port = ConfigSingleton::GetInstance()->Get<int>("port");
			//std::cout << workpath << std::endl;
			_mkdir(workpath.c_str());
			GetApplication().m_netServer = new NetServer(false, ip, port,workpath);
		
			GetApplication().m_clientController = new SimpleClientController();
			GetApplication().m_clientController->Usercode = 123456 & 0x000FFFFF;
			//GetApplication().m_clientController->Usercode = time(nullptr)&0x000FFFFF;
			GetApplication().m_netServer->SetSessionCreateListener(GetApplication().m_clientController);

			//netServer.SetSessionCreateListener(&test);
			GetApplication().m_netServer->Initialize();
		}
		catch (const std::exception& e)
		{
			PyErr_Format(PyExc_IOError, "Client Connect Error:%s", e.what());
			return 0L;
		}

	}
	Py_Return;
}

//返回链接是否可用
PyObject *Application::sClientIsEnable(PyObject *self, PyObject *args, PyObject *kwd)
{
	//新控制部分需要这样返回
	return Py_BuildValue("O", Py_True);
	//连接成功
	if (GetApplication().m_netServer && GetApplication().m_netServer->GetConnectState()
		== PicNet::NetServer::ConnectState::CONNECTED)
	{
		return Py_BuildValue("O", Py_True);
	}
	else{
		return Py_BuildValue("O", Py_False);
	}
}

//返回用户目录
PyObject *Application::sClientWorkpath(PyObject *self, PyObject *args, PyObject *kwd)
{
	{
		using namespace PicNet;
		std::string userWorkPath = "";
		if (!GetApplication().m_workpath.empty())
		{
			userWorkPath = GetApplication().m_workpath;

		}
		else{
			//初始化配置文件
			Singleton<PicNet::Config>::Instance(Config::GetProgramDir() + "\\config.ini");
			//Singleton<PicNet::Config>::Instance(Config::GetProgramDir() + "\\config.ini");
			userWorkPath = ConfigSingleton::GetInstance()->Get<std::string>("workpath");
			//std::string workpath = std::string(GetApplication().getUserAppDataDir()+"\\File\\");//ConfigSingleton::GetInstance()->Get<std::string>("workpath");
			
		}
		std:: string workpath = std::string(userWorkPath + "\\");//ConfigSingleton::GetInstance()->Get<std::string>("workpath");
		workpath = UTF8ToGBK(workpath.c_str());

		return Py_BuildValue("s", workpath.c_str());
	}

}

//返回用户目录
PyObject *Application::sClientUserDir(PyObject *self, PyObject *args, PyObject *kwd)
{
	//连接成功
	if (GetApplication().m_clientController && GetApplication().m_clientController->Usercode)
	{
		using namespace PicNet;
		std::string workpath = "";
		if (!GetApplication().m_workpath.empty())
		{
			workpath = GetApplication().m_workpath + "\\File\\";;
		}
		else
		{
			//初始化配置文件
			Singleton<PicNet::Config>::Instance(Config::GetProgramDir() + "\\config.ini");
			workpath = ConfigSingleton::GetInstance()->Get<std::string>("workpath") + "\\File\\";
		}

		workpath = UTF8ToGBK(workpath.c_str());
		std::string userdir = workpath
			+ "\\" + std::to_string(GetApplication().m_clientController->Usercode) + "\\";
		/*std::string workpath = std::string(GetApplication().getUserAppDataDir()+"\\File\\");
		std::string userdir = workpath
			+ "\\" + std::to_string(GetApplication().m_clientController->Usercode) + "\\";*/
		return Py_BuildValue("s", userdir.c_str());
	}
	else{
		return Py_BuildValue("s", "");
	}
}



//返回链接是否可用
PyObject *Application::sClientGetConnectState(PyObject *self, PyObject *args, PyObject *kwd)
{
	//连接成功
	if (GetApplication().m_netServer)
	{
		return Py_BuildValue("i", GetApplication().m_netServer->GetConnectState());
	}
	else{
		return Py_BuildValue("i", -1);
	}
}

//得到链接状态
PyObject *Application::sClientGetState(PyObject *self, PyObject *args, PyObject *kwd)
{
	Py_Return;
}

//发送并且运行程序
PyObject *Application::sClientSendFile(PyObject *self, PyObject *args, PyObject *kwd)
{

	char* path = 0;
	char* name = 0;
	int id = 0;
	if (!PyArg_ParseTuple(args, "iss",&id, &path, &name))     // convert args: Python->C
		return NULL;

	//std::string pathGBK = UTF8ToGBK(const_cast<char*>(path));

	if (GetApplication().m_clientController 
		&& GetApplication().m_clientController->SendFile(id, std::string(/*pathGBK.c_str()*/path), std::string(name)))
	{
		return Py_BuildValue("O", Py_True);
	}


	return Py_BuildValue("O", Py_False);
}

//得到远程文件
PyObject *Application::sClientShowRemoteFile(PyObject *self, PyObject *args, PyObject *kwd)
{
	Py_Return;
}

//请求接收某个文件
PyObject *Application::sClientRequestReceiveFile(PyObject *self, PyObject *args, PyObject *kwd)
{

	char* name = 0;
	if (!PyArg_ParseTuple(args, "s", &name)) 
		return NULL;

	if (GetApplication().m_clientController
		&& GetApplication().m_clientController->SendStrMsg(1, std::string(name)))
	{
		return Py_BuildValue("O", Py_True);
	}
	return Py_BuildValue("O", Py_False);

}

//发送一个消息
PyObject *Application::sClientSendIdMsg(PyObject *self, PyObject *args, PyObject *kwd)
{

	int id;

	if (!PyArg_ParseTuple(args, "i", &id))
		return NULL;

	if (GetApplication().m_clientController
		&& GetApplication().m_clientController->SendIdMsg(id))
	{
		return Py_BuildValue("O", Py_True);
	}
	return Py_BuildValue("O", Py_False);
}
//发送一个Win消息
PyObject *Application::sClientSendWinMsg(PyObject *self, PyObject *args, PyObject *kwd)
{

	int id;
	int wParam;
	int lParam;

	if (!PyArg_ParseTuple(args, "iii", &id, &wParam,&lParam))
		return NULL;
	//新控制部分的看图接口，暂时使用
	if (id == 109 || id == 107)
	{
		auto contor = ContorlInterface::GetInstance();
		contor->senWinMessage(id, wParam, lParam);
	}
	

	if (GetApplication().m_clientController
		&& GetApplication().m_clientController->SendWinMsg(id,wParam,lParam))
	{
		return Py_BuildValue("O", Py_True);
	}
	return Py_BuildValue("O", Py_False);
}
//发送一个登陆消息
PyObject *Application::sClientLoginMsg(PyObject *self, PyObject *args, PyObject *kwd)
{
	int userId=-1;
	const char * password=0;

	if (!PyArg_ParseTuple(args, "is",&userId, &password))
		return NULL;
	GetApplication().m_clientController->Usercode = userId & 0x000FFFFF;
	PicNet::UserInfoPtr userPtr(new PicNet::UserInfo(userId,password));

	string userInfoStr = userPtr->ToJsonStr();

	if (GetApplication().m_clientController
		&& GetApplication().m_clientController->SendStrMsg(3,userInfoStr))
	{
		return Py_BuildValue("O", Py_True);
	}
	return Py_BuildValue("O", Py_False);
}
//注册消息
PyObject *Application::sClientRegisterMsg(PyObject *self, PyObject *args, PyObject *kwd){
	int userId = -1;
	const char * password = 0;

	if (!PyArg_ParseTuple(args, "is", &userId, &password))
		return NULL;
	GetApplication().m_clientController->Usercode = userId & 0x000FFFFF;
	PicNet::UserInfoPtr userPtr(new PicNet::UserInfo(userId, password));

	string userInfoStr = userPtr->ToJsonStr();

	if (GetApplication().m_clientController
		&& GetApplication().m_clientController->SendStrMsg(4, userInfoStr))
	{
		return Py_BuildValue("O", Py_True);
	}
	return Py_BuildValue("O", Py_False);
}

PyObject *Application::sClientSetUserId(PyObject *self, PyObject *args, PyObject *kwd){
	int userId = -1;
	if (!PyArg_ParseTuple(args, "i", &userId))
		return NULL;
	GetApplication().m_userId = userId;
	Py_Return;
}
PyObject *Application::sClientGetUserId(PyObject *self, PyObject *args, PyObject *kwd){
	return Py_BuildValue("i", GetApplication().m_userId);
}

PyObject *Application::sClientSetPassword(PyObject *self, PyObject *args, PyObject *kwd){
	const char * password = "";
	if (!PyArg_ParseTuple(args, "s", &password))
		return NULL;
	GetApplication().m_password = password;
	Py_Return;
}
PyObject *Application::sClientGetPassword(PyObject *self, PyObject *args, PyObject *kwd){
	return Py_BuildValue("s", GetApplication().m_password.c_str());
}
//获取发送或者接收的比例
PyObject *Application::sClientGetTransmissionRate(PyObject *self, PyObject *args, PyObject *kwd)
{

	if (!PyArg_ParseTuple(args, ""))
		return NULL;

	if (GetApplication().m_clientController)
	{
		return Py_BuildValue("f", GetApplication().m_clientController->GetTransmissionRate());
	}
	return Py_BuildValue("f", 0);
}


//取出一个消息
PyObject *Application::sClientGetMsg(PyObject *self, PyObject *args, PyObject *kwd)
{
	if (!PyArg_ParseTuple(args, ""))     // convert args: Python->C
		return NULL;
	if (GetApplication().m_clientController &&GetApplication().m_clientController->ExistReceiveMsg())
	{
		auto msg = GetApplication().m_clientController->GetMsg();
		switch (msg->GetType())
		{

		case PicNet::NetMsgHeader::ID_COMMAD:
			return Py::new_reference_to(Py_BuildValue("{s:i,s:i}",
				"Type", msg->GetType(),
				"Id", msg->GetId()));

		case PicNet::NetMsgHeader::MSG_COMMAD:
			{
				PicNet::WinMsgInfo wInfo = *(msg->CastBody<PicNet::WinMsgInfo*>());
				return Py::new_reference_to(Py_BuildValue("{s:i,s:i,s:i,s:i}",
				"Type", msg->GetType(),
				"Id", msg->GetId(),
				"wParam", wInfo.wParam,
				"lParam", wInfo.lParam));
			}
			
		case PicNet::NetMsgHeader::STRING:
		{
			std::string infoStr = *(msg->CastBody<std::string*>());
			return Py::new_reference_to(Py_BuildValue("{s:i,s:i,s:s}",
				"Type", msg->GetType(),
				"Id", msg->GetId(),
				"String", infoStr.c_str()));
		}
		case PicNet::NetMsgHeader::FILE_CONENT:
		{			
			PicNet::FileInfo fileInfo = *(msg->CastBody<PicNet::FileInfo*>());
			return Py::new_reference_to(Py_BuildValue("{s:i,s:i,s:s}",
				"Type", msg->GetType(),
				"Id", msg->GetId(),
				"FileName", fileInfo.Name));
		}
		default:
			break;
		}
	}
	//返回字典 Type:0 表示无消息
	return Py::new_reference_to(Py_BuildValue("{s:i}", "Type", 0));
}

//关闭客户端链接
PyObject *Application::sClientClose(PyObject *self, PyObject *args, PyObject *kwd)
{
	if (!PyArg_ParseTuple(args, ""))     // convert args: Python->C
		return NULL;

	if (GetApplication().m_netServer)
	{
		GetApplication().m_netServer->Finalize();
		delete GetApplication().m_netServer;
		GetApplication().m_netServer = nullptr;
	
	}
	if (GetApplication().m_clientController)
	{
		delete GetApplication().m_clientController;
		GetApplication().m_clientController = nullptr;
	}
	Py_Return;
}

//获取工作路径
PyObject *Application::sClientGetWorkpath(PyObject *self, PyObject *args, PyObject *kwd)
{
	if (!PyArg_ParseTuple(args, ""))     // convert args: Python->C
		return NULL;
	using namespace PicNet;
	if (!GetApplication().m_workpath.empty())
	{
		return Py_BuildValue("s", GetApplication().m_workpath.c_str());
	}
	try{
		//初始化配置文件
		Singleton<PicNet::Config>::Instance(Config::GetProgramDir() + "\\config.ini");


		std::string workpath = ConfigSingleton::GetInstance()->Get<std::string>("workpath");
		GetApplication().m_workpath = workpath.c_str();
		return Py_BuildValue("s", workpath.c_str());
	}
	catch (std::exception& e)
	{
		PyErr_Format(PyExc_IOError, "Read Error:%s", e.what());
		return 0L;
	}
	Py_Return;
}
int CN2Unicode(char *input, wchar_t *output)
{
	int len = strlen(input);

	//wchar_t *out = (wchar_t *) malloc(len*sizeof(wchar_t));

	len = MultiByteToWideChar(CP_ACP, 0, input, -1, output, MAX_PATH);

	return 1;
}
PyObject* Application::sSetM3dpath(PyObject *self, PyObject *args, PyObject *kwd)
{
	char* workpath = 0;
	wchar_t *unicodeWorkpath = 0;
	if (!PyArg_ParseTuple(args, "s", &workpath))     // convert args: Python->C
		return NULL;
	std::cerr << workpath << std::endl;
	//CN2Unicode(workpath, unicodeWorkpath);
	auto contorl = ContorlInterface::GetInstance();
	contorl->setM3dPath(workpath);
	Py_Return;
}

//设置工作路径
PyObject *Application::sClientSetWorkpath(PyObject *self, PyObject *args, PyObject *kwd)
{
	char* workpath = 0;
	wchar_t *unicodeWorkpath = 0;
	if (!PyArg_ParseTuple(args, "s", &workpath))     // convert args: Python->C
		return NULL;
	//CN2Unicode(workpath, unicodeWorkpath);
	GetApplication().m_workpath = string(workpath);
	Py_Return;
}


//获取服务器Ip
PyObject *Application::sClientGetServerIP(PyObject *self, PyObject *args, PyObject *kwd)
{
	if (!PyArg_ParseTuple(args, ""))     // convert args: Python->C
		return NULL;
	using namespace PicNet;
	if (!GetApplication().m_serverIP.empty())
	{
		return Py_BuildValue("s", GetApplication().m_serverIP.c_str());
	}
	try{
		//初始化配置文件
		Singleton<PicNet::Config>::Instance(Config::GetProgramDir() + "\\config.ini");


		std::string ip = ConfigSingleton::GetInstance()->Get<std::string>("ip");
		GetApplication().m_serverIP = ip;
		return Py_BuildValue("s", ip.c_str());
	}
	catch (std::exception& e)
	{
		PyErr_Format(PyExc_IOError, "Read Error:%s", e.what());
		return 0L;
	}
	Py_Return;
}



//设置服务器Ip
PyObject *Application::sClientSetServerIP(PyObject *self, PyObject *args, PyObject *kwd)
{
	char* ip = 0;
	if (!PyArg_ParseTuple(args, "s", &ip))     // convert args: Python->C
		return NULL;
	GetApplication().m_serverIP = string(ip);
	Py_Return;
}



//设置并行数量的文件进行运行
PyObject *Application::sClientRunFileUseCount(PyObject *self, PyObject *args, PyObject *kwd)
{
	int count = 0;
	if (!PyArg_ParseTuple(args, "i", &count))     // convert args: Python->C
		return NULL;
	if (GetApplication().m_clientController
		&& GetApplication().m_clientController->SendStrMsg(2, std::to_string(count)))
	{
		return Py_BuildValue("O", Py_True);
	}
	return Py_BuildValue("O", Py_False);
}

PyObject* StringToPyByWin(std::string str)
{
	int wlen = ::MultiByteToWideChar(CP_ACP, NULL, str.c_str(), int(str.size()), NULL, 0);
	wchar_t* wszString = new wchar_t[wlen + 1];
	::MultiByteToWideChar(CP_ACP, NULL, str.c_str(), int(str.size()), wszString, wlen);
	wszString[wlen] = '\0';
	PyObject* pobj = PyUnicode_FromUnicode((const Py_UNICODE*)wszString, wlen);
	delete wszString;
	return pobj;
}

PyObject *Application::sGetFigNameInfoListFromH5File(PyObject *self, PyObject *args, PyObject *kwd)
{
	char* fileName = 0;
	if (!PyArg_ParseTuple(args, "s", &fileName))
		return NULL;
	
	try
	{
	std::string path = UTF8ToGBK(fileName);
	Hdf5IO *h5 = new Hdf5IO(path);
	QList<FigNameInfo> figNameInfoList = h5->getFigNameInfo();
	h5->close();
	
	
	//新建一个参数列表,返回FigNameInfoList
	PyObject *data = PyTuple_New(figNameInfoList.size());
	
	for (int i = 0; i < figNameInfoList.size(); i++)
	{
		//初始化一个列表
		PyObject *pyParams = PyList_New(0);
		//std::cerr << figNameInfoList[i].type << "type\n";
		//std::cerr << figNameInfoList[i].groupName << "groupId\n";
		PyList_Append(pyParams, StringToPyByWin(figNameInfoList[i].type));
		std::cerr << figNameInfoList[i].type << std::endl;
		PyList_Append(pyParams, StringToPyByWin(figNameInfoList[i].groupName));
		PyObject *pyParams2 = PyList_New(0);//初始化一个列表
		for (int j = 0; j < figNameInfoList[i].headList.size(); j++)
		{	
			PyList_Append(pyParams2, StringToPyByWin(figNameInfoList[i].headList[j].toStdString()));
		}
		PyList_Append(pyParams, pyParams2);
		PyTuple_SetItem(data, i, pyParams);//设置该列表此位置的值
	}
	return data;
	}
	catch (...)
	{
		std::cerr << "sGetFigNameInfoListFromH5File failure\n";
		return NULL;
	}
	
}




//获取绘图数据
PyObject *Application::sGetFigDataFromH5File(PyObject *self, PyObject *args, PyObject *kwd)
{
	char* fileName = 0;
	char* groupName = 0;
	char* subgroupName = 0;
	char* subsubgroupName = 0;

	if (!PyArg_ParseTuple(args, "ssss", &fileName, &groupName, &subgroupName, &subsubgroupName))
		return NULL;
	FigData figdata;
	try
	{
	std::string path = UTF8ToGBK(fileName);
	Hdf5IO *h5 = new Hdf5IO(path);
	if (string(subsubgroupName) == "null")
		 figdata = h5->getSingleFigData(string(groupName), string(subgroupName));
	else
		 figdata = h5->getFigData(string(groupName), string(subgroupName), string(subsubgroupName));
	h5->close();
	//新建一个参数列表，返回数据信息
	PyObject *data = PyTuple_New(3);
	PyObject *headPyParams = PyList_New(0);//初始化一个列表

	for (int i = 0; i < figdata.headList.size(); i++)
	{
		//std::cerr << figdata.headList[i].toStdString() << "head\n";
		PyList_Append(headPyParams, StringToPyByWin(figdata.headList[i].toStdString()));
	}
	//设置该列表此位置的值
	PyTuple_SetItem(data, 0, headPyParams);

	PyObject *dataPyParams = PyList_New(0);//初始化一个列表
	for (int i = 0; i < figdata.dataSetList.size(); i++)
	{
		PyObject *pyParams = PyList_New(0);//初始化一个列表
		for (int j = 0; j < figdata.dataSetList[i].size(); j++)
		{
			//std::cerr << figdata.dataSetList[i][j] << "data\n";
			PyList_Append(pyParams, Py_BuildValue("f", figdata.dataSetList[i][j]));
		}
		PyList_Append(dataPyParams, pyParams);
		
	}
	//设置该列表此位置的值
	PyTuple_SetItem(data, 1, dataPyParams);

	PyObject *sizePyParams = PyList_New(0);//初始化一个列表
	for (int i = 0; i < figdata.dataSizeList.size(); i++)
	{
		PyObject *pyParams = PyList_New(0);//初始化一个列表
		for (int j = 0; j < figdata.dataSizeList[i].size(); j++)
		{
			PyList_Append(pyParams, Py_BuildValue("i", figdata.dataSizeList[i][j]));
		}
		PyList_Append(sizePyParams, pyParams);

	}
	//设置该列表此位置的值
	PyTuple_SetItem(data, 2, sizePyParams);
	return  data;
	}
	catch (...)
	{
		std::cerr << "sGetFigDataFromH5File failure\n";
		return NULL;
	}
}