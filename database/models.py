# database/models.py

CREATE_USERS_TABLE = """
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    email TEXT UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP
)
"""

CREATE_GAME_SCORES_TABLE = """
CREATE TABLE IF NOT EXISTS game_scores (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    game_name TEXT NOT NULL,
    score INTEGER NOT NULL,
    difficulty TEXT,
    time_taken REAL,
    moves_count INTEGER,
    played_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
)
"""

CREATE_USER_STATS_TABLE = """
CREATE TABLE IF NOT EXISTS user_stats (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    game_name TEXT NOT NULL,
    games_played INTEGER DEFAULT 0,
    total_score INTEGER DEFAULT 0,
    best_score INTEGER DEFAULT 0,
    average_score REAL DEFAULT 0,
    FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE,
    UNIQUE(user_id, game_name)
)
"""

INSERT_USER = """
INSERT INTO users (username, password_hash, email)
VALUES (?, ?, ?)
"""

GET_USER_BY_USERNAME = """
SELECT id, username, password_hash, email, created_at, last_login
FROM users
WHERE username = ?
"""

UPDATE_LAST_LOGIN = """
UPDATE users
SET last_login = CURRENT_TIMESTAMP
WHERE id = ?
"""

INSERT_GAME_SCORE = """
INSERT INTO game_scores (user_id, game_name, score, difficulty, time_taken, moves_count)
VALUES (?, ?, ?, ?, ?, ?)
"""

GET_USER_HIGH_SCORES = """
SELECT game_name, MAX(score) as high_score, difficulty
FROM game_scores
WHERE user_id = ?
GROUP BY game_name, difficulty
"""

GET_USER_GAME_STATS = """
SELECT game_name, COUNT(*) as games_played, 
       MAX(score) as best_score, AVG(score) as avg_score
FROM game_scores
WHERE user_id = ?
GROUP BY game_name
"""

UPDATE_USER_STATS = """
INSERT INTO user_stats (user_id, game_name, games_played, total_score, best_score, average_score)
VALUES (?, ?, 1, ?, ?, ?)
ON CONFLICT(user_id, game_name) DO UPDATE SET
    games_played = games_played + 1,
    total_score = total_score + excluded.total_score,
    best_score = MAX(best_score, excluded.best_score),
    average_score = CAST(total_score + excluded.total_score AS REAL) / (games_played + 1)
"""

GET_LEADERBOARD = """
SELECT u.username, gs.score, gs.difficulty, gs.played_at
FROM game_scores gs
JOIN users u ON gs.user_id = u.id
WHERE gs.game_name = ?
ORDER BY gs.score DESC
LIMIT 10
"""