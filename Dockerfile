FROM scratch
ADD rootfs.tar /
ENV PATH=/usr/local/bin:/usr/bin:/bin PYTHONPATH=/workspace/.jof-phase1-deps PYTHONDONTWRITEBYTECODE=1 LANG=C.UTF-8 LC_ALL=C.UTF-8 HOME=/root GIT_OPTIONAL_LOCKS=0 GIT_CONFIG_SYSTEM=/etc/gitconfig
WORKDIR /repo
ENTRYPOINT ["/workspace/.venvs/global-lnn-sci/bin/python", "/opt/v15/verify_entry.py"]
