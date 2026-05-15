from SurzsEnviro.computerspeak import ComputerSpeak

def onote(rel_path: str):
	csi= ComputerSpeak()
	csi.ec(f'cat {rel_path}')

