<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"
   "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
	<title>CloudSizzle</title>
	<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
	<meta http-equiv="imagetoolbar" content="no" />
	<meta name="description" content="CloudSizzle homepage"/>
	<meta name="keywords" content=""/>
	<link rel="stylesheet" type="text/css" media="all" href="css/reset.css" />
	<link rel="stylesheet" type="text/css" media="all" href="css/styles.css" />
</head>
<body id="login-page">
	<div id="wrapper">
		<div id="header">
			<h1><img src="graphics/logo.png" alt="CloudSizzle login" id="logo" /></h1>
			
			<div id="login">
				<form method="post" action="#">
					<div>
						<input type="text" name="username" />
						<input type="password" name="password" />
						<input type="submit" name="submit" value="Login" class="button" />
					</div>
				</form>
			</div> <!-- /login -->
		</div> <!-- /header -->
		
		<div id="content">
		
			<div id="sign-up" class="rounded-corners">
				<div class="top-left"></div>
				<div class="top-right"></div>
				<div class="bottom-left"></div>
				<div class="bottom-right"></div>
				<div class="bottom-border"></div>
				<div class="left-border"></div>
				<div class="right-border"></div>
				
				<h2>Sign up</h2>
				<span>Fields marked with * are mandatory</span>
				
				<form method="post" action="#">
					<div>
						<label for="username">Username*</label>
						<input type="text" name="username" id="username" />
					</div>
					<div>
						<label for="first-name">First name</label>
						<input type="text" name="first_name" id="first-name" />
					</div>
					<div>
						<label for="last-name">Last name</label>
						<input type="text" name="last_name" id="last-name" />
					</div>
					<div>
						<label for="password">Password*</label>
						<input type="text" name="password" id="password" />
					</div>
					<div>
						<label for="confirmed-password">Confirm password*</label>
						<input type="text" name="confirmed_password" id="confirmed-password" />
					</div>
					<div>
						<label for="email">Email*</label>
						<input type="text" name="email" id="email" />
					</div>
					<div class="checkbox">
						<label for="consent">I give my consent to the research study*</label>
						<input type="checkbox" name="consent" id="consent" />
					</div>
					<div>
						<input type="submit" name="submit" value="Sign up" class="button" />
					</div>
				</form>
			</div> <!-- /sign-up -->
			
		</div> <!-- /content -->
	</div><!-- wrapper -->
	
	<div id="footer">
		<p>&copy; CloudSizzle 2010</p>
	</div> <!-- /footer -->
	
</body>
</html>