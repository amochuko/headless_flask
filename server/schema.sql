SELECT * FROM nav_menu;


SELECT title 
FROM nav_menu
WHERE title = 'contact us';


SELECT title
INTO @t
FROM nav_menu
WHERE title = 'contact us';

select @t;

UPDATE nav_menu 
    SET title = 'contact us'
    WHERE title = @title


use headless_101_cms;
describe nav_menu;
drop TABLE nav_menu;


ALTER TABLE nav_menu
CHANGE COLUMN nav_menu_id
nav_id int auto_increment;

DROP COLUMN slug

ADD COLUMN slug VARCHAR(50) DEFAULT NULL; 


DELETE FROM nav_menu;


SELECT id, 
    title
FROM nav_menu
WHERE title ='contact us'


/* pages */


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