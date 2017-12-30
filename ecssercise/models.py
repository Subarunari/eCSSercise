from orator import DatabaseManager, Model
from orator.orm import has_many, belongs_to


def set_database_config(config):
    db = DatabaseManager(config)
    Model.set_connection_resolver(db)


class User(Model):
    __table__ = 'Users'

    __fillable__ = ['email', 'name']
    __guarded__ = ['service_id', 'service_name']

    @has_many
    def checks(self):
        return Check

    def set_user_data(self, user_profile):
        self.social_id = str(user_profile.id)
        self.social_name = user_profile.data.get('screen_name', user_profile.name)

    def set_token(self, social_token):
        if 'oauth_token' in social_token:
            self.access_token = social_token['oauth_token']
            self.alt_token = social_token['oauth_token_secret']
            self.expires_at = social_token['x_auth_expires']
        else:
            self.token_type = social_token.get('token_type')
            self.access_token = social_token.get('access_token')
            self.alt_token = social_token.get('refresh_token')
            self.expires_at = social_token.get('expires_at')

    @classmethod
    def find_by_social_id(cls, social_id):
        return cls.query().where_social_id(social_id).get().first()


class Check(Model):
    __table__ = 'Checks'
    __timestamps__ = False

    @classmethod
    def find_by_user_id_and_exercise_number(cls, user_id, exercise_number):
        return cls.query().where_user_id(user_id).where_exercise_number(exercise_number).get().first()

    @belongs_to
    def user(self):
        return User
