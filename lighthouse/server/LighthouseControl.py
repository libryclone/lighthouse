import logging.handlers
from twisted.internet import reactor
from txjsonrpc.web import jsonrpc

log = logging.getLogger()


class LighthouseController(jsonrpc.JSONRPC):
    def __init__(self, l):
        jsonrpc.JSONRPC.__init__(self)
        self.lighthouse = l

    def jsonrpc_dump_sessions(self):
        return self.lighthouse.unique_clients

    def jsonrpc_dump_indexes(self):
        r = {}
        for i in self.lighthouse.search_engine.indexes:
            r.update({i: self.lighthouse.search_engine.indexes[i].results_cache})
        return r

    def jsonrpc_dump_sd_blobs(self):
        return self.lighthouse.metadata_updater.sd_cache

    def jsonrpc_dump_cost_and_available(self):
        return self.lighthouse.metadata_updater.cost_and_availability

    def jsonrpc_stop(self):
        reactor.callLater(0.0, reactor.stop)
        return True

    def jsonrpc_is_running(self):
        return self.lighthouse.running