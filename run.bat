@echo off
call venv\Scripts\activate
python -c "from gui.splash_screen import SplashScreen; from gui.main_menu import StartWindow; SplashScreen(lambda: StartWindow().mainloop()).mainloop()"
pause
