import pathlib

req_file = tdu.expandPath(ipar.ExtPython.Pyreqs)
install_target = tdu.expandPath(ipar.ExtPython.Target)
install_script_path = pathlib.Path(install_target).parents[0]

win_file = install_script_path / 'dep_install.cmd'
mac_file = install_script_path / 'dep_install.sh'

