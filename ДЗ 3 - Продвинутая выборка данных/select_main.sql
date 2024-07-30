-- == ЗАДАНИЕ 2 ==
-- 1. Вывести название и продолжительность самого длительного трека.
-- Вариант №1
SELECT title, duration
FROM tracks
ORDER BY duration DESC
LIMIT 1

-- Вариант №2
SELECT title, duration FROM tracks
WHERE duration = (SELECT MAX(duration) FROM tracks);

-- 2. Вывести название треков, продолжительность которых не менее 3,5 минут.
SELECT title, duration
FROM tracks AS t
WHERE duration >= 210;

-- 3. Вывести названия сборников, вышедших в период с 2018 по 2020 год включительно.
SELECT title, release_year FROM collections
WHERE release_year BETWEEN 2018 AND 2020;

-- 4. Вывести исполнителей, чьё имя состоит из одного слова.
SELECT name FROM artists
WHERE name NOT LIKE '% %';

-- 5. Вывести название треков, которые содержат слово «мой» или «my».
-- Вариант №1
SELECT title FROM tracks
WHERE title ILIKE 'my %'
    OR title ILIKE '% my'
    OR title ILIKE '% my %'
    OR title ILIKE 'my'
    OR title ILIKE 'мой %'
    OR title ILIKE '% мой'
    OR title ILIKE '% мой %'
    OR title ILIKE 'мой';

-- Вариант №2
SELECT title FROM tracks
WHERE string_to_array(lower(title), ' ') && ARRAY['my', 'мой'];

-- Вариант №3
SELECT title FROM tracks
WHERE title ~* '\y(my|мой)\y';

-- == ЗАДАНИЕ 3 ==
-- 1. Количество исполнителей в каждом жанре.
-- Без сортировки
SELECT g.name, COUNT(DISTINCT ag.artist_id) AS num_artists
FROM artist_genres ag
JOIN genres g ON ag.genre_id = g.genre_id
GROUP BY g.name;

-- С сортировкой
SELECT g.name, COUNT(DISTINCT ag.artist_id) AS num_artists
FROM artist_genres ag
JOIN genres g ON ag.genre_id = g.genre_id
GROUP BY g.name
ORDER BY num_artists DESC;

-- 2. Количество треков, вошедших в альбомы 2019–2020 годов.
SELECT COUNT(t.track_id) 
FROM tracks t 
JOIN albums a ON t.album_id = a.album_id 
WHERE a.release_year BETWEEN 2019 AND 2020;

-- 3. Средняя продолжительность треков по каждому альбому.
SELECT a.title, AVG(t.duration)
FROM tracks t
JOIN albums a ON t.album_id = a.album_id
GROUP BY a.title;

-- 4. Все исполнители, которые не выпустили альбомы в 2020 году.
-- Вариант №1. Доработка для эксперта.
SELECT a.name
FROM artists a
WHERE a.name NOT IN (
    SELECT DISTINCT ar.name
    FROM artists ar
    JOIN album_artists aa ON ar.artist_id = aa.artist_id
    JOIN albums al ON aa.album_id = al.album_id
    WHERE al.release_year = 2020
);

-- Вариант №2. То, как должно выглядеть решение по условию задачи.
SELECT a.name
FROM artists a
WHERE NOT EXISTS (
    SELECT 1 FROM album_artists aa
    JOIN albums al ON aa.album_id = al.album_id
    WHERE a.artist_id = aa.artist_id AND al.release_year = 2020
);

-- 5. Названия сборников, в которых присутствует конкретный исполнитель
-- (выберите его сами).
SELECT c.title 
FROM collections c
JOIN collection_tracks ct ON c.collection_id = ct.collection_id
JOIN tracks t ON ct.track_id = t.track_id
JOIN albums a ON t.album_id = a.album_id
JOIN album_artists aa ON a.album_id = aa.album_id
JOIN artists ar ON aa.artist_id = ar.artist_id
WHERE ar.name = 'MoonByul';
