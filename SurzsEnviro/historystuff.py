from computerspeak import ComputerSpeak

def historycall(file: str):
    csi=ComputerSpeak()
    rawc=csi.ec(f"cat {file}")
    cleanc= rawc.split("---------------------------------------")[-1]
    print(cleanc)
    return cleanc