-- Количество исполнителей в каждом жанре.
SELECT g.name, COUNT(DISTINCT ag.artist_id) AS num_artists
FROM artist_genres ag
JOIN genres g ON ag.genre_id = g.genre_id
GROUP BY g.name;

-- Количество треков, вошедших в альбомы 2019–2020 годов.
SELECT COUNT(t.track_id) 
FROM tracks t 
JOIN albums a ON t.album_id = a.album_id 
WHERE a.release_year BETWEEN 2019 AND 2020;

-- Средняя продолжительность треков по каждому альбому.
SELECT a.title, AVG(t.duration)
FROM tracks t
JOIN albums a ON t.album_id = a.album_id
GROUP BY a.title;

-- Все исполнители, которые не выпустили альбомы в 2020 году.
SELECT a.name
FROM artists a
LEFT JOIN albums al ON a.artist_id = al.album_id AND al.release_year = 2020
WHERE al.album_id IS NULL;

-- Названия сборников, в которых присутствует конкретный исполнитель
-- (выберите его сами).
SELECT c.title 
FROM collections c
JOIN collection_tracks ct ON c.collection_id = ct.collection_id
JOIN tracks t ON ct.track_id = t.track_id
JOIN albums a ON t.album_id = a.album_id
JOIN album_artists aa ON a.album_id = aa.album_id
JOIN artists ar ON aa.artist_id = ar.artist_id
WHERE ar.name = 'MoonByul';
