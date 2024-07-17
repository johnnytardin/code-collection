docker run \
    -v ~/.openbb_terminal/:/home/python/.openbb_terminal \
    -v ~/OpenBBUserData:/home/python/OpenBBUserData \
    -it \
    --rm \
    ghcr.io/openbb-finance/openbbterminal-poetry:1.6.0
