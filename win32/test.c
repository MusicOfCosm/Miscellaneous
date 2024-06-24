// #pragma comment(lib, "User32.lib")
#include <windows.h>
#include "resource.h"

const char* g_szClassName = "myWindowClass";

PIXELFORMATDESCRIPTOR pfd = {
    sizeof(PIXELFORMATDESCRIPTOR),
    1,
    PFD_DRAW_TO_WINDOW | PFD_SUPPORT_OPENGL | PFD_DOUBLEBUFFER,    // Flags
    PFD_TYPE_RGBA,        // The kind of framebuffer. RGBA or palette.
    32,                   // Colordepth of the framebuffer.
    0, 0, 0, 0, 0, 0,
    0,
    0,
    0,
    0, 0, 0, 0,
    24,                   // Number of bits for the depthbuffer
    8,                    // Number of bits for the stencilbuffer
    0,                    // Number of Aux buffers in the framebuffer.
    PFD_MAIN_PLANE,
    0,
    0, 0, 0
};

//Dialog procedure
BOOL CALLBACK AboutDlgProc(HWND hwnd, UINT Message, WPARAM wParam, LPARAM lParam)
{
    switch(Message)
    {
        case WM_INITDIALOG:

        return TRUE;
        case WM_COMMAND:
            switch(LOWORD(wParam))
            {
                case IDOK:
                    EndDialog(hwnd, IDOK);
                break;
                case IDCANCEL:
                    EndDialog(hwnd, IDCANCEL);
                break;
            }
        break;
        default:
            return FALSE;
    }
    return TRUE;
}

// Step 4: the Window Procedure (Brain)
LRESULT CALLBACK WndProc(HWND hwnd, UINT msg, WPARAM wParam, LPARAM lParam) //It is called for every message
{
    switch(msg)
    {
        // case WM_CREATE: //MENU from code instead of rc file
        //     HMENU hMenu, hSubMenu;
        //     HICON hIcon, hIconSm;
        
        //     hMenu = CreateMenu();
        
        //     hSubMenu = CreatePopupMenu();
        //     AppendMenu(hSubMenu, MF_STRING, ID_FILE_EXIT, "&Exit");
        //     AppendMenu(hMenu, MF_STRING | MF_POPUP, (UINT)hSubMenu, "&File");
        
        //     hSubMenu = CreatePopupMenu();
        //     AppendMenu(hSubMenu, MF_STRING, ID_STUFF_GO, "&Go");
        //     AppendMenu(hMenu, MF_STRING | MF_POPUP, (UINT)hSubMenu, "&Stuff");
        
        //     SetMenu(hwnd, hMenu);
        
        //     const char* img = "../../Rosace.ico";
        //     hIcon = LoadImage(NULL, img, IMAGE_ICON, 32, 32, LR_LOADFROMFILE);
        //     if(hIcon)
        //         SendMessage(hwnd, WM_SETICON, ICON_BIG, (LPARAM)hIcon);
        //     else
        //         MessageBox(hwnd, "Could not load large icon!", "Error", MB_OK | MB_ICONERROR);
        
        //     hIconSm = LoadImage(NULL, img, IMAGE_ICON, 16, 16, LR_LOADFROMFILE);
        //     if(hIconSm)
        //         SendMessage(hwnd, WM_SETICON, ICON_SMALL, (LPARAM)hIconSm);
        //     else
        //         MessageBox(hwnd, "Could not load small icon!", "Error", MB_OK | MB_ICONERROR);

        // case WM_LBUTTONDOWN:        //If left click is pressed (R for right, M for middle)
        //     char szFileName[MAX_PATH];
        //     HINSTANCE hInstance = GetModuleHandle(NULL); //returns a handle to the file used to create the calling process if NULL
        //     GetModuleFileName(hInstance, szFileName, MAX_PATH);
        //     MessageBox(hwnd, szFileName, "This program is:", MB_OK | MB_ICONINFORMATION);
        //     break;
            
        // case WM_KEYDOWN:
        //     if (wParam == VK_ESCAPE) {
        //         DestroyWindow(hwnd);
        //         break;
        //     }
        
        case WM_COMMAND: //From the MENU
            switch(LOWORD(wParam)) //low word of wParam, in the case of WM_COMMAND, it contains the control or menu id that sent the message
            {
                case ID_HELP_ABOUT:
                {
                    INT_PTR ret = DialogBox(GetModuleHandle(NULL), 
                        MAKEINTRESOURCE(IDD_ABOUT), hwnd, AboutDlgProc);
                    if(ret == IDOK){
                        MessageBox(hwnd, "Dialog exited with IDOK.", "Notice",
                            MB_OK | MB_ICONINFORMATION);
                    }
                    else if(ret == IDCANCEL){
                        MessageBox(hwnd, "Dialog exited with IDCANCEL.", "Notice",
                            MB_OK | MB_ICONINFORMATION);
                    }
                    else if(ret == -1){
                        MessageBox(hwnd, "Dialog failed!", "Error",
                            MB_OK | MB_ICONINFORMATION);
                    }
                    return DefWindowProc(hwnd, msg, wParam, lParam);
                }
                break;
                case ID_FILE_EXIT:
                    PostMessage(hwnd, WM_CLOSE, 0, 0); //Basically DestroyWindow(hwnd);
                    break;
                case ID_STUFF_GO:
                    MessageBox(hwnd, "There's nowhere to go!", "Going somewhere?", MB_OK | MB_ICONINFORMATION);
                    return DefWindowProc(hwnd, msg, wParam, lParam);
            }
        case WM_CLOSE:              //Pressing close or Alt+F4
            DestroyWindow(hwnd);    //Destroys the current window and its slaves
            break;
        case WM_DESTROY:            //If the window is destoyed
            PostQuitMessage(0);     //Ends the program, and also posts WM_QUIT to the message queue
            break;
        default:
            return DefWindowProc(hwnd, msg, wParam, lParam); //Default window process
    }
    return 0;
}

