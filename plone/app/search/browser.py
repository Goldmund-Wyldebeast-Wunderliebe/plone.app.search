from Products.Five.browser import BrowserView
from plone.app.contentlisting.interfaces import IContentListing
from Products.CMFCore.utils import getToolByName
from config import CRITERION

class Search(BrowserView):
    
    def results(self):
        catalog = getToolByName(self.context, 'portal_catalog')
        results = catalog()
        if results:
            return IContentListing(results)
        return []

class AdvancedSearch(BrowserView):
    
    def results(self):
        # parse query
        query = self.parseFormquery(self.request.get('query',None))

        self.query = query
    
        # Get me my stuff!
        catalog = getToolByName(self.context, 'portal_catalog')
        results = catalog(query)
        if results:
            return IContentListing(results)
        return IContentListing([])
        
    def parseFormquery(self, formquery):
        query = {}
        for row in formquery:
            index=row.get('i')
            values=row.get('v')
            criteria=row.get('c')

            if not values:
                continue
                
            # default behaviour
            tmp={index:values}
            
            # Ranges
            
            # query.i:records=modified&query.c:records=between&query.v:records:list=2009/08/12&query.v:records:list=2009/08/14
            # v[0] >= x > v[1]
            if criteria =='between':
                tmp={index:{
                    'query':values,
                    'range':'minmax'
                }}
            
            # query.i:records=modified&query.c:records=larger_then_or_equal&query.v:records=2009/08/12
            # x >= value
            elif criteria =='larger_then_or_equal':
                tmp={index:{
                    'query':values,
                    'range':'min'
                }}
            
            # query.i:records=modified&query.c:records=less_then&query.v:records=2009/08/14
            # x < value
            elif criteria =='less_then':
                tmp={index:{
                    'query':values,
                    'range':'max'
                }}
            
            
            query.update(tmp)
        return query
        
    def printQuery(self):
        return self.query
        
    def getConfig(self):        
        return CRITERION
        
        