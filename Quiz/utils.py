def destroy_widgets(root):
    for widget in root.winfo_children():
        widget.destroy()