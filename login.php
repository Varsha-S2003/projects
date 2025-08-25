<?php
session_start();

// Database connection parameters
$servername = "localhost";
$username = "root"; // Default username for WAMP
$password = ""; // Default password for WAMP
$database = "hotel_db";

// Create connection
$conn = new mysqli($servername, $username, $password, $database);

// Check connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

// Check if the form is submitted
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $name = $_POST["name"];
    $email = $_POST["email"];
   $phone=$_POST["phone"];
   $_SESSION['am']=$email;
   $_SESSION['amn']=$name;
    // SQL query to check if the username and password match
    $sql = "SELECT * FROM rege WHERE  email = '$email' AND phone = '$phone'";
    $result = $conn->query($sql);

    if ($result->num_rows == 1) {
        // Login successful
        $_SESSION["name"] = $name;
        header("Location: index.php"); // Redirect to welcome page
        exit();
    } else {
        // Login failed
        $error = "Invalid email or phone number ";
    }
}

?>

<html><head><title>registration from</title>
<style>
    body{
        background-image: url('images/hotel.jpg');
        background-size:cover;
       float:RIGHT;
    }
    form{
        width:65%;
    background-color:black;
        margin:0 auto;
        padding:45px;
        border:7px solid #ccc;
        border-radius:5px;
    }
    input[type="submit"]{
        padding:10px 20px;
        font-size:25px;
        border-radius:10px;
    }
    input[for="a"]{
        padding:10px 20px;
        font-size:16px;
        border-radius:10px;
    }</style>
    </head>
<body style=" color: azure;"> 
</head>
<body style=" color: azure;">
<p style="float:right">admin login:<a href="admin">admin</a></H3><br><p>
    <center>
<br>
<form method="post" STYLE="float:RIGHT;" action="<?php echo htmlspecialchars($_SERVER["PHP_SELF"]); ?>">
<h1 style="color:WHITE;">Login   Now</h1>
<input for="a" type="text" id="name" name="name" placeholder="enter your name" required><br>
        <BR>
        <input for="a" type="Email" id="email" name="email" placeholder="enter your email" required><br>
        <BR>
        <input for="a"  type="phone" id="phone" name="phone" placeholder="enter your phone number" required><br><br><br>
        <input type="submit" value="Confirm" style=" background-color:hsl(0, 91%, 21%);color: azure; "><BR><BR>
        If you didnt register<BR> then go to>>> <a href="register.php">Registration</a></H3><br>
    </form></H2><BR><BR><H3  STYLE="float:RIGHT;"></center>
    <?php if(isset($error)) { echo "<script>alert('$error'); </script>";} ?>
</body>
</html>

<?php
// Close connection
$conn->close();
?>