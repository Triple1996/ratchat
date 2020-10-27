# Simple chatroom program

# Set up React  
0. `cd ~/environment && git clone https://github.com/NJIT-CS490/project2-m1-aaa237 && cd project2-m1-aaa237`    
1. Install your stuff!    
    a) `npm install`    
    b) `pip install flask-socketio`    
    c) `pip install eventlet`
    d) `pip install rfc3987`
    e) `npm install -g webpack`    
    f) `npm install --save-dev webpack`    
    g) `npm install socket.io-client --save`    
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
# Known Problems
    a) The chat will be delayed until the bot finishes also writing its message out. emit_all_messages is called before 
        the bot code runs, yet it still seems to wait for it to finish before displaying all messages on screen. The only 
        time it is really noticeable is if one of the APIs has a slow connection or is being rate-limited. In these cases, 
        the user's own bot command will not show on screen until the bot terminates its connection to the endpoint.
    
    b) The chat displays the most recent 50 messages. If there are not yet 50 messages on screen, the chat will not 
        stay anchored to the bottom. The cause of this is likely because while there are fewer than 50 messages, the list 
        item grows dynamically, and so the user's position in the scroll bar changes. But once the limit has been reached, 
        the size is static.
    
    c) On very rare cases, chat messages will get inputted at the top or in the middle of the list. This usually only 
        happens when testing locally and the chat is being spammed quickly, and the exact cause is undetermined. Given 
        more time, I would investigate if previous chats from a previous session are somehow ignored.

# Decision on Test
    I chose the test that I did mainly to first, attain as much coverage of my code as possible. That is, I wanted every 
        line (or as close to every line) being run and used by my tests. Once as much coverage as possible was achieved, I then 
        sought to account for edge cases, such as what happens if the user misses a space? For these, I would feed broken input
        into my chatbot handler and expect it to either recognize it and give me the right answer, or reject it outright. Other 
        things I needed to test are all API calls - what happens if I get a KeyError from one of my APIs because the expected 
        string did not get returned? I would handle that by catching the KeyError in a try-catch block.

# Additional Testing
    I unfortunately was not able to reach 100% coverage of my main app.py. This is mostly due to the amount of mocking involved 
    with database and socketio logic. If I had more time, I would definitely have created mock db and mock socket objects to use 
    instead of relying on the actual sql_alchemy calls and socketio calls.
