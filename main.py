import logic
from gui import App

if __name__ == '__main__':
    print('📱 Starting app')
    first_run = not logic.hay_usuarios_registrados()
    app = App(is_first_run=first_run)
    app.mainloop()
