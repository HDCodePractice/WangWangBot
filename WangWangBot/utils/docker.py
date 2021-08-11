import os
import asyncio
from asyncio.subprocess import PIPE
from WangWangBot.utils.logger import log
from compose.cli.command import get_project

from WangWangBot.utils.utils import chdir,NEED_SUBPROCESS_SHELL

async def check_dir_up(d, service=None ,build=False):
    command = ['docker-compose', 'up', '-d']
    if build:
        command.append('--build')
    
    if service:
        command.append(service)

    with chdir(d):
        stdout , stderr , returncode = await sync_run(*command)

    return stdout.decode() + stderr.decode(), returncode


async def check_dir_down(d):
    command = ['docker-compose', 'down']
    with chdir(d):
        stdout , stderr , returncode = await sync_run(*command)

    return stdout.decode() + stderr.decode(), returncode


async def check_dir_stop(d,service=None):
    command = ['docker-compose', 'stop']
    if service:
        command.append(service)

    with chdir(d):
        stdout , stderr , returncode = await sync_run(*command)

    return stdout.decode() + stderr.decode(), returncode


async def check_dir_kill(d):
    command = ['docker-compose', 'kill']
    with chdir(d):
        stdout , stderr , returncode = await sync_run(*command)

    return stdout.decode() + stderr.decode(), returncode


async def check_dir_rm(d="."):
    command = ['docker-compose', 'rm', '-f']
    with chdir(d):
        stdout , stderr , returncode = await sync_run(*command)
    return stdout.decode() + stderr.decode(), returncode


async def check_dir_top(d=".",service=None):
    command = ['docker-compose', 'top']
    if service:
        command.append(service)
    with chdir(d):
        stdout , stderr , returncode = await sync_run(*command)

    return stdout.decode().strip() + stderr.decode().strip(), returncode


async def check_dir_logs(d=".", service=None):
    command = ['docker-compose', 'logs', '--tail', '100']
    if service:
        command.append(service)

    log.info(command)
    with chdir(d):
        stdout , stderr , returncode = await sync_run(*command)
    return stdout.decode().strip() + stderr.decode().strip(), returncode


async def check_dir_ps(d=".",service=None):
    """
    更新docker-compose service image
    d: docker-compose yaml文件所在目录
    service: docker-compose service 名
    """
    command = ['docker-compose', 'ps'] if not service else ['docker-compose', 'ps', service]
    with chdir(d):
        stdout , stderr , returncode = await sync_run(*command)
    return stdout.decode(), returncode

async def check_dir_pull(d=".",service=None):
    """
    更新docker-compose service image
    d: docker-compose yaml文件所在目录
    image: docker-compose service 名
    """
    with chdir(d):
        command = ['docker-compose', 'pull'] if not service else ['docker-compose', 'pull', service]
        stdout , stderr , returncode = await sync_run(*command)
    return stdout.decode() + stderr.decode(), returncode

def check_dir_service_list(file_path="./"):
    project = get_project(
        project_dir=os.path.dirname(file_path)
    )
    services = project.get_services_without_duplicate()
    return services

async def container_running(container):
    command = ['docker', 'ps', '-f', f'name={container}']
    stdout , stderr , returncode = await sync_run(*command)
    return len(stdout.decode().strip().splitlines()) > 1, returncode

async def sync_run(cmd, *args, **kwargs):
    process = await asyncio.create_subprocess_exec(
        cmd, *args, stdout=PIPE, stderr=PIPE, shell=NEED_SUBPROCESS_SHELL)
    stdout, stderr = await process.communicate()
    return stdout, stderr, process.returncode
