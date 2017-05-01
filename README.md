# Pocket-ReadingTime-Estimation-Visualization
Calculate the amount of time each Pocket Article will take reading by adding a tag like "10 min"

# Dependencies
To run this script you need to install the following packages:
```
pip install pocket-api
pip install pocket-cli
pip install beautifulsoup4
pip install requests
pip install newspaper3k
```
# Usage

 1. Edit the [configurations file](https://github.com/msramalho/Pocket-ReadingTime-Estimation-Visualization/blob/master/configs.json) and add your *consumer_key* ([get it here](https://getpocket.com/developer/apps/new)) and your access_token ([get it here](http://reader.fxneumann.de/plugins/oneclickpocket/auth.php))
 2. Execute the file: `python .\main.py` and watch the progress

# Configurations

- *consumer_key* - API specific key for each deployment, see detailed instrucions [here](https://github.com/rakanalh/pocket-cli#configuration)
- *access_token* - API specific key for each account
- *delete_other_tags* - 1 if you want all other article tags to be removed, 0 if you want to leave them be
- *count_articles_to_tag* - specify how many articles to parse, 0 means all
- *add_tags* - 1 adds the tag "x min" to your articles indicating how many minutes you are expected to take reading them, 0 if you don't want to add the tag (this is usefull if you only want to see the program output)
- *commit_tags_only_at_the_end* - The tag changes (additions and deletions) can be commited for each article or in bulk. 1 means that they will only be committed once every article is parsed, 0 means that each time an article time is calculated its changes are committed (useful if you want to break the execution and have no changes committed until the end)