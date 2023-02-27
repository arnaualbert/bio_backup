# VSCode Debug HowTo
-------------------------------------------------------------------------------

# 1. Create launch.json
- Open a .py file in VSCode
- Open the 'Debug' panel to the left.
- Click 'create .json configuration'
- It will automatically create a .vscode/launch.json file
- This file will enable all the Debug configurations.
  They will appear at the top of the Debug panel, in an foldable list.

# 2. Edit launch.json
- When executing code, VS Code uses the workspace dir as the working directory.
- You can edit launch.json to make it use another dir.
- Example:

        {
            "name": "Launch Rewriter",
            "type": "php",
            "request": "launch",
            "runtimeArgs": [
                "-dxdebug.mode=debug",
                "-dxdebug.start_with_request=yes",
                "-S",
                "localhost:8080",
                "-t",
                "${fileDirname}/../../public",
                "${file}"
            ],
            "program": "",
            "cwd": "${workspaceRoot}",
            "port": 9003,
            "serverReadyAction": {
                "pattern": "Development Server \\(http://localhost:([0-9]+)\\) started",
                "uriFormat": "http://localhost:%s",
                "action": "openExternally"
            }
        }


-------------------------------------------------------------------------------

