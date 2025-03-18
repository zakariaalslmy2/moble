import flet as ft
import threading
import time

class DoctorsView(ft.UserControl):
    def __init__(self):
        super().__init__()
        self.route = "/doctors"
        self.doctors_data = [
            {"name": "د. أحمد علي", "phone": "+967 777 123 456", "specialty": "أخصائي قلب"},
            {"name": "د. فاطمة سالم", "phone": "+967 733 987 654", "specialty": "أخصائي أطفال"},
            {"name": "د. عمر حسن", "phone": "+967 711 555 222", "specialty": "أخصائي أعصاب"},
            {"name": "د. ليلى محمد", "phone": "+967 772 333 444", "specialty": "أخصائي جلدية"},
            {"name": "د. سامي يوسف", "phone": "+967 735 777 888", "specialty": "جراح عام"},
            {"name": "د. هدى إبراهيم", "phone": "+967 778 999 000", "specialty": "أخصائي عيون"},
            {"name": "د. خالد سعيد", "phone": "+967 712 444 555", "specialty": "جراح عظام"},
            {"name": "د. منى عبد الله", "phone": "+967 774 666 777", "specialty": "أخصائي أنف وأذن وحنجرة"},
            {"name": "د. رامي ناصر", "phone": "+967 736 888 999", "specialty": "أخصائي مسالك بولية"},
            {"name": "د. نور مصطفى", "phone": "+967 779 111 222", "specialty": "طبيب نفسي"},
        ]
        self.doctors_list = ft.ListView(expand=1, spacing=10, padding=20, auto_scroll=True)


    def build(self):
        self.update_list()  # Initial list build
        return ft.Column(
            controls=[
                ft.Container(
                    content=ft.Text("الأطباء", size=28, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER),
                    alignment=ft.alignment.top_center,
                    padding=ft.padding.only(top=20, bottom=10),  # More padding for title
                    # bgcolor=ft.colors.BLUE_GREY_100, # Optional: subtle background
                ),
                ft.Divider(height=2, color=ft.colors.GREY_400), # Thinner divider
                self.doctors_list,
            ],
            expand=True,
        )

    def update_list(self):
        """Refreshes the doctor list view."""
        self.doctors_list.controls.clear()
        for doctor in self.doctors_data:
            self.doctors_list.controls.append(
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Text(doctor["name"], size=20, weight=ft.FontWeight.BOLD),
                            ft.Text(doctor["specialty"], size=16, color=ft.colors.GREY_600), # Darker grey
                            ft.Row(
                                [
                                    ft.Icon(ft.icons.PHONE, color=ft.colors.BLUE_500), # Themed icon
                                    ft.Text(doctor["phone"], size=16, font_family="Roboto"), # Use a common font
                                ],
                                alignment=ft.MainAxisAlignment.START
                            ),
                        ],
                        tight=True, # Reduce spacing within the column
                        horizontal_alignment=ft.CrossAxisAlignment.STRETCH # Ensure elements fill the width
                    ),
                    bgcolor=ft.colors.WHITE,
                    border=ft.border.all(1, ft.colors.GREY_300),
                    border_radius=ft.border_radius.all(12),  # Slightly larger radius
                    padding=ft.padding.symmetric(vertical=12, horizontal=16), # More padding for content
                    shadow=ft.BoxShadow(
                        spread_radius=0,  # Tighter shadow
                        blur_radius=4,
                        color=ft.colors.GREY_400,
                        offset=ft.Offset(0, 2),
                    ),
                   # margin=ft.margin.only(bottom=8), # Add some bottom margin between cards
                )
            )
        self.update()