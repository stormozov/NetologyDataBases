-- 1. Заполнение таблицы исполнителей (artists)
INSERT INTO artists (artist_id, name) VALUES 
(1, 'Eminem'),
(2, 'MoonByul'),
(3, 'Yezi'),
(4, 'Younha'),
(5, 'Мари Краймбрери');

-- 2. Заполнение таблицы жанров (genres)
INSERT INTO genres (genre_id, name) VALUES 
(1, 'Hip hop'),
(2, 'Pop'),
(5, 'K-pop'),
(4, 'Rap');

-- 3. Заполнение таблицы альбомов (albums)
-- Albums released in 2000
INSERT INTO albums (album_id, title, release_year)
VALUES 
(1, 'The Marshall Mathers', 2000);

-- Albums released in 2002
INSERT INTO albums (album_id, title, release_year)
VALUES 
(8, '8 Mile: Music from and Inspired by the Motion Picture', 2002);

-- Albums released in 2006
INSERT INTO albums (album_id, title, release_year)
VALUES 
(2, 'Eminem Presents: The Re-Up', 2006);

-- Albums released in 2018
INSERT INTO albums (album_id, title, release_year)
VALUES 
(3, 'Переобулась', 2018),
(9, 'Kamikaze', 2018),
(11, 'SELFISH', 2018);

-- Albums released in 2020
INSERT INTO albums (album_id, title, release_year)
VALUES 
(5, 'Dark Side of the Moon', 2020),
(12, 'HOME', 2020);

-- Albums released in 2021
INSERT INTO albums (album_id, title, release_year)
VALUES 
(4, 'Нас узнает весь мир (Part 1)', 2021),
(6, 'End Theory', 2021);

-- Albums released in 2022
INSERT INTO albums (album_id, title, release_year)
VALUES 
(7, 'Acacia', 2022),
(10, '6equence', 2022);

-- Albums released in 2023
INSERT INTO albums (album_id, title, release_year)
VALUES 
(13, 'YOUNHA Studio Live Album \'MINDSET\'', 2023);

-- 4. Заполнение таблицы треков (tracks)
-- Album 1
INSERT INTO tracks (track_id, title, duration, album_id)
VALUES 
(2, 'Kill You', 264, 1),
(24, 'Remember Me?', 228, 1);

-- Album 2
INSERT INTO tracks (track_id, title, duration, album_id)
VALUES 
(1, 'You Don’t Know', 257, 2);

-- Album 3
INSERT INTO tracks (track_id, title, duration, album_id)
VALUES 
(7, 'На тату', 230, 3),
(21, 'Палево', 224, 3),
(22, 'Туси сам', 214, 3);

-- Album 4
INSERT INTO tracks (track_id, title, duration, album_id)
VALUES 
(3, 'Пряталась в ванной', 190, 4),
(15, 'Океан', 208, 4);

-- Album 5
INSERT INTO tracks (track_id, title, duration, album_id)
VALUES 
(4, 'Eclipce', 209, 5),
(17, 'MOON MOVIE', 218, 5);

-- Album 6
INSERT INTO tracks (track_id, title, duration, album_id)
VALUES 
(5, 'Stardust', 210, 6),
(12, 'P.R.R.W.', 194, 6),
(13, 'How U doing', 246, 6);

-- Album 7
INSERT INTO tracks (track_id, title, duration, album_id)
VALUES 
(6, 'ACACIA', 212, 7);

-- Album 8
INSERT INTO tracks (track_id, title, duration, album_id)
VALUES 
(8, 'Lose Yourself', 320, 8);

-- Album 9
INSERT INTO tracks (track_id, title, duration, album_id)
VALUES 
(9, 'Venom', 269, 9),
(23, 'Greatest', 226, 9);

-- Album 10
INSERT INTO tracks (track_id, title, duration, album_id)
VALUES 
(11, 'LUNATIC', 205, 10),
(18, 'G999', 184, 10);

-- Album 11
INSERT INTO tracks (track_id, title, duration, album_id)
VALUES 
(10, 'SELFISH', 193, 11);

-- Album 12
INSERT INTO tracks (track_id, title, duration, album_id)
VALUES 
(14, 'HOME', 196, 12);

-- Album 13
INSERT INTO tracks (track_id, title, duration, album_id)
VALUES 
(16, 'My everyday', 343, 13),
(19, 'See you', 198, 13),
(20, 'Thirtieth Midnight', 222, 13);

-- 5. Заполнение таблицы сборников (collections)
INSERT INTO collections (collection_id, title, release_year)
VALUES (1, 'Rap Fusion', 2018);

INSERT INTO collections (collection_id, title, release_year)
VALUES (2, 'K-Pop Queens', 2020);

INSERT INTO collections (collection_id, title, release_year)
VALUES (3, 'International Flow', 2019);

INSERT INTO collections (collection_id, title, release_year)
VALUES (4, 'Female Power', 2022);

-- 6. Таблица "многие ко многим". Связь между таблицами артистов и жанров
-- Artist 1
INSERT INTO artist_genres (artist_id, genre_id) VALUES 
(1, 1),
(1, 4);

-- Artist 2
INSERT INTO artist_genres (artist_id, genre_id) VALUES 
(2, 5);

-- Artist 3
INSERT INTO artist_genres (artist_id, genre_id) VALUES 
(3, 5);

-- Artist 4
INSERT INTO artist_genres (artist_id, genre_id) VALUES 
(4, 5);

-- Artist 5
INSERT INTO artist_genres (artist_id, genre_id) VALUES 
(5, 2);

-- 7. Таблица "многие ко многим". Связь между таблицами альбомами и артистами
-- Artist 1
INSERT INTO album_artists (album_id, artist_id) VALUES 
(1, 1),
(2, 1),
(8, 1),
(9, 1);

-- Artist 2
INSERT INTO album_artists (album_id, artist_id) VALUES 
(5, 2),
(10, 2),
(11, 2);

-- Artist 3
INSERT INTO album_artists (album_id, artist_id) VALUES 
(7, 3),
(12, 3);

-- Artist 4
INSERT INTO album_artists (album_id, artist_id) VALUES 
(6, 4);

-- Artist 5
INSERT INTO album_artists (album_id, artist_id) VALUES 
(3, 5),
(4, 5);

-- 8. Таблица "многие ко многим". Связь между таблицами коллекций и треками
-- Collection 1
INSERT INTO collection_tracks (collection_id, track_id) VALUES 
(1, 8),
(1, 10),
(1, 6);

-- Collection 2
INSERT INTO collection_tracks (collection_id, track_id) VALUES 
(2, 4),
(2, 14),
(2, 12);

-- Collection 3
INSERT INTO collection_tracks (collection_id, track_id) VALUES 
(3, 9),
(3, 3),
(3, 12);

-- Collection 4
INSERT INTO collection_tracks (collection_id, track_id) VALUES 
(4, 6),
(4, 5),
(4, 15),
(4, 11);