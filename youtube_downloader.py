import json
from functools import partial
from uuid import uuid4

from klein import Klein
from six import string_types
from twisted.internet import threads, reactor
from youtube_dl import YoutubeDL


class YoutubeResource(object):

    router = Klein()

    @router.route('/download', methods=['post'])
    def download(self, request):
        """
        """
        try:
            link = None
            for arg in request.args.get(b'link', []):
                try:
                    link = arg.decode('utf-8')
                except:
                    link = None
            assert isinstance(link, string_types)
        except Exception as err:
            # @TODO log execption
            print(err)
            request.setResponseCode(400)
            return json.dumps({'error': 'INVALID_INPUT'})

        #
        unique_id = uuid4().hex
        promise = threads.deferToThread(
            download_yt_link,
            link,
            unique_id)



def download_yt_link(link, uid):
    """
    """
    _progress = partial(progress_hook, uid=uid)
    options = {
        'format': 'bestvideo',
        'progress_hooks': [_progress]}
    with YoutubeDL(options) as yt:
        yt.download([link])


def progress_hook(status, uid):
    """
    """
    print(uid)
    print(status['status'])
    print(status['total_bytes'])
    print(status['filename'])


app = YoutubeResource()
app.router.run('localhost', 9000)
