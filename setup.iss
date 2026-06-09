[Setup]
AppName=GMC-16
AppVersion=1.0
DefaultDirName={pf}\GMC-16
DefaultGroupName=GMC-16
UninstallDisplayIcon={app}\gmc16.exe
Compression=lzma2
SolidCompression=yes
OutputDir=.
OutputBaseFilename=GMC16_Setup

[Files]
Source: "gmc16.exe"; DestDir: "{app}"
Source: "launch.bat"; DestDir: "{app}"
Source: "gui_launcher.py"; DestDir: "{app}"; Flags: ignoreversion
Source: "examples\*.gmc"; DestDir: "{app}\examples"
; Если есть README.md, лицензия и т.д. – добавьте сюда

[Icons]
Name: "{group}\GMC-16 Launcher (batch)"; Filename: "{app}\launch.bat"; IconFilename: "{app}\gmc16.exe"
Name: "{group}\GMC-16 Launcher (GUI)"; Filename: "{app}\gui_launcher.py"; IconFilename: "{app}\gmc16.exe"; Comment: "Требуется Python"
Name: "{group}\Uninstall GMC-16"; Filename: "{uninstallexe}"
Name: "{commondesktop}\GMC-16 Launcher"; Filename: "{app}\launch.bat"; IconFilename: "{app}\gmc16.exe"

[Run]
Filename: "{app}\launch.bat"; Description: "Запустить лаунчер (консольный)"; Flags: postinstall nowait skipifsilent
Filename: "{app}\gui_launcher.py"; Description: "Запустить графический лаунчер (требуется Python)"; Flags: postinstall nowait skipifsilent

[UninstallDelete]
Type: filesandordirs; Name: "{app}\examples"
