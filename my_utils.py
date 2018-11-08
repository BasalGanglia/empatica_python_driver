import csv, datetime

class logWriter:
    def __init__(self, filename):
        self.f = open(filename, 'w')
        
    def log_msg(self, msg):
        current_time = str(datetime.datetime.now().timestamp())
        self.f.write(current_time +": " + msg)
        self.f.flush()
        
    def close_it_all(self):
        current_time = str(datetime.datetime.now().timestamp())
        self.f.write(current_time +": " + " the end.")
        self.f.close()
        
    

#class logWriter:
    
    #def __init__(self, filename):
        #self.f = open(filename, 'w')
        
        #self.writer = csv.writer(self.f, dialect='excel')
        #self.writer.writerow("testing")
        
    #def log_msg(self, msg):
        #current_time = str(datetime.datetime.now().timestamp())
        #try:
            #self.writer.writerow(current_time + msg)
            #self.f.flush()
        #except:
            #print("Error!")
            
##            current_time = str(datetime.datetime.now().timestamp())
        
#loggi5 = logWriter("Test5.csv");
#loggi5.log_msg("taas uusi koe")


## Following copy pasted from python.org documentation
## https://docs.python.org/2/library/csv.html
#class UnicodeWriter:
    #"""
    #A CSV writer which will write rows to CSV file "f",
    #which is encoded in the given encoding.
    #"""

    #def __init__(self, f, dialect=csv.excel, encoding="utf-8", **kwds):
        ## Redirect output to a queue
        #self.queue = cStringIO.StringIO()
        #self.writer = csv.writer(self.queue, dialect=dialect, **kwds)
        #self.stream = f
        #self.encoder = codecs.getincrementalencoder(encoding)()

    #def writerow(self, row):
        #self.writer.writerow([s.encode("utf-8") for s in row])
        ## Fetch UTF-8 output from the queue ...
        #data = self.queue.getvalue()
        #data = data.decode("utf-8")
        ## ... and reencode it into the target encoding
        #data = self.encoder.encode(data)
        ## write to the target stream
        #self.stream.write(data)
        ## empty queue
        #self.queue.truncate(0)

    #def writerows(self, rows):
        #for row in rows:
            #self.writerow(row)