/**
 * @brief The main program of a window GUI
 * @param hInstance Handle to the programs executable module (the .exe file in memory)
 * @param hPrevInstance Always NULL for Win32 programs.
 * @param lpCmdLine The command line arguments as a single string. NOT including the program name.
 * @param nCmdShow An integer value which may be passed to ShowWindow().
 * @return 
 */
int WINAPI WinMain(HINSTANCE hInstance, HINSTANCE hPrevInstance,
    LPSTR lpCmdLine, int nCmdShow)
{
    SetProcessDpiAwarenessContext(DPI_AWARENESS_CONTEXT_SYSTEM_AWARE); //Setting the DPI to normal
    WNDCLASSEX wc;
    HWND hwnd;
    MSG Msg;

    //Step 1: Registering the Window Class
    /*(UINT) The size of the structure.*/
    wc.cbSize        = sizeof(WNDCLASSEX);
    /*(UINT) Class Styles (CS_*), not to be confused with Window Styles (WS_*) This can usually be set to 0.*/
    wc.style         = 0;
    /*(WNDPROC) Pointer to the window procedure for this window class.*/
    wc.lpfnWndProc   = WndProc;
    /*(int) Amount of extra data allocated for this class in memory. Usually 0.*/
    wc.cbClsExtra    = 0;
    /*(int) Amount of extra data allocated in memory per window of this type. Usually 0.*/
    wc.cbWndExtra    = 0;
    /*(HINSTANCE) Handle to application instance (that we got in the first parameter of WinMain()).*/
    wc.hInstance     = hInstance;
    /*(HICON) Large (usually 32x32) icon shown when the user presses Alt+Tab.*/
    if (IDI_MYICON > 0) wc.hIcon = LoadIcon(GetModuleHandle(NULL), MAKEINTRESOURCE(IDI_MYICON));
    else              wc.hIcon = LoadIcon(NULL, IDI_APPLICATION);
    /*(HCURSOR) Cursor that will be displayed over our window.*/
    wc.hCursor       = LoadCursor(NULL, IDC_ARROW);
    /*(HBRUSH) Background Brush to set the color of our window.*/
    wc.hbrBackground = (HBRUSH)(COLOR_WINDOW+1);
    /*(LPCSTR) Name of a menu resource to use for the windows with this class.*/
    if (IDR_MYMENU > 0) wc.lpszMenuName = MAKEINTRESOURCE(IDR_MYMENU);
    else              wc.lpszMenuName = NULL;
    /*(LPCSTR) Name to identify the class with.*/
    wc.lpszClassName = g_szClassName;
    /*(HICON) Small (usually 16x16) icon to show in the taskbar and in the top left corner of the window.*/
    if (IDI_MYICON > 0) wc.hIconSm = (HICON)LoadImage(GetModuleHandle(NULL), MAKEINTRESOURCE(IDI_MYICON), IMAGE_ICON, 16, 16, 0);
    else              wc.hIconSm = LoadIcon(NULL, IDI_APPLICATION);

    if(!RegisterClassEx(&wc)) { //hWnd, lpText, lpCaption, uType
        MessageBox(NULL, "Window Registration Failed!", "Error!",
            MB_ICONEXCLAMATION | MB_OK);
        return 0;
    }

    // Step 2: Creating the Window
    hwnd = CreateWindowEx(
        WS_EX_CLIENTEDGE,                           //Extended Window Style (line 2830 WinUser.h)
        g_szClassName,                              //Use Window Class identified by name
        "The title of my window",                   //Window Name
        WS_OVERLAPPEDWINDOW,                        //Common Window Style (line 2814 WinUser.h)
        CW_USEDEFAULT, CW_USEDEFAULT, CW_USEDEFAULT, CW_USEDEFAULT,     //X, Y, Width, Height in pixels (0,0 is top left)
        NULL, NULL, hInstance, NULL);               //Parent Window handle, Menu handle, Instance handle, Pointer to window creation data

    if (hwnd == NULL) {
        MessageBox(NULL, "Window Creation Failed!", "Error!",
            MB_ICONEXCLAMATION | MB_OK);
        return 0;
    }

    ShowWindow(hwnd, nCmdShow); //Show the window
    UpdateWindow(hwnd);         //Update it

    // Step 3: The Message Loop (Heart)
    while(GetMessage(&Msg, NULL, 0, 0) > 0) //Get a message (event) from the message queue
    {
        TranslateMessage(&Msg);             //Additional processing on keyboard events (such as key presses into letters)
        DispatchMessage(&Msg);              //Send message (event) to its window (master or slave, the system does it itself)
    }
    return (int)Msg.wParam;
}