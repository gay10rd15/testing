import customtkinter

root = customtkinter.CTk()
root.title("test")
pb = customtkinter.CTkProgressBar(
    root,
    mode="determinate",
    orientation="horizontal",
    height=50,
    width=100,
).pack()

customtkinter.CTkButton(root, text="start").pack()

root.mainloop()
