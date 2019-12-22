DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS post;
DROP TABLE IF EXISTS pages;


CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL
);

CREATE TABLE post (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  author_id INTEGER NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  title TEXT NOT NULL,
  body TEXT NOT NULL,
  FOREIGN KEY (author_id) REFERENCES user (id)
);

create table nav_menu(
    nav_id int auto_increment,
    title VARCHAR(50) unique,
    PRIMARY KEY(id)
);

SELECT * FROM nav_menu
ORDER BY title ASC;

CREATE TABLE pages(
  page_id int AUTO_INCREMENT,
  nav_id int not NULL,
  title varchar(100) NOT NULL UNIQUE,
  slug VARCHAR(50),
  imagUrl varchar(255),
  created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (page_id),
  FOREIGN KEY (nav_id) 
      REFERENCES nav_menu(nav_id)
      ON UPDATE RESTRICT
)

SELECT * FROM pages;

ALTER TABLE pages
CHANGE column imagUrl image_url varchar(255);

SELECT 
  p.page_id, 
  n.title nav_menu,
  p.title page_title,
  p.image_url image
FROM pages as p
INNER JOIN nav_menu as n
  ON n.nav_id = p.nav_id
ORDER BY n.title ASC;

SELECT * from pages;


UPDATE pages
SET 
	title = 'changes from trackers',
    nav_id = 30,
    image_url = 'no image now'
WHERE page_id = 20;


SELECT COUNT(*) 
FROM pages
WHERE page_id = 213333