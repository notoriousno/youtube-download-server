import json
from functools import partial
from uuid import uuid4

from twisted.internet import threads, reactor
from klein import Klein
from six import string_types
from twisted.python import usage
from youtube_dl import YoutubeDL


class Options(usage.Options):
    """
    """

    optParameters = [
        ['host', 'H', '0.0.0.0', 'Host interface'],
        ['port', 'P', 9000, 'Port number', int],
        ['output-dir', 'o', './videos', "Path where videos will be downloaded"]
    ]


class YoutubeResource(object):

    router = Klein()

    def __init__(self, output_dir):
        self.output_dir = output_dir

    @router.route('/download', methods=['post'])
    def download(self, request):
        """
        Download a single Youtube video using the specified URL and
        rename if specified.
        """
        try:
            url = None
            rename = None

            # get the Youtube url
            for arg in request.args.get(b'url', []):
                url = arg.decode('utf-8')
                assert isinstance(url, string_types)
            assert url is not None, 'NO_LINK_PROVIDED'

            # check if the filename should be renamed
            for arg in request.args.get(b'rename', []):
                rename = '{0}.%(ext)s'.format(arg.decode('utf-8'))

            if rename is None:
                # no rename specified so default
                rename = r'%(title)s.%(ext)s'

            # set the final filename including path
            filename = '/'.join([self.output_dir, rename])
        except AssertionError as err:
            # @TODO log execption
            request.setResponseCode(400)
            return json.dumps({'error': str(err)})

        #
        unique_id = uuid4().hex
        promise = threads.deferToThread(
            download_yt_link,
            url = url,
            uid = unique_id,
            filename = filename)


def download_yt_link(url, uid, filename):
    """
    """
    _progress = partial(progress_hook, uid=uid)
    options = {
        'format': '18/best',
        'progress_hooks': [_progress],
        'outtmpl': filename}

    with YoutubeDL(options) as yt:
        yt.extract_info(url)


def progress_hook(status, uid):
    """
    """
    print(uid)
    print(status['status'])
    print(status['total_bytes'])
    print(status['filename'])


def main():
    # cli args
    options = Options()
    options.parseOptions()

    app = YoutubeResource(options['output-dir'])
    app.router.run(options['host'], options['port'])


main()
