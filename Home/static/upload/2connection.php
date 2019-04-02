<?php
try{
	$dbhandler = new PDO('mysql:host=127.0.0.1;dbname=ce164','ce164','$%123456789@');
	echo "Connection is established...<br/>";
	$dbhandler->setAttribute(PDO::ATTR_ERRMODE,PDO::ERRMODE_EXCEPTION); 	
}
catch(PDOException $e){
	echo $e->getMessage();
	die();
}

echo "The rest of our page..."
?>