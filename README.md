# Simple chatroom program

# Set up React  
0. `cd ~/environment && git clone https://github.com/NJIT-CS490/project2-m1-aaa237 && cd project2-m1-aaa237`    
1. Install your stuff!    
  a) `npm install`    
  b) `pip install flask-socketio`    
  c) `pip install eventlet`    
  d) `npm install -g webpack`    
  e) `npm install --save-dev webpack`    
  f) `npm install socket.io-client --save`    
If you see any error messages, make sure you use `sudo pip` or `sudo npm`. If it says "pip cannot be found", run `which pip` and use `sudo [path to pip from which pip] install`  
  
# Getting PSQL to work with Python  
  
1. Update yum: `sudo yum update`, and enter yes to all prompts    
2. Upgrade pip: `sudo /usr/local/bin/pip install --upgrade pip`  
3. Get psycopg2: `sudo /usr/local/bin/pip install psycopg2-binary`    
4. Get SQLAlchemy: `sudo /usr/local/bin/pip install Flask-SQLAlchemy==2.1`    
  
# Setting up PSQL  
  
1. Install PostGreSQL: `sudo yum install postgresql postgresql-server postgresql-devel postgresql-contrib postgresql-docs`    
    Enter yes to all prompts.    
2. Initialize PSQL database: `sudo service postgresql initdb`    
3. Start PSQL: `sudo service postgresql start`    
4. Make a new superuser: `sudo -u postgres createuser --superuser $USER`    
    If you get an error saying "could not change directory", that's okay! It worked!  
5. Make a new database: `sudo -u postgres createdb $USER`    
        If you get an error saying "could not change directory", that's okay! It worked!  
6. Make sure your user shows up:    
    a) `psql`    
    b) `\du` look for ec2-user as a user    
    c) `\l` look for ec2-user as a database    
7. Make a new user:    
    a) `psql` (if you already quit out of psql)    
    ## REPLACE THE [VALUES] IN THIS COMMAND! Type this with a new (short) unique password.   
    b) I recommend 4-5 characters - it doesn't have to be very secure. Remember this password!  
        `create user [some_username_here] superuser password '[some_unique_new_password_here]';`    
    c) `\q` to quit out of sql    
8. `cd` into `project2-m1-aaa237` and make a new file called `sql.env` and add `DATABASE_URL=postgresql://[your_username_here]:[your_password_here]@localhost/postgres` in it  
9. Replace the [bracketed_values] with the values you put in 7. b)  
  
  
# Enabling read/write from SQLAlchemy  
There's a special file that you need to enable your db admin password to work for:  
1. Open the file in vim: `sudo vim /var/lib/pgsql9/data/pg_hba.conf`
If that doesn't work: `sudo vim $(psql -c "show hba_file;" | grep pg_hba.conf)`  
2. Replace all values of `ident` with `md5` in Vim: `:%s/ident/md5/g`  
3. After changing those lines, run `sudo service postgresql restart`  
4. Ensure that `sql.env` has the username/password of the superuser you created!  
5. Run your code!    
  a) `npm run watch`. If prompted to install webpack-cli, type "yes"    
  b) In a new terminal, `python app.py`    
  c) Preview Running Application (might have to clear your cache by doing a hard refresh)    

# Pushing to Heroku
1. If you want to deploy this app onto Heroku, you must first register for an account at: https://signup.heroku.com/login
2. Install heroku CLI by running `npm install -g heroku`
3. Log-in to heroku: `heroku login -i`
4. Create new heroku app:  `heroku create`
5. Create a DB on heroku: `heroku addons:create heroku-postgresql:hobby-dev`
6. Run `heroku pg:wait`
7. Make sure we are the owner of our DB

    a) `psql`    
    b) `ALTER DATABASE postgres OWNER TO [user_name_from_7b];`  
    c) `\du` Check that you user is listed and has attributes: `Superuser,Create role, Create DB, Replication`
    d) `\l` Check that your database "postgres" has your user listed as the owner
    
    **If you are missing a role, you can add it with `ALTER ROLE [user_name_from_7b] WITH [CREATEROLE\CREATEDB\REPLICATION]`**

8. Push our db to heroku: `PGUSER=[user_name_from_7b] heroku pg:push postgres DATABASE_URL` If this returns "pg_restore errored with 1", that's okay!
  a) If you are getting an error "peer authentication failed for user", try running just`heroku pg:push postgres DATABASE_URL`
  
9. Configure Procfile with command needed to run your app (for this repo it is `web: python app.py`)
10. Configure requirements.txt with all requirements needed to run your app (for this repo it is filled in using `pip freeze > requirements.txt`
11. Finally, push your app up to heroku with `git push heroku master`

12. Navigate to your new heroku site
  ## Make sure the url says https:// and you see a secured connection, otherwise list items may load in reverse


# Questions
I wanted to make it so the scroll stays all the way down, and I seemed to have inadvertantly found a fix. While implementing another feature,
I limited the number of chats saved to 25 (the number probably doesn't matter). Then I noticed the chats were being grabbed from the beginning 
of the DB table, so I told the query to order by id, descending. Then, because the chats are now out of order, in Content.jsx I ran the array 
through Array.reverse() before passing it into the setMessages state hook. Upon testing my code, I noticed that after reaching the limit of messages,
the chat stays scrolled to the bottom. This is probably because the <ul></ul> tag is now a fixed-length, and so the window would not have to scroll any more.
