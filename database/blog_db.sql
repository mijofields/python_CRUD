DROP DATABASE IF EXISTS python_blog_db;
CREATE DATABASE python_blog_db;
USE python_blog_db;

CREATE TABLE users(
  userid INTEGER(10) AUTO_INCREMENT NOT NULL,
  firstName VARCHAR(25) NOT NULL,
  lastName VARCHAR(25) NOT NULL,
  email VARCHAR(100) UNIQUE NOT NULL,
  password CHAR(100) NOT NULL,
  username VARCHAR(50) UNIQUE NOT NULL ,
  PRIMARY KEY (userid)
);

CREATE TABLE posts(
  postid INTEGER(11) AUTO_INCREMENT NOT NULL,
  title VARCHAR(100) NOT NULL,
  body VARCHAR(1000) NOT NULL,
  author INTEGER (10) NOT NULL REFERENCES users(userid),
  date TIMESTAMP,
  PRIMARY KEY (postid)
);

INSERT INTO users (firstName, lastName, email, password, username) values ('Michael', 'Fields', 'mfields@dtcc.com', 'Password123', 'MikeyF');
INSERT INTO users (firstName, lastName, email, password, username) values ('John', 'Cleese', 'johncleese@montypython.com', 'PeoplesFront', 'JCleese');
INSERT INTO users (firstName, lastName, email, password, username) values ('Michael', 'Palin', 'michaelpalin@montypython.com', 'fishslap', 'MPalin');
INSERT INTO users (firstName, lastName, email, password, username) values ('Graham', 'Chapman', 'grahamchapman@montypython.com', 'NaughtyBoy', 'GrahamC');
INSERT INTO users (firstName, lastName, email, password, username) values ('Terry', 'Gilliam', 'terrygilliamn@montypython.com', 'timebandit', 'TimeBandit1');

INSERT INTO posts (title, body, author) values ("I'm full", "Mr. Creosote is a fictional character who appears in Monty Python's The Meaning of Life. 
He is a monstrously obese restaurant patron who is served a vast amount of food whilst vomiting repeatedly. After being persuaded to eat an after-dinner mint, he explodes in a very graphic way.
The character is played by Terry Jones, who directed the film", 2);
INSERT INTO posts (title, body, author) values ("He's not the messiah, he's a very naughty boy", "Brian Cohen is born in a stable next door to the one in which Jesus is born, which initially confuses the three wise men who come to praise the future King of the Jews. 
Brian grows up an idealistic young man who resents the continuing Roman occupation of Judea. While attending Jesus' Sermon on the Mount, Brian becomes infatuated with an attractive young rebel, Judith. 
His desire for her and hatred for the Romans lead him to join the People's Front of Judea, one of many fractious and bickering independence movements, who spend more time fighting each other than the Romans.
In the morning, Brian, completely naked, opens the curtains to discover an enormous crowd outside his mother's house which proclaims him to be the Messiah. Brian's mother protests, telling the crowd that 'He's not the Messiah, he's a very naughty boy", 4);
INSERT INTO posts (title, body, author) values ("The Holy Grail Horses", "Originally the knight characters were going to ride real horses, but after it became clear that the film's small budget precluded real horses, 
the Pythons decided that their characters would mime horse-riding while their porters trotted behind them banging coconut shells together. 
The joke was derived from the old-fashioned sound effect used by radio shows to convey the sound of hooves clattering. This was later referred to in the German release of the film, which translated the title as Die Ritter der Kokosnuß (The Knights of the Coconut).", 1);
INSERT INTO posts (title, body, author) values ("The Knights Who Say Ni", "The knights demand a sacrifice, and when Arthur states that he merely wishes to pass through the woods, the knights begin shouting 'Ni!', 
forcing the party to shrink back in fear. After this demonstration of their power, the head knight threatens to say 'Ni!' again unless the travelers appease them with a shrubbery; 
otherwise they shall never pass through the wood alive. When Arthur questions the demand, the knights again shout 'Ni!' until the travelers agree to bring them a shrubbery, which the head knight specifies must be 'one that looks nice. And not too expensive.'", 3);
INSERT INTO posts (title, body, author) values ("And now for something completely different", "'The End of the Film' epilogue features the host of 'The Middle of the Film' being handed an envelope containing the meaning of life. 
She reads it out: 'Try and be nice to people, avoid eating fat, read a good book every now and then, get some walking in, and try and live together in peace and harmony with people of all creeds and nations'.", 5);
INSERT INTO posts (title, body, author) values ("You're all individuals!", "Jesus did, sir. I was hopping along, minding my own business, all of a sudden, up he comes, cures me! 
One minute I'm a leper with a trade, next minute my livelihood's gone. Not so much as a by-your-leave! 'You're cured, mate.' Bloody do-gooder.", 1);


SELECT * FROM users;
SELECT * FROM posts;

SELECT posts.title, posts.body, posts.date, posts.postid, users.firstname, users.lastname 
FROM posts 
LEFT JOIN users ON posts.author = users.userid;

SELECT * FROM users WHERE username = %s, [username]


-- show ALL books with authors
-- INNER JOIN will only return all matching values from both tables
SELECT title, firstName, lastName
FROM books
INNER JOIN authors ON books.authorId = authors.id;

-- show ALL books, even if we don't know the author
-- LEFT JOIN returns all of the values from the left table, and the matching ones from the right table
SELECT title, firstName, lastName
FROM books
LEFT JOIN authors ON books.authorId = authors.id;

-- show ALL books, even if we don't know the author
-- RIGHT JOIN returns all of the values from the right table, and the matching ones from the left table
SELECT title, firstName, lastName
FROM books
RIGHT JOIN authors ON books.authorId = authors.id;