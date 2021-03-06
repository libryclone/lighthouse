import argparse
import logging.handlers
import os
import sys

from twisted.web import server
from twisted.internet import reactor
from jsonrpc.proxy import JSONRPCProxy

from lbrynet import conf as lbrynet_conf
from lighthouse.server.api import Lighthouse
from lighthouse.server.LighthouseServer import LighthouseControllerServer, LighthouseServer
from lighthouse.updater.Blockchain import LBRYcrdManager
from lighthouse.updater.Updater import DBUpdater


RPC_PORT = 50004

DEFAULT_FORMAT = "%(asctime)s %(levelname)-8s %(name)s:%(lineno)d: %(message)s"
DEFAULT_FORMATTER = logging.Formatter(DEFAULT_FORMAT)

log = logging.getLogger()
console_handler = logging.StreamHandler(sys.stdout)
file_handler = logging.FileHandler(os.path.join(os.path.expanduser("~/"), "lighthouse.log"))
console_handler.setFormatter(DEFAULT_FORMATTER)
file_handler.setFormatter(DEFAULT_FORMATTER)
log.addHandler(console_handler)
log.addHandler(file_handler)
log.setLevel(logging.INFO)
logging.getLogger("lbrynet").setLevel(logging.WARNING)
logging.getLogger("requests").setLevel(logging.WARNING)


def cli():
    ecu = JSONRPCProxy.from_url("http://localhost:%i" % RPC_PORT)
    try:
        s = ecu.is_running()
    except:
        print "lighthouse isn't running"
        sys.exit(1)
    args = sys.argv[1:]
    meth = args[0]
    if args:
        print ecu.call(meth)
    else:
        print ecu.call(meth, args)


def start():
    parser = argparse.ArgumentParser()
    parser.add_argument('--lbrycrdd-data-dir')
    args = parser.parse_args()
    # the blob manager needs this directory to exists
    lbrynet_conf.settings.ensure_data_dir()
    lbrycrdd = LBRYcrdManager(args.lbrycrdd_data_dir)
    db_updater = DBUpdater(lbrycrdd)
    engine = Lighthouse(db_updater)
    lighthouse_server = LighthouseServer(engine)
    ecu = LighthouseControllerServer(engine)
    engine.start()
    s = server.Site(lighthouse_server.root)
    e = server.Site(ecu.root)

    reactor.listenTCP(50005, s)
    reactor.listenTCP(RPC_PORT, e, interface="localhost")
    reactor.run()


def stop():
    ecu = JSONRPCProxy.from_url("http://localhost:%i" % RPC_PORT)
    try:
        r = ecu.is_running()
        ecu.stop()
        print "lighthouse stopped"
    except:
        print "lighthouse wasn't running"


if __name__ == "__main__":
    start()
