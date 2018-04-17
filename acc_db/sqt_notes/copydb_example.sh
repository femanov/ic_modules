#!/bin/sh

pg_dump -C -h localhost -U postgres icdata | psql -h linac3 -U postgres icdata