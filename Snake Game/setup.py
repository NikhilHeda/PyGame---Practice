import cx_Freeze

executables = [cx_Freeze.Executable("snake.py")]

cx_Freeze.setup(
	name = "Slither",
	options = {"build_exe" : {"packages":["pygame"], "include_files":["apple.png", "snake.png"]}},
	description = "Slither Game",
	executables = executables
)

