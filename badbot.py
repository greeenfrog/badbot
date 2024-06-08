# mode = 'api'
mode = 'driver'

if __name__ == '__main__':
    if mode == 'api':
        import igapi
        igapi.run()
    elif mode == 'driver':
        import igdriver
        igdriver.run()
