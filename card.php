<!DOCTYPE html>
<html lang = "en">
	<head>
		<title>Resort Online Reservation</title>
		<meta charset = "utf-8" />
		<meta name = "viewport" content = "width=device-width, initial-scale=1.0" />
		<link rel = "stylesheet" type = "text/css" href = "css/bootstrap.css " />
		<link rel = "stylesheet" type = "text/css" href = "css/style.css" />
	</head>
<body>
	<nav style = "background-color:rgba(0, 0, 0, 0.1);" class = "navbar navbar-default">
		<div  class = "container-fluid">
			<div class = "navbar-header">
				<a class = "navbar-brand" >Resort Online Reservation</a>
			</div>
		</div>
	</nav>	
<center>
	<div  style = "margin-left:70; width: 500px;" class = "container">
		<div class = "panel panel-default">
			<div class = "panel-body">
				<strong><h3>MAKE A RESERVATION</h3></strong>
				<br />

<h3>Card Payment</h3>

              <form action="payment-done.php">
    
<div class="inputBox">
  <label for="cardname">
    Name On Card:</label>
    <input type="text" id="cardname" placeholder="enter card name" required>
</div>
<br>
    <div class="inputBox">
  <label for="cardnum">
    Card Number:</label>
    <input type="text" id="cardnum" placeholder="1111-2222-3333-4444" maxlength="19" required>
</div>
<br>
<div class="inputBox">
  <label for="">
    Expiring Year:</label>
    <select name="" id="" required>>
      <option value="">choose year</option>
      <option value="2024">2024</option>
      <option value="2025">2025</option>
      <option value="2026">2026</option>
      <option value="2027">2027</option>

</select>
</div>
<br>
<div class="inputBox">
  <label for="cvv">
    CVV:</label>
    <input type="number" id="cvv" placeholder="1234"  required>
</div>
<br>






<input type="submit" value="Pay Now" class = "btn btn-info">

</div></div></div>
<center>
</form>
</body>
</html>