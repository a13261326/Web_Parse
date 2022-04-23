# 1) Написать приложение, которое будет проходиться по указанному списку двух и/или
# более пользователей и собирать данные об их подписчиках и подписках.
# 2) По каждому пользователю, который является подписчиком или на которого подписан исследуемый
# объект нужно извлечь имя, id, фото (остальные данные по
# желанию). Фото можно дополнительно скачать.
# 4) Собранные данные необходимо сложить в базу данных. Структуру данных нужно заранее продумать, чтобы:
# 5) Написать запрос к базе, который вернет список подписчиков только указанного пользователя
# 6) Написать запрос к базе, который вернет список профилей, на кого подписан указанный пользователь

import json
import re
import scrapy
from scrapy.http import HtmlResponse
from instaparser.items import InstaparserItem
from urllib.parse import urlencode
from copy import deepcopy

class InstaSpider(scrapy.Spider):
    name = 'instagram'
    allowed_domains = ['instagram.com']
    start_urls = ['https://www.instagram.com/']
    inst_login_link = 'https://www.instagram.com/accounts/login/ajax/'
    inst_login = 'mamanata1113'
    inst_pwd = '#PWD_INSTAGRAM_BROWSER:10:1650613524:Ac1QAAxZwkH4ALEcKc+FFWZDzJacsMkGewGtQqOxn+fYTv5nSz7uc85UP2Ph9952id0jot6e+QCtyxCkaCX4j/Dyzln5LdOyP2XiKkj/06r3qfXeLL/pCBpnyYHRWUT8KWLE5/1cqgCH45+B4g=='
    parse_users = ['zzagarakiss','calmerlone']
    inst_friendships_link = 'https://i.instagram.com/api/v1/friendships'


    def parse(self, response: HtmlResponse):
        csrf = self.fetch_csrf_token(response.text)
        yield scrapy.FormRequest(
            self.inst_login_link,
            method='POST',
            callback=self.login,
            formdata={'username': self.inst_login, 'enc_password': self.inst_pwd},
            headers={'X-CSRFToken': csrf}
        )

    def login(self, response: HtmlResponse):
        j_body = response.json()
        if j_body.get('authenticated'):
            for user in self.parse_users:
                yield response.follow(
                f'/{self.parse_user}',
                callback=self.user_data_parse,
                cb_kwargs={'username': self.parse_user}
            )
    def user_data_parse(self, response: HtmlResponse, username):
        user_id = self.fetch_user_id(response.text, username)
        variables = {'count': 12}
        url_followers = f'{self.inst_friendships_link}/{user_id}/followers/?{urlencode(variables)}&search_surface=follow_list_page'
        yield response.follow(url_followers,
                              callback=self.user_followers_parse,
                              cb_kwargs={'username': username,
                                         'user_id': user_id,
                                         'variables': deepcopy(variables)},
                              headers={'User-Agent': 'Instagram 155.0.0.37.107'})

        url_followings = f'{self.inst_friendships_link}/{user_id}/followings/?{urlencode(variables)}&search_surface=follow_list_page'
        yield response.follow(url_followings,
                              callback=self.user_followings_parse,
                              cb_kwargs={'username': username,
                                         'user_id': user_id,
                                         'variables': deepcopy(variables)},
                              headers={'User-Agent': 'Instagram 155.0.0.37.107'})



    def user_followers_parse(self, response: HtmlResponse, username, user_id, variables):
        j_data = response.json()
        if j_data.get('next_max_id'):
            variables['max_id'] = j_data.get('next_max_id')
            url_posts = f'{self.inst_friendships_link}/{user_id}/followers/?{urlencode(variables)}&search_surface=follow_list_page'
            yield response.follow(url_posts,
                                  callback=self.user_followers_parse,
                                  cb_kwargs={'username': username,
                                             'user_id': user_id,
                                             'variables': deepcopy(variables)},
                                  headers={'User-Agent': 'Instagram 155.0.0.37.107'})
        followers = j_data.get('users')
        for follower in followers:
            item = InstaparserItem(
                user_id=follower.get('pk'),
                username=follower.get('username'),
                fullname=follower.get('full_name'),
                photo=follower.get('profile_pic_url'),
                all_info=follower.get('Object'))
            yield item

    def user_followings_parse(self, response: HtmlResponse, username, user_id, variables):
        j_data = response.json()
        if j_data.get('next_max_id'):
            variables['max_id'] = j_data.get('next_max_id')
            url_followings = f'{self.inst_friendships_link}/{user_id}/followings/?{urlencode(variables)}&search_surface=follow_list_page'
            yield response.follow(url_followings,
                                  callback=self.user_followings_parse,
                                  cb_kwargs={'username': username,
                                             'user_id': user_id,
                                             'variables': deepcopy(variables)},
                                  headers={'User-Agent': 'Instagram 155.0.0.37.107'})
        followings = j_data.get('users')
        for following in followings:
            item = InstaparserItem(
                user_id=following.get('pk'),
                username=following.get('username'),
                fullname=following.get('full_name'),
                photo=following.get('profile_pic_url'),
                all_info=following.get('Object'))
            yield item



    def fetch_csrf_token(self, text):
        """ Get csrf-token for auth """
        matched = re.search('\"csrf_token\":\"\\w+\"', text).group()
        return matched.split(':').pop().replace(r'"', '')

    def fetch_user_id(self, text, username):
        try:
            matched = re.search(
                '{\"id\":\"\\d+\",\"username\":\"%s\"}' % username, text
            ).group()
            return json.loads(matched).get('id')
        except:
            return re.findall('\"id\":\"\\d+\"', text)[-1].split('"')[-2]













































