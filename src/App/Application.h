/***************************************************************************
 *   (c) Jürgen Riegel (juergen.riegel@web.de) 2002                        *   
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

#ifndef APP_APPLICATION_H
#define APP_APPLICATION_H

#include <boost/signal.hpp>
#include <boost/signals2.hpp>

#include <vector>

#include <Base/PyObjectBase.h>
#include <Base/Parameter.h>
#include <Base/Observer.h>

#include "NetServer.hpp"
#include "SimpleClientController.hpp"

namespace Base 
{
    class ConsoleObserverStd; 
    class ConsoleObserverFile;
}

namespace App
{

class Document;
class DocumentObject;
class ApplicationObserver;
class Property;



/** The Application
 *  The root of the whole application
 *  @see App::Document
 */
class AppExport Application
{

public:

    //---------------------------------------------------------------------
    // exported functions goes here +++++++++++++++++++++++++++++++++++++++
    //---------------------------------------------------------------------

    /** @name methods for document handling */
    //@{
    /** Creates a new document
     * The first name is a the identifier and some kind of an internal (english)
     * name. It has to be like an identifier in a programming language, with no
     * spaces and not starting with a number. This name gets also forced to be unique
     * in this Application. You can avoid the renaming by using getUniqueDocumentName()
     * to get a unique name before calling newDoucument().
     * The second name is a UTF8 name of any kind. It's that name normally shown to 
     * the user and stored in the App::Document::Name property.
     */
    App::Document* newDocument(const char * Name=0l, const char * UserName=0l);
	//新建一个文本编辑器工程
	App::Document* newDocument(Document* doc,const char * Name = 0l, const char * UserName = 0l);
	App::Document* newDocumentM3dText(const char * Name = 0l, const char * UserName = 0l);
	//DocumentManager* newDocumentM3dText(const char * Name = 0l, const char * UserName = 0l);
	App::Document* newDocumentM2dText(const char * Name = 0l, const char * UserName = 0l);
	App::Document* newDocumentM3dMode(const char * Name = 0l, const char * UserName = 0l);
	App::Document* newDocumentM2dMod(const char * Name = 0l, const char * UserName = 0l);
	App::Document* newDocumentH5(const char * Name = 0l, const char * UserName = 0l);
    /// Closes the document \a name and removes it from the application.
    bool closeDocument(const char* name);
    /// find a unique document name
    std::string getUniqueDocumentName(const char *Name) const;
    /// Open an existing document from a file
    App::Document* openDocument(const char * FileName=0l);
	App::Document* openDocument3dMod(const char * FileName = 0l);
	App::Document* openDocument2dMod(const char * FileName = 0l);
    /// Retrieve the active document
    App::Document* getActiveDocument(void) const;
    /// Retrieve a named document
    App::Document* getDocument(const char *Name) const;
    /// gets the (internal) name of the document
    const char * getDocumentName(const App::Document* ) const;
    /// get a list of all documents in the application
    std::vector<App::Document*> getDocuments() const;
    /// Set the active document
    void setActiveDocument(App::Document* pDoc);
    void setActiveDocument(const char *Name);
    /// close all documents (without saving)
    void closeAllDocuments(void);
    //@}

    /** @name Signals of the Application */
    //@{
    /// signal on new Document
    boost::signal<void (const Document&)> signalNewDocument;
    /// signal on document getting deleted
    boost::signal<void (const Document&)> signalDeleteDocument;
    /// signal on already deleted Document
    boost::signal<void ()> signalDeletedDocument;
    /// signal on relabeling Document (user name)
    boost::signal<void (const Document&)> signalRelabelDocument;
    /// signal on renaming Document (internal name)
    boost::signal<void (const Document&)> signalRenameDocument;
    /// signal on activating Document
    boost::signal<void (const Document&)> signalActiveDocument;
    /// signal on saving Document
    boost::signal<void (const Document&)> signalSaveDocument;
    /// signal on starting to restore Document
    boost::signal<void (const Document&)> signalStartRestoreDocument;
    /// signal on restoring Document
    boost::signal<void (const Document&)> signalFinishRestoreDocument;
    /// signal on undo in document
    boost::signal<void (const Document&)> signalUndoDocument;
    /// signal on redo in document
    boost::signal<void (const Document&)> signalRedoDocument;
	/*fubiao*/
	/// signal on recomputed document
	boost::signal<void(const App::Document&)> signalRecomputed;
	/// signal on recomputed document object
	boost::signal<void(const App::DocumentObject&)> signalObjectRecomputed;
    //@}


