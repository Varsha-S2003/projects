 <html> 
    <head>
        <title> payment</title><link rel="stylesheet" href="homestyle.css">
    </head>
    <body style="background:black; color:white;">
    <div class="logo">
            <img src="logo.jpeg"width="100px" >
            </div>
          <center>  <h2>Your Booking Information</h2>
          <?php
   session_start();
   echo "<h3>Check in:".$_SESSION['rcin']."<br></h3>";
   echo "<h3 >Check out:".$_SESSION['rcout']."<br></h3>";
   echo "<h3 >number of rooms:".$_SESSION['rmno']."<br></h3>";
   echo "<h3>Total Bill Amount:".$_SESSION['c']*1000*$_SESSION['rmno']."<br></h3>";

    ?>
  <a href="rmbook.php" class="btn">Edit Now</a><br><br><br>
 <form action="card.php" method="post">
 <input type='submit' value="proceed to pay">
 </form>



          <center>

      
</body>
</html>