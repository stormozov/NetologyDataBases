-- == ЗАДАНИЕ 4 ==
-- Названия альбомов, в которых присутствуют исполнители более чем одного жанра.
SELECT a.title
FROM albums a
JOIN album_artists aa ON a.album_id = aa.album_id
JOIN artists ar ON aa.artist_id = ar.artist_id
JOIN artist_genres ag ON ar.artist_id = ag.artist_id
GROUP BY a.title, ar.artist_id
HAVING COUNT(DISTINCT ag.genre_id) > 1

-- Наименования треков, которые не входят в сборники.
SELECT t.title
FROM tracks t
LEFT JOIN collection_tracks ct ON t.track_id = ct.track_id
WHERE ct.track_id IS NULL;

-- Исполнитель или исполнители, написавшие самый короткий по продолжительности
-- трек, — теоретически таких треков может быть несколько.
WITH min_duration AS (
	SELECT MIN(t.duration) AS min_dur
	FROM tracks t
)
SELECT a.name
FROM artists a 
JOIN album_artists aa ON a.artist_id = aa.artist_id 
JOIN albums al ON aa.album_id = al.album_id 
JOIN tracks t ON al.album_id = t.album_id 
WHERE t.duration = (SELECT min_dur FROM min_duration);

-- Названия альбомов, содержащих наименьшее количество треков.
WITH album_counts AS (
  SELECT album_id, COUNT(*) AS track_count
  FROM tracks
  GROUP BY album_id
)
SELECT a.title
FROM albums a
JOIN album_counts ac ON a.album_id = ac.album_id
WHERE ac.track_count = (SELECT MIN(track_count) FROM album_counts);