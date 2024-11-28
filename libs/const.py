from libs.delivery_systems.desync import Desync
from libs.delivery_systems.casync import Casync
from libs.delivery_systems.rsync import Rsync
from libs.delivery_systems.wget import Wget

DESYNC = "desync"
CASYNC = "casync"
RSYNC = "rsync"
WGET = "wget"
CAS_TRANSMITTERS = {DESYNC: Desync, CASYNC: Casync}
OTHER_TRANSMITTERS = {RSYNC: Rsync, WGET: Wget}
CAS_CHUNK_SIZES_FACTOR = {DESYNC: 1, CASYNC: 1024}
