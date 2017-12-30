import sys
import os

from orator import DatabaseManager
from orator import Schema

sys.path.append(os.getcwd())
from config import development

USER_TABLE_NAME = 'Users'
CHECK_TABLE_NAME = 'Checks'

db = DatabaseManager(development.DATABASE)
schema = Schema(db)

if not schema.has_table(USER_TABLE_NAME):
    with schema.create(USER_TABLE_NAME) as table:
        table.increments('id')
        table.string('email').nullable()
        # Other Service Id. ex:Twitter, Github etc...
        table.string('social_id')
        table.string('social_name')
        table.string('token_type').nullable()
        table.string('access_token')
        table.string('alt_token').nullable()
        table.integer('expires_at').nullable()
        table.timestamps()

        table.unique(['social_name', 'social_id'])


if not schema.has_table(CHECK_TABLE_NAME):
    with schema.create(CHECK_TABLE_NAME) as table:
        table.increments('id')
        table.integer('exercise_number').unsigned()

        table.integer('user_id').unsigned()
        table.foreign('user_id').references('id').on(USER_TABLE_NAME).on_delete('cascade')
