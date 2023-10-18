# Autoscaler script to Handle replicas of application based on CPU utilization


if the cpu utilization is above 80% the script will scale the application by adding 3 replicas

if the cpu utilization is belove 60% the script will scale down the replicas by 3

if the cpu utilization is with in threshold(60-80%) no scale up/ scale down

Application always tries to maintain minimum 3 replicas of the application
