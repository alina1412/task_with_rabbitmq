#!/bin/sh


# echo "127.0.0.1 localhost" > /etc/hosts
# echo "127.0.1.1 node1" >> /etc/hosts

# echo "node1" > /etc/hostname

# Create Rabbitmq user
( rabbitmqctl wait --timeout 60 $RABBITMQ_PID_FILE ; \
rabbitmqctl add_user $RABBITMQ_DEFAULT_USER $RABBITMQ_DEFAULT_PASS 2>/dev/null ; \
rabbitmqctl set_user_tags $RABBITMQ_DEFAULT_USER administrator ; \
rabbitmqctl set_permissions -p / $RABBITMQ_DEFAULT_USER  ".*" ".*" ".*" ; \
echo "*** User '$RABBITMQ_DEFAULT_USER' with password '$RABBITMQ_DEFAULT_PASS' completed. ***" ; \
echo "*** Log in the WebUI at port 15672 (example: http:/localhost:15672) ***") &

# $@ is used to pass arguments to the rabbitmq-server command.
# For example if you use it like this: docker run -d rabbitmq arg1 arg2,
# it will be as you run in the container rabbitmq-server arg1 arg2
# echo "NODENAME=rabbit@my-docker" > /etc/rabbitmq/rabbitmq-env.conf &


rabbitmq-server $@ 
# OUTPUT=$(rabbitmqctl eval "node().") &
# echo "------ node name ---'${OUTPUT}'" &


