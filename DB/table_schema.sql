CREATE TABLE IF NOT EXISTS User (
	user_id int AUTO_INCREMENT,
    id varchar(100) UNIQUE,
    pw varchar(30),
    PRIMARY KEY (user_id)
);

CREATE TABLE IF NOT EXISTS Article (
	article_id int AUTO_INCREMENT,
    title varchar(100),
    content MEDIUMTEXT,
    area int,
    written_date datetime,
    PRIMARY KEY (article_id)
);

CREATE TABLE IF NOT EXISTS view(
	user_id int,
    article_id int,
    view_date datetime,
    PRIMARY KEY (user_id, article_id, view_date),
    FOREIGN KEY (user_id) REFERENCES User(user_id),
    FOREIGN KEY (article_id) REFERENCES Article(article_id)
);

