Write-Host "Solo debes correr este script 1 vez"
$nombre = Read-Host "Escribe tu nombre"
echo "$nombre cloned this repository at $(Get-Date)" >> clone_logs.txt

$flag = Read-Host "Quieres crear un venv? Escribe SI en caso de tenerlo, cualquier otro input no creara el entorno"
if ($flag -eq "SI"){
    Write-Host "Creando venv..."
    python -m venv venv
}


.\venv\Scripts\Activate.ps1
pip install -r requirements.txt

