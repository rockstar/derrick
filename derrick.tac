from twisted.application import internet, service
from twisted.web import server

from derrick.resource import DerrickRootResource


application = service.Application('derrick')
service = internet.TCPServer(8080, server.Site(DerrickRootResource()))

service.setServiceParent(application)
