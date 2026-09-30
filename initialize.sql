DROP TABLE IF EXISTS posts;
DROP TABLE IF EXISTS users;

CREATE TABLE users (
	user_id INT AUTO_INCREMENT PRIMARY KEY,
	name VARCHAR(50) NOT NULL,
	job VARCHAR(50) NOT NULL,
	age INT NOT NULL
);

CREATE TABLE posts (
	post_id INT AUTO_INCREMENT PRIMARY KEY,
	user_id INT NOT NULL,
	title VARCHAR(100) NOT NULL,
	writing TEXT NOT NULL,
	posted_at DATETIME DEFAULT CURRENT_TIMESTAMP,
	CONSTRAINT post_user_keys FOREIGN KEY (user_id)
        	REFERENCES users(user_id)
        	ON DELETE CASCADE
);

INSERT INTO users (name, job, age) VALUES
('Doug', 'delivery driver', '40'),
('Deacon', 'delivery driver', '39'),
('Carrie', 'legal secretary', '35'),
('Arthur', 'retired', '70'),
('Spence', 'subway worker', '39'),
('Danny', 'delivery driver', '36'),
('Holly', 'dog walker', '32'),
('Richie', 'fire fighter', '43'),
('Ray', 'sports writer', '41'),
('Lou', 'bodybuilder', '50');

INSERT INTO posts (user_id, title, writing) VALUES
(1, 'My eyes', 'are getting weary'),
(2, 'my back', 'is getting tight'),
(3, 'sitting here', 'in traffic'),
(4, 'on the', 'queensborough bridge tonight'),
(5, 'but I dont care', 'because all I'),
(6, 'want to do', 'is cash my check'),
(7, 'and drive', 'right home to you'),
(8, 'because baby', 'all my life'),
(9, 'I will', 'be driving'),
(10, 'home', 'to you');