    /** @name Signals of the document
     * This signals are an aggregation of all document. If you only 
     * the signal of a special document connect to the document itself
     */
    //@{
    /// signal on new Object
    boost::signal<void (const App::DocumentObject&)> signalNewObject;
    //boost::signal<void (const App::DocumentObject&)>     m_sig;
    /// signal on deleted Object
    boost::signal<void (const App::DocumentObject&)> signalDeletedObject;
    /// signal on changed Object
    boost::signal<void (const App::DocumentObject&, const App::Property&)> signalChangedObject;
	/*/// signal on changed Object
	boost::signal<void(const App::DocumentObject&, const App::Property&)> signalBeforeChangeObject;*/

    /// signal on relabeled Object
    boost::signal<void (const App::DocumentObject&)> signalRelabelObject;
    /// signal on activated Object
    boost::signal<void (const App::DocumentObject&)> signalActivatedObject;
    //@}

    /** @name Signals of property changes
     * These signals are emitted on property additions or removal.
     * The changed object can be any sub-class of PropertyContainer.
     */
    //@{
    /// signal on adding a dynamic property
    boost::signal<void (const App::Property&)> signalAppendDynamicProperty;
    /// signal on about removing a dynamic property
    boost::signal<void (const App::Property&)> signalRemoveDynamicProperty;
    /// signal on about changing the editor mode of a property
    boost::signal<void (const App::Property&)> signalChangePropertyEditor;
    //@}


    /** @name methods for parameter handling */
    //@{
    /// returns the system parameter
    ParameterManager &                                GetSystemParameter(void) ;
    /// returns the user parameter
    ParameterManager &                                GetUserParameter(void) ;
    /** Gets a parameter group by a full qualified path
     * It's an easy method to get a group:
     * \code
     * // getting standard parameter
     * ParameterGrp::handle hGrp = App::GetApplication().GetParameterGroupByPath("User parameter:BaseApp/Preferences/Mod/Raytracing");
     * std::string cDir             = hGrp->GetASCII("ProjectPath", "");
     * std::string cCameraName      = hGrp->GetASCII("CameraName", "TempCamera.inc");
     * \endcode
     */
    Base::Reference<ParameterGrp>                     GetParameterGroupByPath(const char* sName);

    ParameterManager *                                GetParameterSet(const char* sName) const;
    const std::map<std::string,ParameterManager *> &  GetParameterSetList(void) const;
    void AddParameterSet(const char* sName);
    void RemoveParameterSet(const char* sName);
    //@}

    /** @name methods for the open handler 
     *  With this facility a Application module can register 
     *  a ending (filetype) which he can handle to open. 
     *  The ending and the module name are stored and if the file
     *  type is opened the module get loaded and need to register a
     *  OpenHandler class in the OpenHandlerFactorySingleton. 
     *  After the module is loaded a OpenHandler of this type is created
     *  and the file get loaded.
     *  @see OpenHandler
     *  @see OpenHandlerFactorySingleton
     */
    //@{
    /// Register an import filetype and a module name
    void addImportType(const char* Type, const char* ModuleName);
    /// Return a list of modules that support the given filetype.
    std::vector<std::string> getImportModules(const char* Type) const;
    /// Return a list of all modules.
    std::vector<std::string> getImportModules() const;
    /// Return a list of filetypes that are supported by a module.
    std::vector<std::string> getImportTypes(const char* Module) const;
    /// Return a list of all filetypes.
    std::vector<std::string> getImportTypes(void) const;
    /// Return the import filters with modules of a given filetype.
    std::map<std::string, std::string> getImportFilters(const char* Type) const;
    /// Return a list of all import filters.
    std::map<std::string, std::string> getImportFilters(void) const;
    //@}
    //@{
    /// Register an export filetype and a module name
    void addExportType(const char* Type, const char* ModuleName);
    /// Return a list of modules that support the given filetype.
    std::vector<std::string> getExportModules(const char* Type) const;
    /// Return a list of all modules.
    std::vector<std::string> getExportModules() const;
    /// Return a list of filetypes that are supported by a module.
    std::vector<std::string> getExportTypes(const char* Module) const;
    /// Return a list of all filetypes.
    std::vector<std::string> getExportTypes(void) const;
    /// Return the export filters with modules of a given filetype.
    std::map<std::string, std::string> getExportFilters(const char* Type) const;
    /// Return a list of all export filters.
    std::map<std::string, std::string> getExportFilters(void) const;
    //@}
	
