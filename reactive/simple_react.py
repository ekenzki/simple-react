from charms.reactive import when, when_not, set_state
import charms.apt
from charmhelpers.core.hookenv import status_set
from charmhelpers.core.hookenv import log
from charms.reactive import when_all, when_any
from charms.reactive import set_flag
from charms.reactive import clear_flag
from charms.reactive import endpoint_from_flag
from charms.reactive import data_changed
from charmhelpers.core import hookenv

@when_not('simple-react.installed')
def install_simple_react():
    log("Installing git")
    status_set("waiting", "Installing git")
    charms.apt.queue_install(['git'])
    log("Git is about to be installed")
    set_state('simple-react.installed')

@when_not('db.connected')
def wating_db():
    log("waiting for mysql relation")
    status_set("blocked", "Waiting for mysql relation.")

@when_not('db.available')
@when('db.connect')
def starting_db():
    log("db connected but not available")
    status_set("waiting", "Waiting for mysql to start")

@when_not('all_done')
@when_all('apt.installed.git', 'db.available')
def installed():
    mysql = endpoint_from_flag('db.available')
    log(mysql.connection_string())

    log("All done!")
    status_set("active", "Ready - accepting connections")
    set_state('all_done')

@when_all('frontend.scania.present', 'all_done')
def signal_ready():
    log("Sending ready signal to frontends")
    frontend = endpoint_from_flag('frontend.scania.present')
    frontend.ready()
