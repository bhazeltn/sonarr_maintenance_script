# bhazeltn's Sonarr Maintenance Script
## _Python Script to manage Sonarr Libraries_

I manage a very large Sonarr library and wanted to automatically unmonitor seasons and series as they are marked fully downloaded. This is for educational purposes.

## Features

- Deleted any series that Sonarr has reported as removed from the TVDb
- Unmonitors any series that has ended and 100% of the episodes have been marked as downloaded by Sonarr
- Unmonitors any season of an ongoing series that has 100% of the eposides marked as downloaded AND has not had an episode air for 365 days
- Remonitors any series that has been unmonitored and is ongoing (i.e. a cancelled show has been renewed)