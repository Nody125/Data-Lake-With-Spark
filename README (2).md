<html>
<body>

<h2>Project: Data Lake with Spark</h2>
<h4>Introduction</h4>
<p>
In this project, you will learn how to build an ETL pipeline for a data lake hosted on S3. 
by loading data from S3, process the data into analytics tables using Spark, and load them back into S3. 
then deploy this Spark process on a cluster using AWS. finding insights in what songs their users are listening to.
</p>

<p>You'll be able to test your database and ETL pipeline by running queries given to you by the analytics team 
from Sparkify and compare your results with their expected results.</p>

<h3>Process</h3>
<p>I desinged a star schema model to facilitate the processes of queriying the data</p>
<p>I have one Fact table, "songplays" and four more Dimension tables named "users", "songs", "artists" and "time". </p>
<p>Ihave developed a pipeline to transfer all the data from JSON files (which stored in the cloud Amazon S3)
 to the cluster. <p>
<h3>Database Schema</h3>
<p>
<p>Fact Table</p>
<ul>
  <li>songplays : records in event data associated with song plays which is filtered by NextSong </li>
  <ul>
  <li>start_time, userId, level, sessionId, location, userAgent, song_id, artist_id, songplay_id</li>
  </ul>
</ul>  

 <p>Dimension Tables</p>
<ul>
  <li>users : users in app  </li>
  <ul>
  <li>firstName, lastName, gender, level, userId</li>
  </ul>
    <li>songs : Songs in app  </li>
  <ul>
  <li>song_id, title, artist_id, year, duration</li>
  </ul>
     <li>artists : all data about artists  </li>
  <ul>
  <li>artist_id, artist_name, artist_location, artist_lattitude, artist_longitude</li>
  </ul>
    
  <li>time : timestamps of records in songplays </li>
  <ul>
  <li>start_time, day, hour, month, year, weekday</li>
  </ul>
</ul>    
    
</p>
<img src="diagram.PNG" alt="">
    <h2>How to run</h2>   
    <ul>
        <li>Adding AWS Credentials in dl.cfg</li>
        <li>Adding output data path in the main function of etl.py</li>
        <li>Run etl.py</li>

     
</body>
</html>





