import nmslib
import numpy

# create a random matrix to index
if __name__ == '__main__':
    data = numpy.random.randn(100, 10).astype(numpy.float32)

    # initialize a new index, using a HNSW index on Cosine Similarity
    index = nmslib.init(method='hnsw', space='cosinesimil')
    index.addDataPointBatch(data)
    index.createIndex({'post': 2}, print_progress=True)

    # query for the nearest neighbours of the first datapoint
    ids, distances = index.knnQuery(data[0], k=100)
    print(ids)
    print(distances)
    # get all nearest neighbours for all the datapoint
    # using a pool of 4 threads to compute
    neighbours = index.knnQueryBatch(data, k=10, num_threads=4)
flag = False
INDEX = ''


def buildIndex(data):
    index = nmslib.init(method='hnsw', space='cosinesimil')
    index.addDataPointBatch(data)
    index.createIndex({'post': 2}, print_progress=True)
    return index


def getIndex(data):
    global flag
    global INDEX
    if flag == False:
        INDEX = buildIndex(data)
        flag = True
    return INDEX


def getneighbours(query, num, index):
    idx, distances = index.knnQuery(query, k=num)
    return idx, distances


def getAllneighbours(query, num, index):
    return index.knnQueryBatch(query, k=num, num_threads=4)
