<?php include_once("header.php"); ?>
	<ul id="breadcrumb">
		<li><a href="home.php">Home</a> ></li>
		<li>Settings</li>
	</ul>
	
	<div id="settings" class="rounded-corners-tab">
		
		<ul class="tabs">
			<li class="selected">
				<span class="tab-left"></span>
				<span class="tab-right"></span>
				<span class="left-border"></span>
				<span class="right-border"></span>
				<a href="general_info.php">General info</a>
			</li>
			<li>
				<span class="tab-left"></span>
				<span class="tab-right"></span>
				<span class="left-border"></span>
				<span class="right-border"></span>
				<span class="bottom-border"></span>
				<a href="privacy.php">Privacy</a>
			</li>
		</ul>
		
		<div class="tab-content">
			<div class="top-right"></div>
			<div class="bottom-left"></div>
			<div class="bottom-right"></div>
			<div class="bottom-border"></div>
			<div class="right-border"></div>
			<div class="left-border"></div>
			
			<h1>Your info</h1>
			
			<form method="post" action="#" enctype="multipart/form-data" id="info">
				<div>
					<label for="first-name">First name</label>
					<input type="text" name="first_name" id="first-name" />
				</div>
				<div>
					<label for="last-name">Last name</label>
					<input type="text" name="last_name" id="last-name" />
				</div>
				<div>
					<label for="email">Email address</label>
					<input type="text" name="email" id="email" />
				</div>
				<div>
					<label for="major">Major</label>
					<input type="text" name="major" id="major" />
				</div>
				<div>
					<label for="minor">Minor</label>
					<input type="text" name="minor" id="minor" />
				</div>
				<div>
					<label for="picture">Profile picture</label>
					<div>
						<img src="images/profile_picture.jpg" alt="" />
						<input type="hidden" name="MAX_FILE_SIZE" value="100000" />
						<input type="file" name="picture" id="picture" value="Browse" />
					</div>
				</div>
				<div>
					<input type="submit" name="submit" value="Save" class="button" />
				</div>
			</form>
		</div>
	</div> <!-- /settings -->
<?php include_once("footer.php"); ?>