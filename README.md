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
    response: bazinga
    credsPath: /Users/shobhits/Documents/redditer/creds.yml
    submissionsFile: /usr/local/share/filtered-submissions.csv
    commentsFile: /usr/local/share/filtered-comments.csv
    ```

4. In `redditer/config.yml` file substitute the path of file created in Step 2 in the field `credsPath`.

5. Modify the other fields of config.yml as per your need.

6. Run:
    ```shell
    cd redditer/
    venv/bin/python main.py
    ```
