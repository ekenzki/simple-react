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
    # Do your setup here.
    #
    # If your charm has other dependencies before it can install,
    # add those as @when() clauses above., or as additional @when()
    # decorated handlers below
    #
    # See the following for information about reactive charms:
    #
    #  * https://jujucharms.com/docs/devel/developer-getting-started
    #  * https://github.com/juju-solutions/layer-basic#overview
    #
    log("Installing git")
    status_set("waiting", "Installing git")
    charms.apt.queue_install(['git'])
    log("Git installed")
    set_state('simple-react.installed')

@when_not('all_done')
@when_all('apt.installed.git', 'db.available')
def installed():
    mysql = endpoint_from_flag('db.available')
    log(mysql.connection_string())

    log("All done!")
    status_set("active", "Ready")
    set_state('all_done')

@when_not('db.connected')
def wating_db():
    log("waiting for mysql relation")
    status_set("blocked", "Waiting for mysql relation.")

@when_not('db.available')
@when('db.connect')
def starting_db():
    log("db connected but not available")
    status_set("waiting", "Waiting for mysql to start")


