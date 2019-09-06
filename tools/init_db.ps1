Set-Location $PSScriptRoot/../src
& ../env/Scripts/Activate.ps1
$Env:FLASK_APP = "olea"
$Env:FLASK_ENV = "dev"
flask init-db
