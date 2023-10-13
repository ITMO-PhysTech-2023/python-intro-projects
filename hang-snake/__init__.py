print("Select game:")
print("  1) hangman")
print("  2) snake")
print("  3) hangsnake")
print()
c = input("> ")
if c == "1":
    import hangman.run
elif c == "2":
    import snake.run
elif c == "3":
    import hangsnake.run
else:
    print("what?")
    exit(1)
