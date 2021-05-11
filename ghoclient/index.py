from whoosh.index import create_in, open_dir
from whoosh.qparser import QueryParser
from whoosh.fields import * 
import os
import copy

schema = Schema(code=ID(stored=True), description=TEXT(stored=True))


class Index:
    def __init__(self, index_path='indexdir'):
        if not os.path.exists(index_path):
            os.mkdir(index_path)
            self.ix = None
        else:
            self.ix = open_dir(index_path)
        
    def build_index(self, codes):
        if self.ix is None:
            self.ix = create_in("indexdir", schema)
            writer = self.ix.writer()
            for row in codes.itertuples():
                writer.add_document(code=row.Label, description=row.Display)
            writer.commit()
            
        
    def search(self, query):
        with self.ix.searcher() as searcher:
            qp = QueryParser("description", schema=self.ix.schema)
            q = qp.parse(query)
            results = searcher.search(q, limit=10000)
            out  = [dict(h) for h in results]
        return out
        
        
