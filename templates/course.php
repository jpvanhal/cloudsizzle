<?php include_once("header.php"); ?>
	<ul id="breadcrumb">
		<li><a href="home.php">Home</a> ></li>
		<li><a href="courses.php">Courses</a> ></li>
		<li><a href="courses_faculty.php">Faculty of Information and Natural Sciences</a> ></li>
		<li><a href="courses_department.php">Department of Information and Computer Science</a> ></li>
		<li>T-61.5130 Machine Learning and Neural Networks P</li>
	</ul>

	<div id="course" class="rounded-corners">
		<div class="top-left"></div>
		<div class="top-right"></div>
		<div class="bottom-left"></div>
		<div class="bottom-right"></div>
		<div class="bottom-border"></div>
		<div class="left-border"></div>
		<div class="right-border"></div>
		
		<h1>T-61.5130 Machine Learning and Neural Networks P</h1>
		
		<table>
			<tr>
				<th>Credits</th>
				<td>5 cr</td>
			</tr>
			<tr>
				<th>Teaching period</th>
				<td>I - II (Autumn)</td>
			</tr>
			<tr>
				<th>Learning outcomes</th>
				<td>You are aware of how easily fatal, hard to identify and innocent looking bugs creep in to the code of concurrently running programs. You can apply general design principles, models and methods to construct concurrent systems that, in addition to all other requirements, behave correctly with the respect to their functional specifications. You have got an experience of applying the theories using the concurrency features of Java in programming exercises.</td>
			</tr>
			<tr>
				<th>Content</th>
				<td>Principles of concurrent programming, synchronization and
communication mechanism. Concurrent and distributed algorithms,
Concurrent and distributed systems.</td>
			</tr>
			<tr>
				<th>Prerequisites</th>
				<td>Principles of computer architecture, operating system and run-time
system from software perspective. Eg. courses: S-87.3190,
T-106.4155, T-106.3101. Java programming experience.</td>
			</tr>
			<tr>
				<th>Study materials</th>
				<td>M. Ben-Ari: Principles of Concurrent and Distributed Programming, 2nd edition, Addison-Wesley 2006 (Obligatory reading)</td>
			</tr>
		</table>
		
		<div class="options">
			<form method="post" action="#">
				<div>
					<input type="submit" name="submit" value="Plan to take course" class="button" />
				</div>
			</form>
			
			<form method="post" action="#">
				<div>
					<input type="submit" name="submit" value="Enroll to course" class="button" />
				</div>
			</form>
			
			<form method="post" action="recommend_course.php">
				<div>
					<input type="submit" name="submit" value="Recommend course" class="button" />
				</div>
			</form>
		</div>
		
		<h2>Friends taking this course</h2>
		
		<ul id="friend-list">
			<li><a href="#"><img src="images/profile_picture_small.jpg" alt="" />mmeikalaine</a></li>
			<li><a href="#"><img src="images/profile_picture_small.jpg" alt="" />mmeikalaine</a></li>
			<li><a href="#"><img src="images/profile_picture_small.jpg" alt="" />mmeikalaine</a></li>
			<li><a href="#"><img src="images/profile_picture_small.jpg" alt="" />mmeikalaine</a></li>
			<li><a href="#"><img src="images/profile_picture_small.jpg" alt="" />mmeikalaine</a></li>
			<li><a href="#"><img src="images/profile_picture_small.jpg" alt="" />mmeikalaine</a></li>
			<li><a href="#"><img src="images/profile_picture_small.jpg" alt="" />mmeikalaine</a></li>
			<li><a href="#"><img src="images/profile_picture_small.jpg" alt="" />mmeikalaine</a></li>
			<li><a href="#"><img src="images/profile_picture_small.jpg" alt="" />mmeikalaine</a></li>
			<li><a href="#"><img src="images/profile_picture_small.jpg" alt="" />mmeikalaine</a></li>
			<li><a href="#"><img src="images/profile_picture_small.jpg" alt="" />mmeikalaine</a></li>
			<li><a href="#"><img src="images/profile_picture_small.jpg" alt="" />mmeikalaine</a></li>
			<li><a href="#"><img src="images/profile_picture_small.jpg" alt="" />mmeikalaine</a></li>
			<li><a href="#"><img src="images/profile_picture_small.jpg" alt="" />mmeikalaine</a></li>
			<li><a href="#"><img src="images/profile_picture_small.jpg" alt="" />mmeikalaine</a></li>
		</ul> <!-- /friend-list -->
		
	</div> <!-- /course -->
<?php include_once("footer.php"); ?>