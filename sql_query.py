
#extract columns from songs table
Select_Songs_Table = "SELECT distinct song_id, title as song_title, artist_id, year, duration FROM songs"

#extract columns from Artists table
Select_Artists_Table = "SELECT distinct artist_id, artist_name, artist_location, artist_latitude, artist_longitude FROM songs"

#extract columns from staging_events table
staging_events_query = "SELECT *, cast(ts/1000 as Timestamp) as timestamp from staging_events where page = 'NextSong'"

#Filter Users Data from staging_events table
Load_users_data = ("""
select user.userId, user.firstName, user.lastName, user.gender, user.level
from staging_events user
inner join (
select userId, max(ts) as ts 
from staging_events 
group by page,userId
) b on user.userId = b.userId and user.ts = b.ts
""")
#Load Date and Time from staging_events
dateandtime_query = ("""
select distinct timestamp as start_time, 
weekofyear(timestamp) as week, 
hour(timestamp) as hour, 
month(timestamp) as month, 
year(timestamp) as year, 
day(timestamp) as day, 
weekday(timestamp) as weekday
from staging_events
""")
#Filtering songplays data
filteredsongplays_query = ("""
select stg.userId, stg.level, stg.timestamp as start_time, stg.sessionId, stg.location, stg.userAgent,year(stg.timestamp) as year, month(stg.timestamp) as month ,s.song_id, s.artist_id
from staging_events as stg 
inner join songs as s on stg.song = s.song_title
""")