<?php
# Reseed script
#

# Database settings
define('MYSQL_HOSTNAME','127.0.0.1');
define('MYSQL_USERNAME','user name');
define('MYSQL_PASSWORD','password');
define('MYSQL_DATABASE','database name');

# Other settings
define('NETDB_DIR', '/Users/meeh/Sites/reseed/netDb/');
define('NUM_ROUTERS', 60);
define('DEBUG', true);

$testips = array(
    '127.0.0.1',
);

/*
-------------------------------------
Add following to .htaccess:
Options +FollowSymlinks
RewriteEngine On
RewriteRule ^(.*\.dat)$ /index.php?file=$1 [L]
RewriteCond %{REQUEST_FILENAME} !index.php
RewriteCond %{REQUEST_FILENAME} !robots.txt

-------------------------------------
Please paste this into your mysql database:

CREATE  TABLE `clients` (
  `id` INT NOT NULL AUTO_INCREMENT ,
  `host` VARCHAR(255) NOT NULL ,
  `time` INT NOT NULL ,
  PRIMARY KEY (`id`) );

CREATE  TABLE `rientry` (
  `id` INT NOT NULL AUTO_INCREMENT ,
  `time` INT NOT NULL ,
  `ristring` VARCHAR(100) NOT NULL ,
  PRIMARY KEY (`id`) );

-------------------------------------
Do not touch if you don't know what you're doing.
*/

# Database handle
class ReseedDatabase {

    protected $db;
    
    public function __construct($h,$u,$p,$d) {
        $this->db = new mysqli($h,$u,$p,$d);
    }

    public function insertEntry($time, $entry) {
        if ($results = $this->db->query(sprintf('insert into rientry (time,ristring) values ("%d","%s");', $time, $entry))) return true;
        return false;
    }

    public function insertClient($time, $host) {
        if ($results = $this->db->query(sprintf('insert into clients (host,time) values ("%s","%d");', $host, $time))) return true;
        return false;
    }

    public function getEntries($time) {
        if ($results = $this->db->query(sprintf('select * from rientry where time = %d', $time))) {
            $t = array();
            while ($j = $results->fetch_assoc()) {
                $t[] = $j;
            }
            return $t;
        }
        return false;
    }

    public function getEntriesFromClient($host) {
        if ($results = $this->db->query(sprintf('select e.ristring from rientry e, clients c where c.time=e.time and c.host = "%s";', $host))) {
            $t = array();
            while ($j = $results->fetch_assoc()) {
                $t[] = $j['ristring'];
            }
            return $t;
        }
        return false;
    }

    public function getClient($host) {
        if ($results = $this->db->query(sprintf('select * from clients where host = "%s";', $host))) {
            if ($results->num_rows>0) return true;
        }
        return false;
    }

    public function cleanup() {
        $this->db->query(sprintf('delete from clients where time < "%d";', (time() - 86400)));
        $this->db->query(sprintf('delete from rientry where time < "%d";', (time() - 87000)));
    }

    public function close() {
        $this->db->close();
    }

}


$user_agent = $_SERVER['HTTP_USER_AGENT'];
$remote_ip = $_SERVER["REMOTE_ADDR"];
$myh = MYSQL_HOSTNAME;
$myu = MYSQL_USERNAME;
$myp = MYSQL_PASSWORD;
$myd = MYSQL_DATABASE;
if (!in_array($remote_ip,$testips) && true !== DEBUG && !strstr($user_agent, 'Wget/1.11.4')) {
    header('HTTP/1.0 400 Access Denied');
    header('Content-Type: text/plain');
    die("Access denied.");
}

// if they're requesting a file, let's try to send it to them
if (isset($_GET['file'])) {
    // sanitize the input filename
    $file = htmlentities($_GET['file'], ENT_QUOTES, 'UTF-8', false);
    $file = str_replace('..', '', str_replace('/', '', $file));
    $file = realpath(NETDB_DIR . DIRECTORY_SEPARATOR . $file);
    $filename = basename($file);

    // make sure they are requesting a real file
    if (!$file || empty($filename) ||
        #NETDB_DIR !== substr($file, 0, strlen(NETDB_DIR)) ||
        preg_match("/^routerInfo-(.+)\=.dat$/", $filename) !== 1 ||
        !file_exists($file) ||
        is_dir($file)
    ) {
        header('HTTP/1.0 404 Not Found');
        header('Content-Type: text/plain');
        die('Not found.');
    }

    $db = new ReseedDatabase($myh,$myu,$myp,$myd);
    $res = $db->getEntriesFromClient($remote_ip);
    $db->close();
    unset($db);
    if ($res === false || !in_array($filename, $res)) {
        header('HTTP/1.0 404 Not Found');
        header('Content-Type: text/plain');
        die('Not found.');
    }

    header('Content-Type: application/octet-stream');
    header('Content-Transfer-Encoding: binary');
    header('Content-Length: ' . filesize($file));
    header(sprintf('Content-Disposition: attachment; filename="%s"', $filename));

    ob_clean();
    flush();
    readfile($file);

    die();
}

$page = '<html><head><title>NetDB</title></head><body><ul>%s</ul></body></html>';
$entry = '<li><a href="%s">%s</a></li>';

$db = new ReseedDatabase($myh,$myu,$myp,$myd);
if ($db->getClient($remote_ip) === false) {
    $time = time();
    $db->insertClient($time, $remote_ip);

    # generate new list
    $clientRouterList = array();
    if (is_dir(NETDB_DIR) && is_readable(NETDB_DIR)) {
        $clientRouterList = array_map('basename', glob(NETDB_DIR . DIRECTORY_SEPARATOR . 'routerInfo-*=.dat', GLOB_ERR));
    }

    foreach (array_rand($clientRouterList, NUM_ROUTERS) as $router) {
        $db->insertEntry($time, $clientRouterList[$router]);
    }
} else {
    // run cleanup 50% of requests
    if (rand(0, 100) < 50) {
       $db->cleanup();
    }
}

# use old list based on date in database, i.e. sends the same as before
$clientRouterList = $db->getEntriesFromClient($remote_ip);

$db->close();
unset($db);

header('Content-Type: text/html');
die(sprintf($page, implode('', array_map(function($single) use ($entry) { return sprintf($entry, $single, $single);}, $clientRouterList))));

