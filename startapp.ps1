Write-Host "Asegurate de"
$flag = Read-Host "Quieres crear los contenedores?? 1: Si, else: No"

$mongo_name = "mongo_"
$cassandra_name = "cassandra_"
$dgraph_name = "dgraph_"

if ($flag -eq 1){
    docker run --name $mongo_name -d -p 27017:27017 mongo
    docker run --name $cassandra_name -d -p 9042:9042 cassandra
    docker run --name $dgraph_name -d -p 8080:8080 -p 9080:9080  dgraph/standalone
}

docker start $cassandra_name
docker start $mongo_name
docker start $dgraph_name

$flag = Read-Host "Quieres parar los contenedores?? 1: Si, else: No"
if ($flag -eq 1){
    docker stop $(docker ps -q)
}