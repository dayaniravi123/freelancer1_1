<?php
try{
	$dbhandler = new PDO('mysql:host=127.0.0.1;dbname=ce164','ce164','$%123456789@');
	echo "Connection is established...<br/>";
	$dbhandler->setAttribute(PDO::ATTR_ERRMODE,PDO::ERRMODE_EXCEPTION);
	$sql="insert into guestbook (name,message,posted) values ('Surya','Good night',now())";
	$query=$dbhandler->query($sql);
	echo "Data is inserted successfully";
	
}
catch(PDOException $e){
	echo $e->getMessage();
	die();
}


?>