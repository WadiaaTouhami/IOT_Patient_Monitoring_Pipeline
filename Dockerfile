
 FROM confluentinc/cp-kafka-connect-base:5.3.2
 
 ENV  CONNECT_PLUGIN_PATH="/usr/share/java,/usr/share/confluent-hub-components" 
 
 RUN confluent-hub install --no-prompt mongodb/kafka-connect-mongodb:latest
