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

1. Create an App in reddit using the instructions mentioned here [here](https://github.com/reddit-archive/reddit/wiki/OAuth2-Quick-Start-Example#first-steps)

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

4. In `redditer/config.yml` file substitute the path of the file created in Step 2 in the field `credsPath`.

5. Modify the other fields of config.yml as per your need.

6. Start redditer:
    ```shell
    cd redditer/
    venv/bin/python aggregator.py
    ```
    
    
## How it Works


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
