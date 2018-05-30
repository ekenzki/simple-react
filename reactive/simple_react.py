from charms.reactive import when, when_not, set_state
import charms.apt
from charmhelpers.core.hookenv import status_set
from charmhelpers.core.hookenv import log


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

@when('apt.installed.git')
def installed():
    status_set("active", "Ready")
