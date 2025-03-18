
import flet as ft
from bidi.algorithm import get_display

import time
import asyncio
from views.splash_screen import Splash,SplashFirst,PatientInfo,WelcomeScreen
from views.home_screen import Home,Home2,Settings,DoctorsView
from views.MedicalAnalysisApp import MedicalAnalysisApp
from views.home_screen import ResultsView
import flet as ft
# def main(page: ft.Page) -> None:
#     page.theme_mode = ft.ThemeMode.LIGHT
#     page.window.width = 380
#     page.window.height = 750
#     page.window.top = 0.5
#     page.window.left = 898
#     page.padding = 0

#     async def show_splash_sequence():
#         page.views.append(SplashFirst())
#         page.update()
#         # زيادة وقت الانتظار إلى 2 ثواني
#         await asyncio.sleep(2.0)
#         page.views.clear()
#         page.views.append(PatientInfo())
#         page.update()


#     # async def Splash():
#     #     await asyncio.sleep(3.0)
#     #     page.views.clear()
#     #     page.views.append(Splash())
#     #     page.update()
#     #     page.go("/")


      

#     def router(route: str) -> None:
#         print(f"Route changing to: {route}")
#         page.views.clear()
    
#         if page.route == "/":
#             asyncio.run(show_splash_sequence())
#         elif page.route == "/home":
#             page.views.append(Home())
#         elif page.route == "/PatientInfo":
#             page.views.append(PatientInfo())
#         elif page.route == "/home2":
#             page.views.append(Home2())
#         elif page.route == "/MedicalAnalysisApp":
#             medical_app = MedicalAnalysisApp()
#             # تأكد من تنظيف الـ views السابقة
#             page.views.clear()
#             page.views.append(medical_app)
#             page.update()
#         elif page.route == "/results":
#             if hasattr(page, 'results_data'):
#                 page.views.append(ResultsView(page.results_data))
#             else:
#                 print("No results data found")
#                 page.go("/home")
#         elif page.route == "/WelcomeScreen":
#             if hasattr(page, 'results_data'):
#                 results_view = WelcomeScreen(page.results_data)
#                 page.views.append(results_view)
#                 page.update()
               
#         # زيادة وقت الانتظار إلى 2 ثواني
           
#             else:
#                 print("No results data found")
#                 page.go("/PatientInfo")
            
        
#         page.update()
#     def view_pop(view):
#         page.views.pop()
#         top_view = page.views[-1]
#         page.go(top_view.route)
#     page.on_route_change = router
#     page.on_view_pop = view_pop
#     page.go("/")
#     # باقي الدوال تبقى كما هي...
# ft.app(target=main, assets_dir="assets")




# import flet as ft
# import asyncio
# from views.splash_screen import Splash  # Splash هو View
# from views.home_screen import Home, Home2, PatientInfo  # تأكد من استيراد PatientInfo
# from views.MedicalAnalysisApp import MedicalAnalysisApp
# from views.home_screen import ResultsView
# from views.splash_screen import WelcomeScreen






# import flet as ft
# import asyncio
# from views.splash_screen import Splash  # Splash هو View
# from views.home_screen import Home, Home2, PatientInfo  # تأكد من استيراد PatientInfo
# from views.MedicalAnalysisApp import MedicalAnalysisApp
# from views.home_screen import ResultsView
# from views.WelcomeScreen import WelcomeScreen


async def show_splash_sequence(page: ft.Page):
    page.views.append(SplashFirst())  # اعرض Splash مباشرة (الأزرار)
    page.update()
    await asyncio.sleep(3.0)  # انتظار اختياري
    page.views.clear()
    page.views.append(PatientInfo())  # ثم اعرض PatientInfo
    page.update()


def main(page: ft.Page) -> None:
    page.theme_mode = ft.ThemeMode.LIGHT
    page.window.width = 380
    page.window.height = 750
    page.window.top = 0.5
    page.window.left = 898
    page.padding = 0
    async def router(route: str) -> None:
        print(f"Route changing to: {route}")
        page.views.clear()

        if page.route == "/":
            await show_splash_sequence(page) # يتم استدعاء show_splash_sequence عند "/"
        elif page.route == "/home":
            page.views.append(Home())
        elif page.route == "/Splash":
            
            page.views.append(Splash())
        elif page.route == "/doctors":
            page.views.append(DoctorsView())
        elif page.route == "/PatientInfo":
            page.views.append(PatientInfo())
        elif page.route == "/settings":
            page.views.append(Settings())
        elif page.route == "/home2":
            page.views.append(Home2())

            
        elif page.route == "/MedicalAnalysisApp":
            medical_app = MedicalAnalysisApp()
            page.views.clear()
            page.views.append(medical_app)
        elif page.route == "/results":
            if hasattr(page, 'results_data'):
                page.views.append(ResultsView(page.results_data))
            else:
                print("No results data found")
                page.go("/home")
        elif page.route == "/WelcomeScreen":
            if hasattr(page, 'results_data'):
                results_view = WelcomeScreen(page.results_data)
                page.views.append(results_view)
                page.update()
                await asyncio.sleep(9.0)  # انتظار 3 ثوانٍ
                page.views.clear()
                page.views.append(Splash())
                page.update()  # الانتقال إلى Splash (المسار "/")
            else:
                print("No results data found")
                
        page.update()
    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)
    page.on_route_change = router
    page.on_view_pop = view_pop
    page.go("/")  # ابدأ بالمسار "/"
ft.app(target=main, assets_dir="assets")





























