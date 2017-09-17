import os
import sys
import requests
import json
import ast
import threading
import time
from tqdm import tqdm
# from sh import cat

class pyget:

    # targetURL = 'http://audio.turntablelab.com/realfiles/snoop/snoopdogg-stepyogameup.mp3'
    targetURL = 'http://ipv4.download.thinkbroadband.com/100MB.zip'
    # targetURL = 'http://ipv4.download.thinkbroadband.com/512MB.zip'
    # targetURL = 'http://dl.dlfile.pro/2/Logan.2017.1080p.6CH.mkv'
    # targetURL = 'http://fs.evonetbd.com/Media/Movies/English%20Movies/2017/Guardians%20of%20the%20Galaxy%20Vol.2%20(2017)%20/Guardians.Of.The.Galaxy.Vol..2.2017.1080p.BluRay.x264.mp4'
    # fileName = 'downloadedFile.mp3'
    numWorkers = 20

    def __init__(self):
        print 'Init'
        return

    def print_url(self, r, *args, **kwargs):
        # print r.url
        # print args
        # print kwargs
        return


    def downloadSection(self, partNum='', startPos='', endPos=''):
        total = (int(endPos) - int(startPos))
        # print 'total: %s' % total
        fileName = 'dlfile.part%s' % partNum
        header = {'Range': 'bytes=%s-%s' % (startPos, endPos)}
        data = requests.get(self.targetURL, headers=header, stream=True, verify=False, allow_redirects=True, hooks=dict(response=self.print_url))
        if data.status_code == 206:
            CHUNK_SIZE = 8192
            bytes_read = 0
            with open(fileName, 'wb') as f:
                itrcount=1
                for chunk in tqdm(data.iter_content(CHUNK_SIZE), desc='File %s progress' % partNum, position=int(partNum), total=(total/CHUNK_SIZE), mininterval=0.5):
                    itrcount=itrcount+1
                    f.write(chunk)
        return 0

    def combineSections(self):
        return 0

    def main(self):
        data = requests.head(self.targetURL)
        headerDict = ast.literal_eval(str(data.headers))
        filesize = headerDict['content-length']
        print 'Filesize is %s' % filesize

        startPos = 0
        partSize = int(filesize) / self.numWorkers
        endPos = partSize
        print 'End Position is %s' % endPos

        threads = []

        for i in range(0, self.numWorkers):
            endPos = partSize * (i + 1)
            if (i + 1) == self.numWorkers:      # Is last iteration?
                endPos = filesize
            # print '%i> Start: %s End: %s' % (i, startPos, endPos)
            t = threading.Thread(target=self.downloadSection, args=(i, startPos, endPos))
            t.start()
            threads.append(t)
            startPos = int(endPos) + 1
            # endPos = partSize * (i + 1)

        map(lambda t: t.join(), threads)

        return 0

start = time.time()
retVal = pyget().main()
end = time.time()
print('It took %s seconds' % (end - start))
sys.exit(retVal)