	PicNet::NetServer* m_netServer;
	PicNet::SimpleClientController * m_clientController;

	std::string m_serverIP;

	std::string m_workpath;

	int m_userId=-1;
	std::string m_password="";
    /** @name Init, Destruct an Access methods */
    //@{
    static void init(int argc, char ** argv);
    static void initTypes(void);
    static void destruct(void);
    static void destructObserver(void);
    static void processCmdLineFiles(void);
    static std::list<std::string> getCmdLineFiles();
    static std::list<std::string> processFiles(const std::list<std::string>&);
    static void runApplication(void);
    friend Application &GetApplication(void);
    static std::map<std::string,std::string> &Config(void){return mConfig;}
    static int GetARGC(void){return _argc;}
    static char** GetARGV(void){return _argv;}
    //@}

    /** @name Application directories */
    //@{
    const char* getHomePath(void) const;
    const char* getExecutableName(void) const;
    /*!
     Returns the temporary directory. By default, this is set to the
     system's temporary directory but can be customized by the user.
     */
    static std::string getTempPath();
    static std::string getTempFileName(const char* FileName=0);
    static std::string getUserAppDataDir();
    static std::string getUserMacroDir();
    static std::string getResourceDir();
    static std::string getHelpDir();
    //@}

    friend class App::Document;

protected:
    /// get called by the document when the name is changing
    void renameDocument(const char *OldName, const char *NewName);

    /** @name I/O of the document 
     * This slot get connected to all App::Documents created
     */
    //@{
    void slotNewObject(const App::DocumentObject&);
    void slotDeletedObject(const App::DocumentObject&);
    void slotChangedObject(const App::DocumentObject&, const App::Property& Prop);
    void slotRelabelObject(const App::DocumentObject&);
    void slotActivatedObject(const App::DocumentObject&);
    void slotUndoDocument(const App::Document&);
    void slotRedoDocument(const App::Document&);
	/*fubiao*/
	void slotRecomputedObject(const App::DocumentObject&);
	void slotRecomputed(const App::Document&);
	/*
	void slotBeforeChangeObject(const App::DocumentObject&, const App::Property& Prop);
	*/
    //@}

private:
    /// Constructor
    Application(std::map<std::string,std::string> &mConfig);
    /// Destructor
    virtual ~Application();

    /** @name member for parameter */
    //@{
    static ParameterManager *_pcSysParamMngr;
    static ParameterManager *_pcUserParamMngr;
    //@}


    //---------------------------------------------------------------------
    // python exports goes here +++++++++++++++++++++++++++++++++++++++++++
    //---------------------------------------------------------------------

    // static python wrapper of the exported functions
    static PyObject* sGetParam          (PyObject *self,PyObject *args,PyObject *kwd);
    static PyObject* sSaveParameter     (PyObject *self,PyObject *args,PyObject *kwd);
    static PyObject* sGetVersion        (PyObject *self,PyObject *args,PyObject *kwd);
    static PyObject* sGetConfig         (PyObject *self,PyObject *args,PyObject *kwd);
    static PyObject* sSetConfig         (PyObject *self,PyObject *args,PyObject *kwd);
    static PyObject* sDumpConfig        (PyObject *self,PyObject *args,PyObject *kwd);
    static PyObject* sTemplateAdd       (PyObject *self,PyObject *args,PyObject *kwd);
    static PyObject* sTemplateDelete    (PyObject *self,PyObject *args,PyObject *kwd);
    static PyObject* sTemplateGet       (PyObject *self,PyObject *args,PyObject *kwd);
    static PyObject* sAddImportType     (PyObject *self,PyObject *args,PyObject *kwd);
    static PyObject* sGetImportType     (PyObject *self,PyObject *args,PyObject *kwd);
    static PyObject* sAddExportType     (PyObject *self,PyObject *args,PyObject *kwd);
    static PyObject* sGetExportType     (PyObject *self,PyObject *args,PyObject *kwd);
    static PyObject* sGetResourceDir    (PyObject *self,PyObject *args,PyObject *kwd);
    static PyObject* sGetUserAppDataDir (PyObject *self,PyObject *args,PyObject *kwd);
    static PyObject* sGetUserMacroDir   (PyObject *self,PyObject *args,PyObject *kwd);
    static PyObject* sGetHelpDir        (PyObject *self,PyObject *args,PyObject *kwd);
    static PyObject* sGetHomePath       (PyObject *self,PyObject *args,PyObject *kwd);

