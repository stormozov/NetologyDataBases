CREATE TABLE IF NOT EXISTS genres (
    genre_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    UNIQUE (name)
);

CREATE TABLE IF NOT EXISTS artists (
    artist_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    UNIQUE (name)
);

CREATE TABLE IF NOT EXISTS albums (
    album_id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    release_year NUMERIC(4, 0) NOT NULL CHECK (release_year > 1900),
    UNIQUE (title)
);

CREATE TABLE IF NOT EXISTS tracks (
    track_id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    duration INTEGER NOT NULL CHECK(duration > 0),
    album_id INTEGER NOT NULL,
    CONSTRAINT fk_album FOREIGN KEY(album_id) REFERENCES albums(album_id) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS collections (
    collection_id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    release_year NUMERIC(4, 0) NOT NULL CHECK(release_year > 1900),
    UNIQUE (title)
);

CREATE TABLE IF NOT EXISTS artist_genres (
    artist_id INTEGER NOT NULL,
    genre_id INTEGER NOT NULL,
    CONSTRAINT fk_artist FOREIGN KEY(artist_id) REFERENCES artists(artist_id) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_genre FOREIGN KEY(genre_id) REFERENCES genres(genre_id) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS album_artists (
    album_id INTEGER NOT NULL,
    artist_id INTEGER NOT NULL,
    CONSTRAINT fk_album FOREIGN KEY(album_id) REFERENCES albums(album_id) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_artist FOREIGN KEY(artist_id) REFERENCES artists(artist_id) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS collection_tracks (
    collection_id INTEGER NOT NULL,
    track_id INTEGER NOT NULL,
    CONSTRAINT fk_collection FOREIGN KEY(collection_id) REFERENCES collections(collection_id),
    CONSTRAINT fk_track FOREIGN KEY(track_id) REFERENCES tracks(track_id)
);