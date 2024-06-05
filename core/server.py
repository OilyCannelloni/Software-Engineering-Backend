import os
import platform
import re
import subprocess
from functools import reduce

from core.game import Game
from models.models import Poll


class Server:
    def __init__(self):
        self.game = Game()

    @staticmethod
    def save_poll(poll: Poll, filename: str) -> bool:
        with open(filename, "w") as file:
            file.write(poll.to_json())
            return True

    @staticmethod
    def load_poll(filename: str) -> Poll:
        with open(filename, "r") as file:
            content = file.read()
            return Poll.from_json(content)

    @staticmethod
    def get_ip():
        def parse_result(output: str) -> str:
            output = output.split('\n')

            def remove_whitespaces(text):
                return re.sub(r'\s+', '', text)

            def compare_addresses(final_addr, addr):
                if final_addr != addr:
                    raise Exception("The addresses are not the same")
                return addr

            def is_ip(text: str):
                return re.match(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', text)

            addresses = dict((('wifi', []), ('eth', [])))
            for conn_type, addr in zip(output[::2], output[1::2]):
                if "Wi-Fi" in conn_type:
                    addr = remove_whitespaces(addr)
                    if is_ip(addr):
                        addresses['wifi'].append(addr)
                elif "Ethernet" in conn_type:
                    addr = remove_whitespaces(addr)
                    if is_ip(addr):
                        addresses['eth'].append(addr)
                else:
                    print("unknown type")
            if addresses['eth']:
                return reduce(compare_addresses, addresses['eth'])
            elif addresses['wifi']:
                return reduce(compare_addresses, addresses['wifi'])
            raise Exception("No IP address found")

        def get_win_ip_address():
            batch_script = 'scripts\win_ip_script.bat'
            if not os.path.exists(batch_script):
                raise FileNotFoundError(f"The batch script '{batch_script}' does not exist.")
            result = subprocess.run([batch_script], capture_output=True, text=True, shell=True)
            return parse_result(result.stdout)

        def get_linux_ip_address():
            script_file = "scripts/linux_ip_script.sh"
            os.chmod(script_file, 0o755)
            result = subprocess.run([script_file], capture_output=True, text=True)
            return parse_result(result.stdout)

        os_name = platform.system()
        if os_name == "Windows":
            return get_win_ip_address()
        elif os_name == "Darwin":
            return get_linux_ip_address()
        elif os_name == "Linux":
            return get_linux_ip_address()
        else:
            print(f"Unsupported OS: {os_name}")


server = Server()
