from collections import ChainMap


default_settings = {
    'ENGINE': 'sqlite://'
}

settings = ChainMap(default_settings)
