from libs.delivery_systems.desync import Desync
from libs.delivery_systems.casync import Casync
from libs.delivery_systems.rsync import Rsync
from libs.delivery_systems.wget import Wget
from libs.target_function.time import Time
from libs.target_function.traffic import Traffic

DESYNC = "desync"
CASYNC = "casync"
RSYNC = "rsync"
WGET = "wget"
TIME = "time"
TRAFFIC = "traffic"

CAS_TRANSMITTERS = {DESYNC: Desync, CASYNC: Casync}
OTHER_TRANSMITTERS = {RSYNC: Rsync, WGET: Wget}
CAS_CHUNK_SIZES_FACTOR = {DESYNC: 1, CASYNC: 1024}

TARGET_FUNCTIONS = {TIME: Time, TRAFFIC: Traffic}
