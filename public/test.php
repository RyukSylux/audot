<?php
require_once dirname(__DIR__).'/vendor/autoload.php'; // include Composer's autoloader

use MongoDB\Client as Mongo;

$client = new Mongo("mongodb://admin:root@mongodb:27017");
$collection = $client->audot->auction_items;

$result = $collection->find( [ 'id_item' => 54849] );

foreach ($result as $entry) {
    echo $entry['_id'], ': ', $entry['id_item'], "\n";
}
?>
