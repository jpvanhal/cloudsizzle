<?php include_once("header.php"); ?>
	<ul id="breadcrumb">
		<li><a href="home.php">Home</a> ></li>
		<li><a href="profile.php">Profile</a> ></li>
		<li>Planned courses</li>
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
			<li>
				<span class="tab-left"></span>
				<span class="tab-right"></span>
				<span class="left-border"></span>
				<span class="right-border"></span>
				<span class="bottom-border"></span>
				<a href="friends.php">Friends</a>
			</li>
			<li class="selected">
				<span class="tab-left"></span>
				<span class="tab-right"></span>
				<span class="left-border"></span>
				<span class="right-border"></span>
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
			
			<h1>Username's courses</h1>
			
			<div class="left-col">
				<ul id="courses-sub-menu">
					<li class="selected"><a href="planned_courses.php">Planned courses</a></li>
					<li><a href="registrations.php">Registrations</a></li>
					<li><a href="completed_studies.php">Completed studies</a></li>
					<li><a href="friends_courses.php">Friends' courses</a></li>
				</ul>
			</div>
			
			<div class="right-col">
				<h2>Planned courses</h2>
				
				<table>
					<tr>
						<th>Course code</th>
						<th>Course name</th>
						<th>Credits</th>
						<th>Timing</th>
						<th>Friends</th>
					</tr>
					<tr>
						<td>T-106.5250</td>
						<td>Distributed Systems</td>
						<td>5cr</td>
						<td>
							<select name="id_1">
								<option>Spring 2010</option>
								<option>Autumn 2010</option>
								<option>Spring 2011</option>
								<option>Autumn 2011</option>
							</select>
						</td>
						<td>3</td>
					</tr>
					<tr class="even">
						<td>T-106.5250</td>
						<td>Distributed Systems</td>
						<td>5cr</td>
						<td>
							<select name="id_1">
								<option>Spring 2010</option>
								<option>Autumn 2010</option>
								<option>Spring 2011</option>
								<option>Autumn 2011</option>
							</select>
						</td>
						<td>3</td>
					</tr>
					<tr>
						<td>T-106.5250</td>
						<td>Distributed Systems</td>
						<td>5cr</td>
						<td>
							<select name="id_1">
								<option>Spring 2010</option>
								<option>Autumn 2010</option>
								<option>Spring 2011</option>
								<option>Autumn 2011</option>
							</select>
						</td>
						<td>3</td>
					</tr>
					<tr class="even">
						<td>T-106.5250</td>
						<td>Distributed Systems</td>
						<td>5cr</td>
						<td>
							<select name="id_1">
								<option>Spring 2010</option>
								<option>Autumn 2010</option>
								<option>Spring 2011</option>
								<option>Autumn 2011</option>
							</select>
						</td>
						<td>3</td>
					</tr>
				</table>
				
			</div>
		</div>
	</div> <!-- /profile -->
<?php include_once("footer.php"); ?>