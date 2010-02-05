<?php include_once("header.php"); ?>
	<ul id="breadcrumb">
		<li><a href="home.php">Home</a> ></li>
		<li><a href="profile.php">Profile</a> ></li>
		<li>Friends</li>
	</ul>

	<div id="profile" class="rounded-corners-tab">
		
		<ul class="tabs">
			<li>
				<span class="tab-left"></span>
				<span class="tab-right"></span>
				<span class="left-border"></span>
				<span class="right-border"></span>
				<span class="bottom-border"></span>
				<a href="profile.php">Profile</a>
			</li>
			<li class="selected">
				<span class="tab-left"></span>
				<span class="tab-right"></span>
				<span class="left-border"></span>
				<span class="right-border"></span>
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
		</ul>
		
		<div class="tab-content">
			<div class="top-right"></div>
			<div class="bottom-left"></div>
			<div class="bottom-right"></div>
			<div class="bottom-border"></div>
			<div class="right-border"></div>
			<div class="left-border"></div>
			
			<h1>Username's friends</h1>
			
			<div id="friends">
				<div class="friend">
					<form method="post" action="#">
						<div>
							<input type="hidden" name="friend_id" value="1" />
							<input type="submit" name="remove" value="Remove" class="button" />
						</div>
					</form>
				
					<a href="#"><img src="images/profile_picture_small.jpg" alt="" /></a>
					<h2><a href="#">mmeikalaine</a></h2>
					<p>3 mutual courses</p>
					<p>2 mutual friends</p>
					
				</div> <!-- /friend -->
				
				<div class="friend">
					<form method="post" action="#">
						<div>
							<input type="hidden" name="friend_id" value="1" />
							<input type="submit" name="remove" value="Remove" class="button" />
						</div>
					</form>
				
					<a href="#"><img src="images/profile_picture_small.jpg" alt="" /></a>
					<h2><a href="#">mmeikalaine</a></h2>
					<p>3 mutual courses</p>
					<p>2 mutual friends</p>
					
				</div> <!-- /friend -->
				
				<div class="friend">
					<form method="post" action="#">
						<div>
							<input type="hidden" name="friend_id" value="1" />
							<input type="submit" name="remove" value="Remove" class="button" />
						</div>
					</form>
				
					<a href="#"><img src="images/profile_picture_small.jpg" alt="" /></a>
					<h2><a href="#">mmeikalaine</a></h2>
					<p>3 mutual courses</p>
					<p>2 mutual friends</p>
					
				</div> <!-- /friend -->
				
				<div class="friend">
					<form method="post" action="#">
						<div>
							<input type="hidden" name="friend_id" value="1" />
							<input type="submit" name="remove" value="Remove" class="button" />
						</div>
					</form>
				
					<a href="#"><img src="images/profile_picture_small.jpg" alt="" /></a>
					<h2><a href="#">mmeikalaine</a></h2>
					<p>3 mutual courses</p>
					<p>2 mutual friends</p>
					
				</div> <!-- /friend -->
				
				<div class="friend">
					<form method="post" action="#">
						<div>
							<input type="hidden" name="friend_id" value="1" />
							<input type="submit" name="remove" value="Remove" class="button" />
						</div>
					</form>
				
					<a href="#"><img src="images/profile_picture_small.jpg" alt="" /></a>
					<h2><a href="#">mmeikalaine</a></h2>
					<p>3 mutual courses</p>
					<p>2 mutual friends</p>
					
				</div> <!-- /friend -->
				
				<div class="friend last">
					<form method="post" action="#">
						<div>
							<input type="hidden" name="friend_id" value="1" />
							<input type="submit" name="remove" value="Remove" class="button" />
						</div>
					</form>
				
					<a href="#"><img src="images/profile_picture_small.jpg" alt="" /></a>
					<h2><a href="#">mmeikalaine</a></h2>
					<p>3 mutual courses</p>
					<p>2 mutual friends</p>
					
				</div> <!-- /friend -->
			</div> <!-- /friends -->
			
		</div>
	</div> <!-- /profile -->
<?php include_once("footer.php"); ?>