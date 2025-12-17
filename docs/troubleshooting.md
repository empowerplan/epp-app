# Troubleshooting

## Upgrading numpy

Upgrading the numpy version led to an error in the django caching function as
pickle loading in redis had changed in numpy.
Error says: `ModuleNotFoundError: No module named 'numpy._core.numeric'`

Solution: Flushing of redis via
`docker exec -it <redis_container> redis-cli -a YOUR_PASSWORD FLUSHDB`
