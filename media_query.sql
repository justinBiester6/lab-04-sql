SELECT users.name, users.job, posts.title, posts.writing
FROM users JOIN posts
	ON users.user_id = posts.user_id
WHERE users.job = 'delivery driver';