    static PyObject* sLoadFile          (PyObject *self,PyObject *args,PyObject *kwd);
    static PyObject* sOpenDocument      (PyObject *self,PyObject *args,PyObject *kwd);
    static PyObject* sSaveDocument      (PyObject *self,PyObject *args,PyObject *kwd);
    static PyObject* sSaveDocumentAs    (PyObject *self,PyObject *args,PyObject *kwd);
    static PyObject* sNewDocument       (PyObject *self,PyObject *args,PyObject *kwd);
	static PyObject* sNewDocumentM3dMod(PyObject *self, PyObject *args, PyObject *kwd);
	static PyObject* sNewDocumentM2dMod(PyObject *self, PyObject *args, PyObject *kwd);
	static PyObject* sNewDocumentM3dText(PyObject *self, PyObject *args, PyObject *kwd);
	static PyObject* sNewDocumentM2dText(PyObject *self, PyObject *args, PyObject *kwd);
    static PyObject* sCloseDocument     (PyObject *self,PyObject *args,PyObject *kwd);
    static PyObject* sActiveDocument    (PyObject *self,PyObject *args,PyObject *kwd);
    static PyObject* sSetActiveDocument (PyObject *self,PyObject *args,PyObject *kwd);
    static PyObject* sGetDocument       (PyObject *self,PyObject *args,PyObject *kwd);
    static PyObject* sListDocuments     (PyObject *self,PyObject *args,PyObject *kwd);
    static PyObject* sAddDocObserver    (PyObject *self,PyObject *args,PyObject *kwd);
    static PyObject* sRemoveDocObserver (PyObject *self,PyObject *args,PyObject *kwd);
    static PyObject* sTranslateUnit     (PyObject *self,PyObject *args,PyObject *kwd);
	//fubiao
	static PyObject* sRemoveAllDocObserver(PyObject *self, PyObject *args, PyObject *kwd);

    static PyObject *sSetLogLevel       (PyObject *self,PyObject *args,PyObject *kwd);
    static PyObject *sGetLogLevel       (PyObject *self,PyObject *args,PyObject *kwd);

	//客户端连接
	static PyObject* sClientConnect(PyObject *self, PyObject *args, PyObject *kwd);

	//返回链接是否可用
	static PyObject* sClientIsEnable(PyObject *self, PyObject *args, PyObject *kwd);

	//返回当前的工作目录
	static PyObject* sClientWorkpath(PyObject *self, PyObject *args, PyObject *kwd);

	//返回当前的用户目录
	static PyObject* sClientUserDir(PyObject *self, PyObject *args, PyObject *kwd);

	//返回链接状态
	static PyObject* sClientGetConnectState(PyObject *self, PyObject *args, PyObject *kwd);

	//得到客户端状态
	static PyObject* sClientGetState(PyObject *self, PyObject *args, PyObject *kwd);

	//发送并且运行程序
	static PyObject* sClientSendFile(PyObject *self, PyObject *args, PyObject *kwd);

	//得到远程文件
	static PyObject* sClientShowRemoteFile(PyObject *self, PyObject *args, PyObject *kwd);

	//请求接收某个文件
	static PyObject* sClientRequestReceiveFile(PyObject *self, PyObject *args, PyObject *kwd);

