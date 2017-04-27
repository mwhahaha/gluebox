========
Usage
========

Run the cli::

    usage: gluebox [--version] [-v | -q] [--log-file LOG_FILE] [-h] [--debug]

    CLI to manage Puppet OpenStack Module releases

    optional arguments:
      --version            show program's version number and exit
      -v, --verbose        Increase verbosity of output. Can be repeated.
      -q, --quiet          Suppress output except warnings and errors.
      --log-file LOG_FILE  Specify a file to log output. Disabled by default.
      -h, --help           Show help message and exit.
      --debug              Show tracebacks on errors.

    Commands:
      bump bugfix    Perform a bugfix version bump
      bump dev       Remove -dev from existing version
      bump major     Perform a major version bump
      bump minor     Perform a minor version bump
      complete       print bash completion command
      git checkout   Perform module checkout to the workspace
      git cleanup    Remove module from the workspace
      git commit     Commit changes to the module in the workspace
      git review     Push the change up via git review
      help           print detailed help for another command
      release cleanup  Cleanup the releases workspace
      release new    Create a new release entry for a given release
      release update  Update a new release entry from an existing review

