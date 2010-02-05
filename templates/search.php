<?php include_once("header.php"); ?>
	
	<ul id="breadcrumb">
		<li><a href="home.php">Home</a> ></li>
		<li>Search</li>
	</ul>
	
	<div id="advanced-search" class="rounded-corners">
		<div class="top-left"></div>
		<div class="top-right"></div>
		<div class="bottom-left"></div>
		<div class="bottom-right"></div>
		<div class="bottom-border"></div>
		<div class="left-border"></div>
		<div class="right-border"></div>
		
		<h1>Search</h1>
		
		<form method="post" action="#">
			<div>
				<label for="query">Keywords</label>
				<input type="text" name="query" id="query" />
			</div>
			<div>
				<label for="search-option">Search option</label>
				<select name="search_option" id="search-option">
					<option value="">All content</option>
					<option value="">Courses</option>
					<option value="">Users</option>
				</select>
			</div>
			<div>
				<input type="submit" name="search" value="Search" class="button" />
			</div>
		</form>
		
		<h2>Search results</h2>
		
		<p>Results 0-10 of 153 hits for the keyword "T-76.5115"</p>
		
		<ul class="pagination">
			<li><a href="#">&lt; Previous</a></li>
			<li><a href="#">1</a></li>
			<li>&#8230;</li>
			<li><a href="#">4</a></li>
			<li><a href="#">5</a></li>
			<li><a href="#">6</a></li>
			<li class="selected"><a href="#">7</a></li>
			<li><a href="#">8</a></li>
			<li><a href="#">9</a></li>
			<li><a href="#">10</a></li>
			<li>&#8230;</li>
			<li><a href="#">53</a></li>
			<li><a href="#">Next &gt;</a></li>
		</ul>
		
		<div id="search-results">
			<div class="search-result course">
				<p class="type">Course</p>
				<h3><a href="#">T-76.5115 Software Development Project II</a></h3>
			</div>
			
			<div class="search-result user">
				<p class="type">User</p>
				<img src="images/profile_picture_small.jpg" alt="" />
				<h3><a href="#">mmeikalaine</a></h3>
				<p>2 mutual friends</p>
				<p>3 mutual courses</p>
			</div>
			
			<div class="search-result course">
				<p class="type">Course</p>
				<h3><a href="#">T-76.5115 Software Development Project II</a></h3>
			</div>
			
			<div class="search-result user">
				<p class="type">User</p>
				<img src="images/profile_picture_small.jpg" alt="" />
				<h3><a href="#">mmeikalaine</a></h3>
				<p>2 mutual friends</p>
				<p>3 mutual courses</p>
			</div>
			
			<div class="search-result course">
				<p class="type">Course</p>
				<h3><a href="#">T-76.5115 Software Development Project II</a></h3>
			</div>
			
			<div class="search-result user">
				<p class="type">User</p>
				<img src="images/profile_picture_small.jpg" alt="" />
				<h3><a href="#">mmeikalaine</a></h3>
				<p>2 mutual friends</p>
				<p>3 mutual courses</p>
			</div>
			
			<div class="search-result course">
				<p class="type">Course</p>
				<h3><a href="#">T-76.5115 Software Development Project II</a></h3>
			</div>
			
			<div class="search-result user last">
				<p class="type">User</p>
				<img src="images/profile_picture_small.jpg" alt="" />
				<h3><a href="#">mmeikalaine</a></h3>
				<p>2 mutual friends</p>
				<p>3 mutual courses</p>
			</div>
		</div> <!-- /search-results -->
		
		<ul class="pagination">
			<li><a href="#">&lt; Previous</a></li>
			<li><a href="#">1</a></li>
			<li>&#8230;</li>
			<li><a href="#">4</a></li>
			<li><a href="#">5</a></li>
			<li><a href="#">6</a></li>
			<li class="selected"><a href="#">7</a></li>
			<li><a href="#">8</a></li>
			<li><a href="#">9</a></li>
			<li><a href="#">10</a></li>
			<li>&#8230;</li>
			<li><a href="#">53</a></li>
			<li><a href="#">Next &gt;</a></li>
		</ul>
		
		
	</div> <!-- /advanced-search -->
<?php include_once("footer.php"); ?>