	//发送一个Id消息
	static PyObject* sClientSendIdMsg(PyObject *self, PyObject *args, PyObject *kwd);

	//发送一个登陆消息 @fubiao
	static PyObject* sClientLoginMsg(PyObject *self, PyObject *args, PyObject *kwd);

	//发送一个注册消息
	static PyObject* sClientRegisterMsg(PyObject *self, PyObject *args, PyObject *kwd);
	//发送一个Win消息
	static PyObject* sClientSendWinMsg(PyObject *self, PyObject *args, PyObject *kwd);

	//取出一个消息
	static PyObject* sClientGetMsg(PyObject *self, PyObject *args, PyObject *kwd);
	
	//运行并行计算的文件
	static PyObject* sClientRunFileUseCount(PyObject *self, PyObject *args, PyObject *kwd);

	//获取当前上传/下载百分比
	static PyObject* sClientGetTransmissionRate(PyObject *self, PyObject *args, PyObject *kwd);

	
	//关闭客户端链接
	static PyObject* sClientClose(PyObject *self, PyObject *args, PyObject *kwd);

	//获取服务器Ip
	static PyObject* sClientGetServerIP(PyObject *self, PyObject *args, PyObject *kwd);
	//获取服务器Ip
	static PyObject* sClientSetServerIP(PyObject *self, PyObject *args, PyObject *kwd);
	//获取工作路径
	static PyObject* sClientGetWorkpath(PyObject *self, PyObject *args, PyObject *kwd);
	//设置工作路径
	static PyObject* sClientSetWorkpath(PyObject *self, PyObject *args, PyObject *kwd);
	//设置M3d路径
	static PyObject* sSetM3dpath(PyObject *self, PyObject *args, PyObject *kwd);


	//
	static PyObject* sClientSetUserId(PyObject *self, PyObject *args, PyObject *kwd);
	static PyObject* sClientGetUserId(PyObject *self, PyObject *args, PyObject *kwd);
	static PyObject* sClientSetPassword(PyObject *self, PyObject *args, PyObject *kwd);
	static PyObject* sClientGetPassword(PyObject *self, PyObject *args, PyObject *kwd);
	//获取绘图名称
	static PyObject* sGetFigNameInfoListFromH5File(PyObject *self, PyObject *args, PyObject *kwd);
	//获取绘图数据
	static PyObject* sGetFigDataFromH5File(PyObject *self, PyObject *args, PyObject *kwd);
    static PyMethodDef Methods[]; 

    friend class ApplicationObserver;

    /** @name  Private Init, Destruct an Access methods */
    //@{
    static void initConfig(int argc, char ** argv);
    static void initApplication(void);
    static void logStatus(void);
    // the one and only pointer to the application object
    static Application *_pcSingleton;
    /// argument helper function
    static void ParseOptions(int argc, char ** argv);
    /// checks if the environment is allreight
    //static void CheckEnv(void);
    /// Search for the FreeCAD home path based on argv[0]
    /*!
     * There are multiple implementations of this method per-OS
     */
    static std::string FindHomePath(const char* sCall);
    /// Print the help message
    static void PrintInitHelp(void);
    /// figure out some things
    static void ExtractUserPath();
    /// load the user and system parameter set
    static void LoadParameters(void);
    /// puts the given env variable in the config
    static void SaveEnv(const char *);
    /// startup configuration container
    static std::map<std::string,std::string> mConfig;
    static int _argc;
    static char ** _argv;
    //@}

    struct FileTypeItem {
        std::string filter;
        std::string module;
        std::vector<std::string> types;
    };

    /// open ending information
    std::vector<FileTypeItem> _mImportTypes;
    std::vector<FileTypeItem> _mExportTypes;
    std::map<std::string,Document*> DocMap;
    std::map<std::string,ParameterManager *> mpcPramManager;
    std::map<std::string,std::string> &_mConfig;
    App::Document* _pActiveDoc;

    static Base::ConsoleObserverStd  *_pConsoleObserverStd;
    static Base::ConsoleObserverFile *_pConsoleObserverFile;
};

/// Singleton getter of the Applicaton
inline App::Application &GetApplication(void){
    return *App::Application::_pcSingleton;
}

} // namespace App


#endif // APP_APPLICATION_H

