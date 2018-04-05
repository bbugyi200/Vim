import re
import yaml

# pylint: disable=C0111
c = c  # noqa: F821 pylint: disable=E0602,C0103
config = config  # noqa: F821 pylint: disable=E0602,C0103

# Load autoconfig.yml
config.load_autoconfig()


class URL(str):
    """ URL for 'url.searchengines' dict

    Allows for additional pattern matching.
    """
    def __new__(cls, value, *args, **kwargs):
        return super(URL, cls).__new__(cls, value)

    def __init__(self, default, others, regexps, filters=None):
        self.default = default
        if isinstance(others, str):
            self.others = (others,)
            self.regexps = (regexps,)
            self.filters = (filters,)
        else:
            self.others = tuple(others)
            self.regexps = tuple(regexps)
            self.filters = filters

        # Allows 'filters' argument to be omitted even when multiple 'others' exist
        if filters is None:
            self.filters = (None,) * len(self.others)

        # Allows 'None' to be given as default filter
        self.filters = tuple(map(lambda x: x if x else lambda y: (y,), self.filters))

    def format(self, term, *args, **kwargs):
        for other, regexp, filter_ in zip(self.others, self.regexps, self.filters):
            if re.match(regexp, term):
                return str.format(other, *filter_(term), *args, **kwargs)

        return str.format(self.default, term, *args, **kwargs)


# ----- Dictionary Values
c.url.searchengines['DEFAULT'] = URL('https://google.com/search?q={}',
                                     'https://duckduckgo.com/?q={}',
                                     '^%21.*')
c.url.searchengines['ep'] = URL('https://google.com/search?q={}+episodes',
                                'https://google.com/search?q=Season+{}+episodes',
                                '^[0-9].*')
c.url.searchengines['ddg'] = 'https://duckduckgo.com/?q={}'
c.url.searchengines['al'] = 'https://google.com/search?q=arch+linux+{}'
c.url.searchengines['gg'] = 'https://google.com/search?q=site%3Agithub.com+{}&ia=web'
c.url.searchengines['ggg'] = 'https://github.com/bbugyi200/{}'
c.url.searchengines['ggi'] = URL('https://github.com/bbugyi200/{}/issues',
                                 'https://github.com/bbugyi200/{1}/issues/{0}',
                                 '^[0-9].*',
                                 filters=lambda x: re.split('\+|%20', x, maxsplit=1))
c.url.searchengines['ggii'] = 'https://github.com/bbugyi200/{}/issues/new'
c.url.searchengines['li'] = 'https://google.com/search?q=site%3Alinkedin.com+{}&ia=web'
c.url.searchengines['py'] = 'https://docs.python.org/2/library/{}'
c.url.searchengines['red'] = 'https://google.com/search?q=site%3Areddit.com+{}&ia=web'
c.url.searchengines['waf'] = 'https://waffle.io/bbugyi200/{}'


# ----- Bindings
def bind(key, *commands, mode='normal'):
    config.bind(key, ' ;; '.join(commands), mode=mode)


# >>> INSERT
bind('<Ctrl-i>', 'spawn -d qute-pass-add {url}', mode='insert')
bind('<Ctrl-p>', 'spawn --userscript qute-pass', mode='insert')
bind('<Ctrl-Shift-u>', 'spawn --userscript qute-pass --username-only', mode='insert')
bind('<Ctrl-Shift-p>', 'spawn --userscript qute-pass --password-only', mode='insert')

# >>> PROMPT
bind('<Ctrl-o>', 'prompt-open-download zathura {}', mode='prompt')

# >>> COMMAND
bind('<Ctrl-f>', 'edit-command', mode='command')

# >>> NORMAL
# Ctrl
bind('<Ctrl-r>', 'restart')
bind('<Ctrl-t>', 'spawn --userscript taskadd tags:inbox')
bind('<Ctrl-l>', 'edit-url')
# Leader (,)
bind(',e', 'scroll-to-perc 0', 'later 25 hint inputs -m number',
     'later 50 spawn xdotool key 0', 'later 100 open-editor')
bind(',t', 'config-cycle tabs.position left top')
bind(',rss', 'spawn --userscript openfeeds')
# Miscellaneous
bind('gi', 'hint inputs')
bind('sb', 'quickmark-save')
bind('C', 'tab-clone', 'back', 'tab-move -')
bind('m', 'enter-mode set_mark')

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
