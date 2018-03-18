import yaml

# pylint: disable=C0111
c = c  # noqa: F821 pylint: disable=E0602,C0103
config = config  # noqa: F821 pylint: disable=E0602,C0103

# Load autoconfig.yml
config.load_autoconfig()


# ----- Dictionary Values
c.url.searchengines['DEFAULT'] = 'http://www.google.com/search?q={}'
c.url.searchengines['al'] = 'http://www.google.com/search?q=arch+linux+{}'
c.url.searchengines['gg'] = 'https://www.google.com/search?q=site%3Agithub.com+{}'
c.url.searchengines['ggg'] = 'https://github.com/bbugyi200/{}'
c.url.searchengines['waf'] = 'https://waffle.io/bbugyi200/{}'
c.url.searchengines['li'] = 'https://www.google.com/search?q=site%3Alinkedin.com+{}'
c.url.searchengines['red'] = 'https://www.google.com/search?q=site%3Areddit.com+{}'
c.url.searchengines['a'] = 'https://www.amazon.com/s/ref=nb_sb_noss?url=search-alias%3Daps&field-keywords={}'
c.url.searchengines['w'] = 'https://www.wikipedia.org/w/index.php?title=Special:Search&search={}'
c.url.searchengines['yt'] = 'https://www.youtube.com/results?search_query={}'
c.url.searchengines['img'] = 'https://www.google.com/search?tbm=isch&q={}'
c.url.searchengines['t'] = 'http://www.thesaurus.com/browse/{}'
c.url.searchengines['d'] = 'http://www.dictionary.com/browse/{}'


# ----- Bindings
def bind(key, *commands, mode='normal'):
    config.bind(key, ' ;; '.join(commands), mode=mode)


# qute-pass
bind('<Ctrl-i>', 'spawn -d qute-pass-add {url}', mode='insert')
bind('<Ctrl-p>', 'spawn --userscript qute-pass', mode='insert')
bind('<Ctrl-Alt-u>', 'spawn --userscript qute-pass --username-only', mode='insert')
bind('<Ctrl-Alt-p>', 'spawn --userscript qute-pass --password-only', mode='insert')

# misc
bind('<Ctrl-r>', 'restart')
bind('<Ctrl-t>', 'spawn --userscript taskadd +read')
bind('<Ctrl-l>', 'edit-url')
bind('gi', 'hint inputs')
bind(',e', 'scroll-to-perc 0', 'later 25 hint inputs -m number',
     'later 50 spawn xdotool key 0', 'later 75 open-editor')
bind(',t', 'config-cycle tabs.position left top')
bind(',rss', 'spawn --userscript openfeeds')


# ----- Load Yaml Config
with (config.configdir / 'config.yml').open() as f:
    yaml_data = yaml.load(f)


def dict_attrs(obj, path=''):
    if isinstance(obj, dict):
        for k, v in obj.items():
            yield from dict_attrs(v, '{}.{}'.format(path, k) if path else k)
    else:
        yield path, obj


for k, v in dict_attrs(yaml_data):
    config.set(k, v)