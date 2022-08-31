CONSUMER_KEY = "cfWZaDt5WfjDJzWRg1VYeUccp"
CONSUMER_PASS = "eAFx4XfqRgl84FrDTn9uoLVnAvcXLMdkapyaGRvsEqWuo1Co4D"
ACCESS_KEY = "1246611248449327104-ovqcuOwNPEYJwdsCJ38JkMeRbiBKGQ"
ACCESS_PASS = "H48amXmZdGUeM3SsYSGTY85h20c3cbxM5MO4nBuFJmuuZ"

class VideoTweet(object):

  def __init__(self, file_name):
    '''
    Defines video tweet properties
    '''
    self.video_filename = file_name
    self.total_bytes = os.path.getsize(self.video_filename)
    self.media_id = None
    self.processing_info = None