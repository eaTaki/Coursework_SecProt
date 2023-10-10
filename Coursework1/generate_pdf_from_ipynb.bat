@echo off

if "%~1"=="" (
    echo Please provide an exercise number as an argument.
    exit /b 1
)

set PATH=%PATH%;C:\Users\etaki\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.10_qbz5n2kfra8p0\LocalCache\local-packages\Python310\Scripts

jupyter nbconvert --to pdf "Coursework1\cw1ex%1\Coursework 1 - Exercise %1.ipynb"
