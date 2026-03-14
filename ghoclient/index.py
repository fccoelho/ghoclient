from whoosh.index import create_in, open_dir, exists_in
from whoosh.qparser import QueryParser
from whoosh.fields import *
import os
import copy

schema = Schema(code=ID(stored=True), description=TEXT(stored=True))


class Index:
    def __init__(self, index_path="indexdir"):
        self.index_path = index_path
        if not os.path.exists(index_path):
            os.mkdir(index_path)
            self.ix = None
        elif exists_in(index_path):
            self.ix = open_dir(index_path)
        else:
            self.ix = None

    def build_index(self, codes):
        if self.ix is None:
            self.ix = create_in(self.index_path, schema)
        writer = self.ix.writer()
        for row in codes.itertuples():
            writer.add_document(code=row.Label, description=row.Display)
        writer.commit()

    def search(self, query):
        if self.ix is None:
            return []
        with self.ix.searcher() as searcher:
            qp = QueryParser("description", schema=self.ix.schema)
            q = qp.parse(query)
            results = searcher.search(q, limit=10000)
            out = [dict(h) for h in results]
        return out
