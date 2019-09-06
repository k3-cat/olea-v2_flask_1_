Set-Location $PSScriptRoot/..
python -m venv --system-site-packages env
& env/Scripts/Activate.ps1
python -m pip install -U pip setuptools
python -m pip install -U -r requirements.txt
