import logging
import sys

import click

from typing import Optional
import storm.__main__ as storm

log = logging.getLogger(__name__)


@click.group()
@click.version_option()
def cli():
    # log to sys out
    logging.basicConfig(stream=sys.stdout, format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


@cli.command('add-runtime')
@click.argument("name")
@click.argument("connection_uri")
@click.option("--id_file", "-id", required=False, type=click.STRING,
              help="The private key file that should be used for authentication")
@click.option("--config", "-c", required=False, type=click.STRING, help="The ssh config file")
def add_runtime(name: str, connection_uri: str, id_file: Optional[str] = None, config: Optional[str] = None):
    storm.add(name, connection_uri, id_file, [], config)


@cli.command('edit-runtime')
@click.argument("name")
@click.argument("connection_uri")
@click.option("--id_file", "-id", required=False, type=click.STRING,
              help="The private key file that should be used for authentication")
@click.option("--config", "-c", required=False, type=click.STRING, help="The ssh config file")
def edit_runtime(name: str, connection_uri: str, id_file: Optional[str] = None, config: Optional[str] = None):
    storm.update(name, connection_uri, id_file, [], config)


@cli.command('delete-runtime')
@click.argument("name")
@click.option("--config", "-c", required=False, type=click.STRING, help="The ssh config file")
def delete_runtimes(name: str, config: Optional[str] = None):
    storm.delete(name, config)


@cli.command('list-runtimes')
def list_runtime():

    from lazycluster import RuntimeManager, NoRuntimesDetectedError

    try:
        runtime_group = RuntimeManager().create_group()
    except NoRuntimesDetectedError:
        print('\nNo runtimes detected!')

    # Accessing an info attribute will enforce the actual reading of the data via ssh. Since the reading causes
    # many prints to the console we enforce this before actually printing the desired output.json.loads
    for runtime in runtime_group.runtimes:
        runtime.info


    runtime_group.cleanup()

    print('\n\u001b[1m')
    print(str(runtime_group.runtime_count) + ' Runtimes detected:')
    print('\u001b[0m')

    runtime_group.print_runtime_info()

    print('\n')


if __name__ == '__main__':
    cli()