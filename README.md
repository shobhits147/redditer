Redditer
======

Redditer allows you to stream Posts and Comments matching a configurable set of filters.

It adds user-provided comment to Posts matching a desired pattern and also replies to comments that match the pattern.

## Setup
```shell
git clone https://github.com/shobhits147/redditer.git
cd redditer/
virtualenv -p python3 venv
venv/bin/pip install -r requirements.txt
```

## Usage

1. Create an App in reddit using the instructions mentioned [here](https://github.com/reddit-archive/reddit/wiki/OAuth2-Quick-Start-Example#first-steps)

2. Create a yml file storing the user credentials generated above in the following format:
    ```yaml
    client-id: <your-client-id>
    client-secret: <your-client-secret>
    app-name: <your-app-name>
    username: <your-user-name>
    password: <your-password>
    ```

3. Following is the format of the configuration file used by redditer:
    ```yaml
    keywords:
      - sheldon
      - cooper
    response: Bazinga!!
    credsPath: /Users/shobhits/Documents/redditer/creds.yml
    submissionsFile: /usr/local/share/filtered-submissions.csv
    commentsFile: /usr/local/share/filtered-comments.csv
    ```

4. In `redditer/config.yml` file substitute the path of the file created in Step 2 in the field `credsPath`

5. Modify other fields in config.yml as per your need

6. Start redditer:
    ```shell
    cd redditer/
    venv/bin/python aggregator.py
    ```
    
    
## How it Works

1. Loads configuration from `redditer/config.yml`

2. Loads credentials from the `credsPath` specified in `redditer/config.yml`

3. Resets result files that are specified by the following fields in `redditer/config.yml`:
    1. submissionsFile
    2. commentsFile

4. Creates `redditHelper` object using the configurations provided and `praw` python package.

5. Initializes Aggregator object. Aggregator in turn does the following before returning the object:
    1. Initialize `filters` object - The job of filters is to apply user-provided filters to all posts or comments that the aggregator aggregates.
    2. Initialize `postMan` object - Postman reads the response provided by the user and applies that response to all the filtered out posts and comments.
    3. Initialize `dumper` object - The job of dumper is to dump all the filtered out submissions and comments to files specified by the user in CSV format. Refer to *Results format* section to know more about results structure.
    
6. Spawn two threads:
    1. One thread to stream submissions based on filters provided
    2. One thread to stream comments based on filters provided
    
7. Reddit doesn't allow you to post comments more than once every 5 seconds. So to avoid being blocked by reddit, `Aggregator` polls reddit for new Posts or Comments with a sleep of 10 seconds.

8. For any matching Submission, aggregator adds a comment to that post and dumps the original post's details to `submissionsFile`

9. For any matching Comment, aggregator adds a reply to that comment and dumps the original comment's details to `commentsFile`

## Results format

Submissions file:
```csv
shobhits-mbp:~ shobhits$ tail -f /usr/local/share/filtered-submissions.csv
jh5wb9,shobhit-s,https://www.reddit.com/r/testingground4bots/comments/jh5wb9/new_post_24/
```
Format: `submission-id,submission-author,submission-url`


Comments file:
```csv
shobhits-mbp:~ shobhits$ tail -f /usr/local/share/filtered-comments.csv
g9vr02q,shobhit-s
```
Format: `comment-id,comment-author`


Since we are dumping a CSV, this can be easily loaded into analytics systems and used in Pandas Dataframes.

## How to add custom filter logics

1. To add a new filter to the collected submissions and comments, you need modify `redditer/filters.py`

2. Define your own class of filters, e.g.:
    ```python
    class ComplexLogic
       def __init__(self):
           # initialize some stuffs
           pass
       
       # applyToComment takes comment object as argument and returns the modified comment object
       def applyToComment(self, comment):
           # your fancy logic
           # return comment object if it matches your filter else return None
           pass
    ```
    
3. Call `ComplexLogic's` filters from `applyToComment` method of `Filters` class:
    ```python
    class Filters(BaseFilter):
        def __init__(self, config):
           BaseFilter.__init__(self, config)
           self.complexLogic = ComplexLogic()
    
        def applyToComment(self, object):
           object = self.basicCommentFilters(object)
           if object:
               object = self.complexLogic.applyToComment(object)
           # call other filters if required e.g.:
           # object = SomeNewFilterClass.someNewFilter(object) if object is not None else None
           return object
    ```
4. New filters can be applied to submissions in the same manner

## Let's see it work

1. Let's say I want to respond `Bazinga!!` to any post or comment made to any subreddit I am subscribed to if the post/comment contains keywords `sheldon` and `cooper`

2. Redditer will respond `Bazinga!!` to any post or comment it finds matching the filters specified.

3. The following images should make it a bit clear:
    ###### New post containing required keywords:
    ![New post containing required keywords](https://github.com/shobhits147/redditer/blob/master/images/new_post.png?raw=true)
    
    ###### Comment added by Redditer to matched posts
    ![Comment added by Redditer to matched posts](https://github.com/shobhits147/redditer/blob/master/images/new_post_with_comment.png?raw=true)
    
    ###### New comment containing required keywords
    ![New comment containing required keywords](https://github.com/shobhits147/redditer/blob/master/images/new_comment.png?raw=true)
    
    ###### Reply added by Redditer to matched comments
    ![Reply added by Redditer to matched comments](https://github.com/shobhits147/redditer/blob/master/images/new_comment_with_reply.png?raw=true)
    
    ###### Relevant logs generated by Redditer
    ![Relevant logs generated by Redditer](https://github.com/shobhits147/redditer/blob/master/images/command_line_logs.png?raw=true)