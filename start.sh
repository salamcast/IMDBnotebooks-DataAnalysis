#!/bin/bash

sudo chown -R mysql:mysql /export/.ht_mysql
sudo systemctl restart mysqld
cd /export
jupyter-lab --ip="*" 
