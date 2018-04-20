## Zendesk KB Migration Tools

The tools migrate knowledge base content from one Zendesk Help Center to another. The migrated content include articles, comments, votes, and subscriptions. It doesn't support migrating community content.

The tools add and update the content incrementally based on the timestamp of the last sync.

### Steps

#### Prep

1. Manually create the categories and sections in the destination KB.
2. Create a section map of section ids from the source KB and their corresponding ids in the destination KB. The sections can be in any category. The map is used for migrating the articles to the correct sections in the destination KB.
3. Create a general "Team" user in Support and make the user an agent. Assign the user id to in the settings.ini file.

	Articles in HC can't be authored by end users. If an author leaves the company, they're demoted to end user in Zendesk. Trying to recreate the article elsewhere with the same author causes an error.

#### Syncing

Run the following scripts in order. You can perform this procedure as many times are needed on any schedule. 

**Note**: Don't sync the subscriptions until after the HC goes live and the content has been synced the final time. Because users are notified when somebody adds an article to a section or adds a comment to an article, syncing the subscriptions before a content sync could be a bad experience for users.

1. Run `sync_articles.py`.
2. Run `sync_comments_articles.py`.
3. Run the following scripts in any order:
    - `sync_votes_articles.py`
    - `sync_votes_comments.py`

#### D-day

1. Run the regular sync scripts one last time.
2. Activate the destination Help Center.
3. Activate redirects to the migrated content. See script.js. Copy the ids in js_redirects.txt to redirect function in theme JS.
4. Run the archive article script.
5. Activate "We've moved" articles.
6. Run the subscription scripts:
    - `sync_subscriptions_sections`
    - `sync_subscriptions_articles`

Don't make any more syncs after the syncing the subscriptions.

#### D-day +30 days

- Deactivate the source categories and sections in the source Help Center.

If the old HC is not deactivated, set up redirects in it to the migrated content. See script.js. Copy the ids in js_redirects.txt to redirect function in theme JS.