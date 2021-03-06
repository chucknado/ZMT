import arrow

from helpers import read_data, write_data, get_settings, package_comment
import api


settings = get_settings()
sync_dates = read_data('sync_dates')
last_sync = arrow.get(sync_dates['comments'])
article_map = read_data('article_map')
comment_map = read_data('comment_map')
comment_article_map = read_data('comment_article_map')

for src_article in article_map:
    dst_article = article_map[src_article]
    print('\nGetting comments in article {}...'.format(src_article))
    url = '{}/{}/articles/{}/comments.json'.format(settings['src_root'], settings['locale'], src_article)
    comments = api.get_resource_list(url)
    if not comments:
        print('- no comments found')
        continue
    for src_comment in comments:
        if src_comment['body'] == '':
            continue
        if last_sync < arrow.get(src_comment['created_at']):
            print('- adding new comment {} to article {}'.format(src_comment['id'], dst_article))
            url = '{}/articles/{}/comments.json'.format(settings['dst_root'], dst_article)
            payload = package_comment(src_comment)
            new_comment = api.post_resource(url, payload)
            if new_comment is False:
                print('Skipping comment {}'.format(src_comment['id']))
                continue
            comment_map[str(src_comment['id'])] = new_comment['id']
            comment_article_map[str(src_comment['id'])] = src_article
            continue
        if last_sync < arrow.get(src_comment['updated_at']):
            print('- updating comment {} in article {}'.format(src_comment['id'], dst_article))
            dst_comment = comment_map[str(src_comment['id'])]
            url = '{}/articles/{}/comments/{}.json'.format(settings['dst_root'], dst_article, dst_comment)
            payload = package_comment(src_comment, put=True)
            response = api.put_resource(url, payload)
            if response is False:
                print('Skipping comment {}'.format(src_comment['id']))
            continue
        print('- comment {} is up to date'.format(src_comment['id']))

utc = arrow.utcnow()
sync_dates['comments'] = utc.format()
write_data(sync_dates, 'sync_dates')
write_data(comment_map, 'comment_map')
write_data(comment_article_map, 'comment_article_map')
