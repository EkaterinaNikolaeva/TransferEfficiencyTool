from libs.delivery_systems.desync import Desync
from libs.delivery_systems.casync import Casync
from libs.delivery_systems.rsync import Rsync

DESYNC = "desync"
CASYNC = "casync"
RSYNC = "rsync"
CAS_TRANSMITTERS = {DESYNC: Desync, CASYNC: Casync}
RSYNC_TRANSMITTERS = {RSYNC: Rsync}
CAS_CHUNK_SIZES_FACTOR = {DESYNC: 1, CASYNC: 1024}
