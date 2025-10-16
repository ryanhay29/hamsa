from hamsa import HamsaHand
import code

# Initialize hand
hand = HamsaHand()
print("Hamsa hand ready. You can now type commands like:")
print("  hand.curl_pinky(0.5, 700)")
print("  hand.wiggle_index(0.7, 2000)")
print("Type 'exit()' or Ctrl-D to quit.\n")

# Start interactive console with `hand` preloaded
variables = globals().copy()
variables.update(locals())
shell = code.InteractiveConsole(variables)
shell.interact(banner="Hamsa Hand Interactive Mode")

