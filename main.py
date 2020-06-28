import os
import sys

from PyQt5.QtCore import QProcess, QProcessEnvironment
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel

core_process = None
label = None


def on_core_finished(exit_code, exit_status):
    label.setText("Stopped with exit code %d and status %d" % (exit_code, exit_status))


def on_core_read_ready():
    raw_output = bytes(core_process.readAll())
    decoded_output = raw_output.decode(errors="replace")
    print("Core -> %s" % decoded_output.strip())


if __name__ == "__main__":
    if 'CORE_PROCESS' in os.environ:
        print("Hi!")
    else:
        app = QApplication([])
        window = QWidget()
        layout = QVBoxLayout()
        label = QLabel('Core process running')
        layout.addWidget(label)
        window.setLayout(layout)
        window.show()

        # Spawn QProcess
        print("Spawning process")
        core_env = QProcessEnvironment.systemEnvironment()
        core_env.insert("CORE_PROCESS", "1")

        core_process = QProcess()
        core_process.setProcessEnvironment(core_env)
        core_process.readyRead.connect(on_core_read_ready)
        core_process.finished.connect(on_core_finished)
        core_process.start(sys.executable, sys.argv)

        app.exec_()
