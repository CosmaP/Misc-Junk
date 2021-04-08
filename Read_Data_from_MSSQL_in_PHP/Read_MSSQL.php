
<?php    
$serverName = "192.168.50.232";   
$databaseName = "tempdata";   
$username = "sa";
$password = "Aut0mation!";
     
$connectionInfo = array( "Database"=>$databaseName,"UID" => $username,"PWD" => $password);                          


/* Connect using SQL Server Authentication. */    
$conn = sqlsrv_connect( $serverName, $connectionInfo);    

$tsql = "SELECT id, temp, readingdate FROM tempdata";    

/* Execute the query. */    

$stmt = sqlsrv_query( $conn, $tsql);    

if ( $stmt )    
{    
     echo "Statement executed.<br>\n";    
}     
else     
{    
     echo "Error in statement execution.\n";    
     die( print_r( sqlsrv_errors(), true));    
}    

/* Iterate through the result set printing a row of data upon each iteration.*/    

while( $row = sqlsrv_fetch_array( $stmt, SQLSRV_FETCH_ASSOC))    
{    
     echo "id: " . $row["id"]. " - temp: " . $row["temp"]. " readingdate: " . $row["readingdate"]. "<br>";    
}    

/* Free statement and connection resources. */    
sqlsrv_free_stmt( $stmt);    
sqlsrv_close( $conn);    
?>    