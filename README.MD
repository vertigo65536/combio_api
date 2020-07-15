# Comb.io API

This is a simple python api for using the comb.io website and retrieving a URL for a generated clip

## Functionality

### search(search)
Takes a search query an returns an array of arrays containing [title, url, icon url]

### getDefaultTimestamps(url)
Takes a url returned by search, and returns a dictionary containing the default start and end timestamps decided by comb.io ['ts1': <start timestamp>, 'ts2': <end timestamp>]

### getAllTimestamps(url)
Takes a url returned by search, and returns an array of dictionary containing all possible start and end time stamps that are selectable

### getVideoUrl(url, timestamps)
Takes the url returned by search, and dictionary formatted the same as getDefaultTimestamps returns containing start and end timestamps, and returns a generated video url
