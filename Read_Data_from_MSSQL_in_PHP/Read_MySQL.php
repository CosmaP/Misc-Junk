<?php
$servername = "192.168.0.64";
$username = "pi";
$password = "Aut0mation!";
$dbname = "tempdata";

// Create connection
$conn = new mysqli($servername, $username, $password, $dbname);
// Check connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
} 

$sql = "SELECT id, temp, readingdate FROM tempdata";
$result = $conn->query($sql);

if ($result->num_rows > 0) {
    // output data of each row
    while($row = $result->fetch_assoc()) {
        echo "id: " . $row["id"]. " - temp: " . $row["temp"]. " readingdate: " . $row["readingdate"]. "<br>";
    }
} else {
    echo "0 results";
}
$conn->close();
?>