<?php include_once("header.php"); ?>
	<ul id="breadcrumb">
		<li><a href="home.php">Home</a> ></li>
		<li><a href="general_info.php">Settings</a> ></li>
		<li>Privacy</li>
	</ul>

	<div id="settings" class="rounded-corners-tab">
		
		<ul class="tabs">
			<li>
				<span class="tab-left"></span>
				<span class="tab-right"></span>
				<span class="left-border"></span>
				<span class="right-border"></span>
				<span class="bottom-border"></span>
				<a href="general_info.php">General info</a>
			</li>
			<li class="selected">
				<span class="tab-left"></span>
				<span class="tab-right"></span>
				<span class="left-border"></span>
				<span class="right-border"></span>
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
			
			<h1>Your privacy settings</h1>
			
			<form method="post" action="#" enctype="multipart/form-data" id="privacy">
				<div>
					<label for="planned-courses">Your planned courses</label>
					<select name="planned_courses" id="planned-courses">
						<option value="" selected="selected">All</option>
						<option value="">Friends</option>
						<option value="">Only me</option>
					</select>
				</div>
				<div>
					<label for="completed-courses">Your completed courses</label>
					<select name="completed_courses" id="completed-courses">
						<option value="">All</option>
						<option value="">Friends</option>
						<option value="" selected="selected">Only me</option>
					</select>
				</div>
				<div>
					<label for="registrations">Your registrations</label>
					<select name="registrations" id="registrations">
						<option value="">All</option>
						<option value="" selected="selected">Friends</option>
						<option value="">Only me</option>
					</select>
				</div>
				<div>
					<label for="profile">Your profile</label>
					<select name="profile" id="profile">
						<option value="">All</option>
						<option value="" selected="selected">Friends</option>
						<option value="">Only me</option>
					</select>
				</div>
				<div>
					<input type="submit" name="submit" value="Save" class="button" />
				</div>
			</form>
		</div>
	</div> <!-- /settings -->
<?php include_once("footer.php"); ?>