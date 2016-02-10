import logging
import cloudstorage

class Session(object):

    def __init__(self, key):
        self.bucket = "/%s.appspot.com" % key

    def full(self, filename):
        return "%s/%s" % (self.bucket, filename)

    def list_dir(self, dirname):
        return cloudstorage.listbucket (self.full(dirname))

    def get(self, filename):
        dat = ''

        try:
            gcs_file = cloudstorage.open(self.full(filename))
            dat = gcs_file.read()
            gcs_file.close()

        except cloudstorage.NotFoundError:
            pass

        return dat

    def put(self, filename, data):
        gcs_file = cloudstorage.open(self.full(filename), 'w')
        gcs_file.write(data)
        gcs_file.close()

    def trunc(self, filename):
        self.put(filename, '')

    def remove(self, filename):
        try:
            cloudstorage.delete(self.full(filename))
        except cloudstorage.NotFoundError:
            pass
