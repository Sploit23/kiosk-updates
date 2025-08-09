; Script para criar um instalador com Inno Setup
; Para usar este script, você precisa ter o Inno Setup instalado: https://jrsoftware.org/isinfo.php

#define MyAppName "Kiosk de Fotos"
#define MyAppVersion "1.0.0"
#define MyAppPublisher "Sua Empresa"
#define MyAppURL "https://www.seusite.com"
#define MyAppExeName "Kiosk de Fotos.exe"

[Setup]
; Configurações básicas do instalador
AppId={{A1B2C3D4-E5F6-4A5B-8C7D-9E0F1A2B3C4D}}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
DefaultDirName={autopf}\{#MyAppName}
DefaultGroupName={#MyAppName}
LicenseFile=LICENSE.txt
; Descomente a linha abaixo para criar um instalador com senha
;Password=sua_senha_aqui
OutputDir=installer
OutputBaseFilename={#MyAppName}_Setup_v{#MyAppVersion}
SetupIconFile=static\icon.ico
Compression=lzma
SolidCompression=yes
WizardStyle=modern

[Languages]
Name: "portuguese"; MessagesFile: "compiler:Languages\Portuguese.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked
Name: "quicklaunchicon"; Description: "{cm:CreateQuickLaunchIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked; OnlyBelowVersion: 6.1; Check: not IsAdminInstallMode

[Files]
; Adicione aqui os arquivos que serão incluídos no instalador
Source: "dist\{#MyAppExeName}"; DestDir: "{app}"; Flags: ignoreversion
Source: "LICENSE.txt"; DestDir: "{app}"; Flags: ignoreversion
Source: "README.md"; DestDir: "{app}"; Flags: ignoreversion

; Cria diretório para armazenar imagens
Source: "*"; DestDir: "{app}\imagens"; Flags: ignoreversion recursesubdirs createallsubdirs; Permissions: everyone-full

[Icons]
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{group}\{cm:UninstallProgram,{#MyAppName}}"; Filename: "{uninstallexe}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent

[Code]
// Código personalizado para o instalador
function InitializeSetup(): Boolean;
begin
  // Verifica se o aplicativo está em execução e pede para fechá-lo
  if FindWindowByClassName('TApplication') <> 0 then
  begin
    if MsgBox('O aplicativo está em execução. Deseja fechá-lo para continuar com a instalação?', mbConfirmation, MB_YESNO) = IDYES then
    begin
      // Tenta fechar o aplicativo
      if not TerminateProcessByName('{#MyAppExeName}') then
      begin
        MsgBox('Não foi possível fechar o aplicativo. Por favor, feche-o manualmente e tente novamente.', mbError, MB_OK);
        Result := False;
        Exit;
      end;
    end
    else
    begin
      Result := False;
      Exit;
    end;
  end;
  
  Result := True;
end;

// Função para terminar um processo pelo nome
function TerminateProcessByName(ProcessName: String): Boolean;
var
  WMIService: Variant;
  ProcessList: Variant;
  Process: Variant;
  TerminateMethod: Variant;
  ReturnValue: Integer;
begin
  Result := False;
  
  try
    WMIService := GetObject('winmgmts:{impersonationLevel=impersonate}!\\.\root\cimv2');
    ProcessList := WMIService.ExecQuery('SELECT * FROM Win32_Process WHERE Name = ''' + ProcessName + '''');
    
    for Process in ProcessList do
    begin
      TerminateMethod := Process.Methods_('Terminate');
      ReturnValue := Process.Terminate(0);
      Result := True;
    end;
  except
    // Ignora erros
  end;
end;

// Código para criar um arquivo de configuração personalizado durante a instalação
procedure CurStepChanged(CurStep: TSetupStep);
var
  SettingsFile: String;
  SettingsContent: String;
begin
  if CurStep = ssPostInstall then
  begin
    // Cria um arquivo de configuração personalizado
    SettingsFile := ExpandConstant('{app}\settings.json');
    SettingsContent := '{
  "server": {
    "host": "0.0.0.0",
    "port": 5000,
    "debug": false
  },
  "images": {
    "base_path": "imagens",
    "allowed_extensions": [".jpg", ".jpeg", ".png"]
  }
}';
    
    SaveStringToFile(SettingsFile, SettingsContent, False);
  end;
end;