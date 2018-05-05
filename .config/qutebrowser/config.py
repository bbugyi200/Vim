import re
import yaml

import searchengines as SE

# pylint: disable=C0111
c = c  # noqa: F821 pylint: disable=E0602,C0103
config = config  # noqa: F821 pylint: disable=E0602,C0103

# Load autoconfig.yml
config.load_autoconfig()

# construction of bang search pattern for 1-3 letter words and specified longer bangs
excluded_bangs = ['is', 'py']
included_bangs = ['gt[A-z][A-z]+', 'ddg', 'bang', 'giphy']
bang_fmt = '^({}[A-z][A-z]?|({}))%20'
bang_pttrn = bang_fmt.format(''.join(['(?!{})'.format(w) for w in excluded_bangs]),
                             '|'.join(included_bangs))

# ----- Search Engines
c.url.searchengines = {
    'DEFAULT': SE.URL(SE.static.google('{}'),
                      SE.static.duckduckgo('{}'),
                      SE.static.duckduckgo('!{}'),
                      SE.LuckyQuery.url('{}'),
                      patterns=('^%21', bang_pttrn, SE.LuckyQuery.pattern),
                      filters=(None, None, SE.LuckyQuery.filter)),
    'ep': SE.URL(SE.static.google('{} episodes'),
                 SE.static.google('Season {} episodes'),
                 patterns=SE.OneIntQuery.pattern),
    'al': SE.static.google('arch linux {}'),
    'gh': SE.URL(SE.static.google('{} site:github.com'),
                 SE.LuckyQuery.url('{} site:github.com'),
                 'https://github.com/bbugyi200/{}',
                 patterns=(SE.LuckyQuery.pattern, '^%40'),
                 filters=(SE.LuckyQuery.filter, lambda x: x.replace('%40', ''))),
    'ghi': SE.URL('https://github.com/bbugyi200/{}/issues',
                  'https://github.com/bbugyi200/scripts/issues/{}',
                  'https://github.com/bbugyi200/{1}/issues/{0}',
                  SE.LuckyQuery.url('{} site:github.com', end='issues?&q=is%3Aissue+{}'),
                  SE.LuckyQuery.url('{} site:github.com', end='issues'),
                  patterns=('^[0-9]+$',
                            SE.OneIntQuery.pattern,
                            '{}{}'.format(SE.LuckyQuery.pattern, r'([A-z]|%20)+%3F'),
                            SE.LuckyQuery.pattern),
                  filters=(None,
                           SE.OneIntQuery.filter,
                           lambda x: re.split(r'%20%3F', SE.LuckyQuery.filter(x), maxsplit=1),
                           SE.LuckyQuery.filter)),
    'li': SE.static.google('site:linkedin.com {}'),
    'r': SE.URL(SE.static.google('{} site:reddit.com'),
                SE.LuckyQuery.url('{} site:reddit.com'),
                patterns=SE.LuckyQuery.pattern,
                filters=SE.LuckyQuery.filter),
    'waf':'https://waffle.io/bbugyi200/{}',
    'lib':'http://libgen.io/search.php?req={}',
    'pir': SE.URL('https://thepiratebay.org/search/{}',
                  'https://thepiratebay.org/search/{2} S{0:02d}E{1:02d}',
                  patterns=SE.TwoIntQuery.pattern,
                  filters=SE.TwoIntQuery.filter),
    'sub': SE.URL(SE.static.google('{} inurl:english site:subscene.com'),
                  SE.LuckyQuery.url('{0} inurl:english site:subscene.com'),
                  SE.LuckyQuery.url('{2} S{0:02d}E{1:02d} inurl:english site:subscene.com'),
                  patterns=(SE.LuckyQuery.pattern, SE.TwoIntQuery.pattern),
                  filters=(SE.LuckyQuery.filter, SE.TwoIntQuery.filter))
}

# ----- Aliases
c.aliases['mpv'] = 'spawn --userscript view_in_mpv {url}'


# ----- Bindings
def bind(key, *commands, mode='normal'):
    config.bind(key, ' ;; '.join(commands), mode=mode)


def unbind(*args, **kwargs):
    config.unbind(*args, **kwargs)


# >>> INSERT
bind('<Ctrl-i>', 'spawn -d qute-pass-add {url}', mode='insert')
bind('<Ctrl-p>', 'spawn --userscript qute-pass', mode='insert')
bind('<Ctrl-Shift-u>', 'spawn --userscript qute-pass --username-only', mode='insert')
bind('<Ctrl-Shift-p>', 'spawn --userscript qute-pass --password-only', mode='insert')

# >>> PROMPT
bind('<Ctrl-o>', 'prompt-open-download xdg-open {}', mode='prompt')

# >>> COMMAND
bind('<Ctrl-f>', 'edit-command', mode='command')

# >>> NORMAL
# Unbinds
unbound_keys = ['b', 'B', 'd', 'D', 'gd', 'ad', 'co', 'M']
for key in unbound_keys:
    unbind(key)
# Youtube
bind('Y', 'spawn ytcast {url}')
bind(';Y', 'hint links spawn ytcast {hint-url}')
bind('m', 'hint links spawn umpv {hint-url}')
bind('M', 'hint links spawn umpv --append {hint-url}')
# Bookmarks / Quickmarks / Marks
bind('sq', 'quickmark-save')
bind('sb', 'bookmark-add')
bind('dq', 'quickmark-del')
bind('db', 'bookmark-del')
bind('a', ':set-cmd-text -s :quickmark-load')
bind('A', ':set-cmd-text -s :quickmark-load -t')
# <Ctrl-?>
bind('<Ctrl-r>', 'restart')
bind('<Ctrl-t>', 'spawn --userscript taskadd tags:inbox')
bind('<Ctrl-l>', 'edit-url')
# Leader (,)
bind(',e', 'spawn --userscript searchbar-command')
bind(',t', 'config-cycle tabs.position left top')
bind(',rss', 'spawn --userscript openfeeds')
bind(',q', 'set-cmd-text :', 'run-with-count 2 command-history-prev', 'edit-command --run')
# Miscellaneous
bind('b', 'set-cmd-text -s :buffer')
bind('gi', 'hint inputs')
bind('tg', 'set-cmd-text -s :tab-give')
bind('tt', 'set-cmd-text -s :tab-take')
bind('x', 'tab-close')
bind('X', 'tab-close -o')
bind('D', 'download')
bind('dd', 'download-cancel')
bind('to', 'tab-only')
bind('p', 'open -- {clipboard}')
bind('P', 'open -t -- {clipboard}')

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
