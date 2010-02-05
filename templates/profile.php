<?php include_once("header.php"); ?>
	<ul id="breadcrumb">
		<li><a href="home.php">Home</a> ></li>
		<li>Profile</li>
	</ul>

	<div id="profile" class="rounded-corners-tab">
		
		<ul class="tabs">
			<li class="selected">
				<span class="tab-left"></span>
				<span class="tab-right"></span>
				<span class="left-border"></span>
				<span class="right-border"></span>
				<a href="profile.php">Profile</a>
			</li>
			<li>
				<span class="tab-left"></span>
				<span class="tab-right"></span>
				<span class="left-border"></span>
				<span class="right-border"></span>
				<span class="bottom-border"></span>
				<a href="friends.php">Friends</a>
			</li>
			<li>
				<span class="tab-left"></span>
				<span class="tab-right"></span>
				<span class="left-border"></span>
				<span class="right-border"></span>
				<span class="bottom-border"></span>
				<a href="planned_courses.php">Courses</a>
			</li>
		</ul> <!-- /tabs -->
		
		<div class="tab-content">
			<div class="top-right"></div>
			<div class="bottom-left"></div>
			<div class="bottom-right"></div>
			<div class="bottom-border"></div>
			<div class="right-border"></div>
			<div class="left-border"></div>
			
			<div class="left-col">
				<h2>Username</h2>
				
				<img src="images/profile_picture.jpg" alt="" />
			</div>
			
			<div class="right-col">
				<h3>Real name</h3>
				<p>Major: Software Engineering</p>
				<p>Minor: Distributed Systems</p>
				
				<div id="personal-news-feed">
					<h3>News feed</h3>
				
					<div class="feed-item">
						<a href="#"><img src="images/profile_picture_small.jpg" alt="" /></a>
						<p><a href="#">Jari</a> enrolled to <a href="#">T-76.5115 Software Development Project II</a></p>
						<p class="date">2 hours ago</p>
					</div> <!-- /feed-item -->
					
					<div class="feed-item">
						<a href="#"><img src="images/profile_picture_small.jpg" alt="" /></a>
						<p><a href="#">Jari</a> enrolled to <a href="#">T-76.5115 Software Development Project II</a></p>
						<p class="date">2 hours ago</p>
					</div> <!-- /feed-item -->
					
					<div class="feed-item">
						<a href="#"><img src="images/profile_picture_small.jpg" alt="" /></a>
						<p><a href="#">Jari</a> enrolled to <a href="#">T-76.5115 Software Development Project II</a></p>
						<p class="date">2 hours ago</p>
					</div> <!-- /feed-item -->
					
					<div class="feed-item last">
						<a href="#"><img src="images/profile_picture_small.jpg" alt="" /></a>
						<p><a href="#">Jari</a> enrolled to <a href="#">T-76.5115 Software Development Project II</a></p>
						<p class="date">2 hours ago</p>
					</div> <!-- /feed-item -->
				</div>
			</div>
		</div>
	</div> <!-- /profile -->
<?php include_once("footer.php"); ?>