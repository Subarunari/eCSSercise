from ecssercise import views, models


if __name__ == '__main__':
    views.app.config.from_pyfile('config.py')
    views.app.config.from_envvar('ECSSERCISE_CONFIG_PATH')
    models.set_database_config(views.app.config['DATABASE'])

    views.app.run()
