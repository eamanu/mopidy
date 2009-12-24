import logging
import re

from mopidy import settings
from mopidy.backends.dummy_backend import DummyBackend

logger = logging.getLogger('handler')

global _request_handlers
_request_handlers = {}

def register(pattern):
    def decorator(func):
        global _request_handlers
        if pattern in _request_handlers:
            raise ValueError(u'Tried to redefine handler for %s with %s' % (
                pattern, func))
        _request_handlers[pattern] = func
        return func
    return decorator

class MpdHandler(object):
    def __init__(self, backend=DummyBackend):
        self.register_backend(backend())

    def handle_request(self, request):
        for pattern in _request_handlers:
            matches = re.match(pattern, request)
            if matches is not None:
                groups = matches.groupdict()
                return _request_handlers[pattern](self, **groups)
        logger.warning(u'Unhandled request: %s', request)
        return False

    def register_backend(self, backend):
        self.backend = backend

    @register(r'^clearerror$')
    def _clearerror(self):
        pass # TODO

    @register(r'^consume (?P<state>[01])$')
    def _consume(self, state):
        state = int(state)
        if state:
            pass # TODO
        else:
            pass # TODO

    @register(r'^crossfade (?P<seconds>\d+)$')
    def _crossfade(self, seconds):
        seconds = int(seconds)
        pass # TODO

    @register(r'^currentsong$')
    def _currentsong(self):
        return self.backend.current_song()

    @register(r'^idle( (?P<subsystems>.+))*$')
    def _idle(self, subsystems=None):
        pass # TODO

    @register(r'^listplaylists$')
    def _listplaylists(self):
        return self.backend.list_playlists()

    @register(r'^lsinfo( "(?P<uri>[^"]*)")*$')
    def _lsinfo(self, uri):
        if uri == u'/':
            return self._listplaylists()
        pass # TODO

    @register(r'^next$')
    def _next(self):
        pass # TODO

    @register(r'^pause (?P<state>[01])$')
    def _pause(self, state):
        pass # TODO

    @register(r'^ping$')
    def _ping(self):
        pass

    @register(r'^play (?P<songpos>.+)$')
    def _play(self, songpos):
        pass # TODO

    @register(r'^playid (?P<songid>.+)$')
    def _playid(self, songid):
        pass # TODO

    @register(r'^previous$')
    def _previous(self):
        pass # TODO

    @register(r'^plchanges (?P<version>\d+)$')
    def _plchanges(self, version):
        return self.backend.playlist_changes(version)

    @register(r'^random (?P<state>[01])$')
    def _random(self, state):
        state = int(state)
        if state:
            pass # TODO
        else:
            pass # TODO

    @register(r'^repeat (?P<state>[01])$')
    def _repeat(self, state):
        state = int(state)
        if state:
            pass # TODO
        else:
            pass # TODO

    @register(r'^replay_gain_mode (?P<mode>(off|track|album))$')
    def _replay_gain_mode(self, mode):
        pass # TODO

    @register(r'^replay_gain_status$')
    def _replay_gain_status(self):
        return u'off'

    @register(r'^seek (?P<songpos>.+) (?P<seconds>\d+)$')
    def _seek(self, songpos, seconds):
        pass # TODO

    @register(r'^seekid (?P<songid>.+) (?P<seconds>\d+)$')
    def _seekid(self, songid, seconds):
        pass # TODO

    @register(r'^setvol (?P<volume>-*\d+)$')
    def _setvol(self, volume):
        volume = int(volume)
        if volume < 0:
            volume = 0
        if volume > 100:
            volume = 100
        pass # TODO

    @register(r'^single (?P<state>[01])$')
    def _single(self, state):
        state = int(state)
        if state:
            pass # TODO
        else:
            pass # TODO

    @register(r'^stats$')
    def _stats(self):
        # TODO
        return {
            'artists': 0,
            'albums': 0,
            'songs': 0,
            'uptime': 0,
            'db_playtime': 0,
            'db_update': 0,
            'playtime': 0,
        }

    @register(r'^stop$')
    def _stop(self):
        pass # TODO

    @register(r'^status$')
    def _status(self):
        return {
            'volume': self.backend.status_volume(),
            'repeat': self.backend.status_repeat(),
            'random': self.backend.status_random(),
            'single': self.backend.status_single(),
            'consume': self.backend.status_consume(),
            'playlist': self.backend.status_playlist(),
            'playlistlength': self.backend.status_playlist_length(),
            'xfade': self.backend.status_xfade(),
            'state': self.backend.status_state(),
        }
