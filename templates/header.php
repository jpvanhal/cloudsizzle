<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"
   "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
	<title>CloudSizzle</title>
	<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
	<meta http-equiv="imagetoolbar" content="no" />
	<meta name="description" content="CloudSizzle"/>
	<meta name="keywords" content=""/>
	<link rel="stylesheet" type="text/css" media="all" href="css/reset.css" />
	<link rel="stylesheet" type="text/css" media="all" href="css/styles.css" />
</head>
<body id="courses-page">
	<div id="wrapper">
		<div id="header">
			<img src="graphics/logo_small.png" alt="" id="logo" />
			
			<ul class="main-nav">
				<li><a href="home.php">Home</a></li>
				<li><a href="profile.php">Profile</a></li>
				<li><a href="courses.php">Courses</a></li>
			</ul> <!-- /main-nav -->
			
			<ul class="main-nav" id="sub-nav">
				<li><a href="general_info.php">Settings</a></li>
				<li><a href="#">Logout</a></li>
			</ul> <!-- /sub-nav -->
			
			
			<div id="search">
				<form method="post" action="search.php">
					<div>
						<input type="text" name="query" />
						<input type="hidden" name="submit" />
						<input type="image" src="graphics/search_btn.png" name="submit_btn" value="Search" class="search-button" />
					</div>
				</form>
			</div> <!-- /search -->
		</div> <!-- /header -->
		
		<div id="content">