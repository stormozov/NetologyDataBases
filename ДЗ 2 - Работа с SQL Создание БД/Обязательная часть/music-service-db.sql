CREATE TABLE IF NOT EXISTS genres (
    genre_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL
);

CREATE TABLE IF NOT EXISTS artists (
    artist_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    UNIQUE (name)
);

CREATE TABLE IF NOT EXISTS albums (
    album_id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    release_year INT NOT NULL,
    UNIQUE (title)
);

CREATE TABLE IF NOT EXISTS tracks (
    track_id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    duration INTERVAL NOT NULL,
    album_id INT NOT NULL,
    CONSTRAINT fk_album FOREIGN KEY(album_id) REFERENCES albums(album_id) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS collections (
    collection_id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    release_year INT NOT NULL,
    UNIQUE (title)
);

CREATE TABLE IF NOT EXISTS artist_genres (
    artist_id INT NOT NULL,
    genre_id INT NOT NULL,
    CONSTRAINT fk_artist FOREIGN KEY(artist_id) REFERENCES artists(artist_id) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_genre FOREIGN KEY(genre_id) REFERENCES genres(genre_id) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS album_artists (
    album_id INT NOT NULL,
    artist_id INT NOT NULL,
    CONSTRAINT fk_album FOREIGN KEY(album_id) REFERENCES albums(album_id) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_artist FOREIGN KEY(artist_id) REFERENCES artists(artist_id) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS collection_tracks (
    collection_id INT NOT NULL,
    track_id INT NOT NULL,
    CONSTRAINT fk_collection FOREIGN KEY(collection_id) REFERENCES collections(collection_id) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_track FOREIGN KEY(track_id) REFERENCES tracks(track_id) ON DELETE CASCADE ON UPDATE CASCADE
);
