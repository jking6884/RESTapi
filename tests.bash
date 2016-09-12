#!/bin/bash





#TESTS
#Tests for authors
protractor  app/templates/authors/conf.js  &&
python app/authors/test_authors.py
#End Tests for authors
#Tests for comments
protractor  app/templates/comments/conf.js  &&
python app/comments/test_comments.py
#End Tests for comments
#Tests for posts
protractor  app/templates/posts/conf.js  &&
python app/posts/test_posts.py
#End Tests for posts
#Tests for posts
protractor  app/templates/posts/conf.js  &&
python app/posts/test_posts.py
#End Tests for posts

