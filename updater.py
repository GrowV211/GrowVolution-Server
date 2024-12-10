
def updater():
    import website

    website.init_app()

    from website.temporary import start_updater
    start_updater()
