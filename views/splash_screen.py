
import flet as ft
import asyncio  # Import asyncio

import flet as ft

class Splash(ft.View):
    def __init__(self):
        super().__init__()
        self.route = "/"  # الواجهة الرئيسية
        self.padding = ft.padding.all(0)  # إزالة الهوامش الافتراضية
        self.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        self.vertical_alignment = ft.MainAxisAlignment.CENTER
        self.bgcolor = "#E6F3F3"  # لون خلفية متناسق مع الواجهات الأخرى

        # --- Header ---
        self.header = ft.Container(
            content=ft.Row(
                controls=[
                    ft.Text(
                        "تطبيق التشخيص الطبي",
                        size=24,
                        weight=ft.FontWeight.BOLD,
                        color=ft.colors.WHITE,  # لون أزرق داكن للنص
                        font_family="Cairo",
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,  # توسيط العنوان
            ),
            bgcolor="#87CEEB",  # لون أزرق فاتح للخلفية (متناسق)
            padding=ft.padding.symmetric(vertical=10), # هوامش رأسية
            height=70,  # ارتفاع مناسب
            # محاذاة رأسية وأفقية للمحتوى
            alignment=ft.alignment.center,
        )

        # --- Texts ---
        self.app_title = ft.Text(
            value="اكتشف صحتك بسهولة",
            size=28,  # حجم أكبر قليلاً
            weight=ft.FontWeight.BOLD,
            color="#004AAD",  # نفس اللون الأزرق الداكن
            font_family="Cairo",
            text_align=ft.TextAlign.CENTER,
        )

        self.welcome_message = ft.Text(
            value="ابدأ رحلة التشخيص الذكي الآن", # رسالة ترحيبية أوضح
            size=16,
            color=ft.colors.GREY_700, # لون رمادي للنص
            text_align=ft.TextAlign.CENTER,
            font_family="Cairo"
        )

        # --- Buttons ---
        def create_styled_button(text, route):
            return ft.ElevatedButton(
                content=ft.Text(
                    value=text,
                    color=ft.colors.WHITE,
                    font_family="Cairo",
                    size=16,
                    weight=ft.FontWeight.W_500,
                ),
                width=280, # عرض أوسع قليلاً
                height=55,  # ارتفاع أكبر قليلاً
                style=ft.ButtonStyle(
                    bgcolor={
                        ft.MaterialState.DEFAULT: "#87CEEB",  # لون أزرق للزر
                        ft.MaterialState.HOVERED: "#0056b3",   # لون أزرق أغمق عند التحويم
                    },
                    shape=ft.RoundedRectangleBorder(radius=12), # حواف أكثر استدارة
                    elevation={
                        ft.MaterialState.DEFAULT: 2,
                        ft.MaterialState.HOVERED: 4
                    }
                ),
                on_click=lambda e: e.page.go(route)
            )

        self.btn1 = create_styled_button("كتابة الأعراض", "/home")
        self.btn_pain = create_styled_button("تحديد الأعراض", "/home2") # نص أوضح
        self.btn2 = create_styled_button("تحليل صورة الفحص", "/MedicalAnalysisApp")


        # --- Card ---
        self.button_card = ft.Card(
            elevation=4,  # ظل أقل
            color="#FFFFFF",  # لون أبيض للخلفية
            content=ft.Container(
                content=ft.Column(
                    [
                        self.btn_pain,
                        ft.Divider(height=5, color="transparent"), # فاصل
                        self.btn1,
                        ft.Divider(height=5, color="transparent"),
                        self.btn2,
                    ],
                    spacing=10,  # مسافة أقل بين الأزرار
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                width=300,
                padding=ft.padding.all(30), # هوامش أكبر داخل البطاقة
                border_radius=ft.border_radius.all(20) # حواف أكثر استدارة
            )
        )

        # --- Main Content ---
        self.splash_content = ft.Container(
            content=ft.Column(
                [
                    # self.app_title,  <-- Removed to avoid repetition
                    ft.Divider(height=20, color="transparent"), # فاصل
                    self.welcome_message,
                    ft.Divider(height=40, color="transparent"), # فاصل أكبر
                    self.button_card,
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            # width=360,  <-- Removed, let the container adapt to content
            # height=750, <-- Removed
            expand=True, # توسيع ليملأ الشاشة
        )

        self.controls = [self.header, self.splash_content] # الهيدر والمحتوى



        
import flet as ft

# --- Constants (Refined) ---
PRIMARY_COLOR = "#87CEEB"  # Sky Blue
SECONDARY_COLOR = "#4682B4"  # Steel Blue
ERROR_COLOR = "#DB4437"
TEXT_COLOR = "#333333"  # Dark gray for text
BG_COLOR = "#F0F4F8"  # Lighter background for better contrast
BUTTON_HOVER_COLOR = "#60A5D8"  # Lighter Steel Blue for hover effect

import flet as ft

import flet as ft

class WelcomeScreen(ft.View):
    def __init__(self, results_data):
        super().__init__(
            padding=0,
            bgcolor="white"  # Start with white, gradient will overlay
        )
        self.results_data = results_data
        self.vertical_alignment = ft.MainAxisAlignment.CENTER
        self.horizontal_alignment = ft.CrossAxisAlignment.CENTER

        # Re-use title style from SplashFirst, but adapt
        self.__title = ft.Text(
            value="تطبيق التشخيص الطبي",  # Arabic title
            color=ft.colors.BLUE_GREY_900,  # Darker color for better contrast
            size=28,  # Slightly smaller than SplashFirst
            font_family="Cairo",  # Use Cairo for Arabic
            weight=ft.FontWeight.BOLD,
            text_align=ft.TextAlign.CENTER,
        )

        self.__logo = self._create_logo()  # Use the improved logo
        self.__user_greeting = self._create_user_greeting()

        # Main container, mimicking SplashFirst's structure
        self.__container = ft.Container(
            width=380,
            height=750,
            content=ft.Column(
                controls=[
                    self.__title,
                    self.__logo,
                    ft.Container(height=20),  # Spacing
                    self.__user_greeting,
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            gradient=ft.LinearGradient(  # Same gradient as SplashFirst
                begin=ft.alignment.top_center,
                end=ft.alignment.bottom_center,
                colors=["#87CEEB", "#D3D3D3"]
            ),
            border=ft.border.all(1, ft.colors.GREY_300), # subtle border
        )

        self.controls = [self.__container]



    def _create_logo(self):
        return ft.Container(
            content=ft.Image(
                src="assets/ai.jpg",
                width=180,  # Slightly smaller than SplashFirst's logo
                height=180,
                fit=ft.ImageFit.CONTAIN,  # Use CONTAIN to avoid distortion
                border_radius=ft.border_radius.all(90),  # Circular
            ),
            margin=ft.margin.only(top=10, bottom=10),  # Adjust margins
            alignment=ft.alignment.center,
             shadow=ft.BoxShadow(  # Add shadow for depth
                spread_radius=1,
                blur_radius=8,
                color=ft.colors.GREY_400,
                offset=ft.Offset(0, 4),
            ),
        )

    def _create_user_greeting(self):
        return ft.Container(
            content=ft.Text(
                value=f"مرحبًا بك يا {self.results_data.get('patient_name', 'مستخدم')}!",
                color=ft.colors.BLUE_GREY_800, # Dark color, consistent with title
                size=22,
                font_family="Cairo",
                weight=ft.FontWeight.BOLD,
                text_align=ft.TextAlign.CENTER,
            ),
            padding=ft.padding.only(top=5, bottom=5),
        )


class PatientInfo(ft.View):
    def __init__(self):
        super().__init__(
            route="/PatientInfo",
            padding=ft.padding.all(20),
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            vertical_alignment=ft.MainAxisAlignment.CENTER,
            bgcolor=BG_COLOR,
        )

        self.page_title = self._create_page_title()
        self.patient_name = self._create_text_field("اسم المريض", "أدخل اسم المريض هنا")
        self.patient_age = self._create_text_field(
            "العمر", "أدخل العمر هنا", ft.KeyboardType.NUMBER
        )
        self.patient_gender = self._create_dropdown("الجنس", ["ذكر", "أنثى"])
        self.submit_button = self._create_elevated_button("إرسال", self.predict_disease)
        self.input_card = self._create_input_card()
        self.controls = [self.input_card]

    def _create_rounded_container(self, content, width=None, height=None, bgcolor=None, border_radius=15, padding=10, alignment=ft.alignment.center):
      """Creates a container with rounded corners (within the class)."""
      return ft.Container(
          content=content,
          width=width,
          height=height,
          bgcolor=bgcolor,
          border_radius=ft.border_radius.all(border_radius),
          padding=padding,
          alignment=alignment
      )

    def _create_page_title(self):
        return ft.Text(
            value="معلومات المريض",
            size=30,
            weight=ft.FontWeight.BOLD,
            color=SECONDARY_COLOR,
        )

    def _create_text_field(self, label: str, hint: str, keyboard_type: ft.KeyboardType = None, width=300, height=55) -> ft.TextField:
        return ft.TextField(
            label=label,
            hint_text=hint,
            border_color=SECONDARY_COLOR,
            width=width,
            height=height,
            border_radius=ft.border_radius.all(10),
            keyboard_type=keyboard_type,
        )

    def _create_dropdown(self, label: str, options: list[str], width=300, height=55) -> ft.Dropdown:
        return ft.Dropdown(
            options=[ft.dropdown.Option(option) for option in options],
            label=label,
            width=width,
            height=height,
            border_color=SECONDARY_COLOR,
            border_radius=ft.border_radius.all(10),
        )

    def _create_elevated_button(self, text: str, on_click_handler, width=250, height=50) -> ft.ElevatedButton:
        return ft.ElevatedButton(
            content=ft.Text(
                value=text,
                color=ft.colors.WHITE,
                size=18,
                weight=ft.FontWeight.W_500,
            ),
            width=width,
            height=height,
            style=ft.ButtonStyle(
                bgcolor={
                    ft.ControlState.DEFAULT: SECONDARY_COLOR,
                    ft.ControlState.HOVERED: BUTTON_HOVER_COLOR,
                },
                shape=ft.RoundedRectangleBorder(radius=10),
                elevation={
                    ft.ControlState.DEFAULT: 3,
                    ft.ControlState.HOVERED: 6,
                },
            ),
            on_click=on_click_handler,
        )

    def _create_input_card(self):
      return ft.Card(
          elevation=8,
          color=ft.colors.WHITE,
          surface_tint_color=ft.colors.WHITE,
          content=self._create_rounded_container(
              content=ft.Column(
                  [
                      self.page_title,
                      self.patient_name,
                      self.patient_age,
                      self.patient_gender,
                      ft.Container(height=20),
                      self.submit_button,
                  ],
                  spacing=18,
                  alignment=ft.MainAxisAlignment.CENTER,
                  horizontal_alignment=ft.CrossAxisAlignment.CENTER,
              ),
              width=350,
              padding=ft.padding.all(25),
              bgcolor=ft.colors.WHITE,
              border_radius=20,
          ),
      )

    def _show_error_dialog(self, message: str):
        dlg = ft.AlertDialog(
            modal=True,
            title=ft.Text("خطأ", color=ERROR_COLOR),
            content=ft.Text(message),
            actions=[ft.TextButton("موافق", on_click=lambda e: self._close_dlg(dlg))],
        )
        self.page.dialog = dlg
        dlg.open = True
        self.page.update()

    def _close_dlg(self, dlg: ft.AlertDialog):
        dlg.open = False
        self.page.update()

    def validate_input(self):
        if not self.patient_name.value:
            return "يرجى إدخال اسم المريض."
        if not self.patient_age.value:
            return "يرجى إدخال العمر."
        try:
            age = int(self.patient_age.value)
            if age <= 0:
                return "العمر يجب أن يكون أكبر من صفر."
        except ValueError:
            return "يرجى إدخال رقم صحيح للعمر."
        if not self.patient_gender.value:
            return "يرجى اختيار الجنس."
        return None

    def predict_disease(self, e):
        error = self.validate_input()
        if error:
            self._show_error_dialog(error)
            return

        self.page.results_data = {
            "patient_name": self.patient_name.value,
            "gender": self.patient_gender.value,
            "age": self.patient_age.value,
        }

        self.page.update()
        self.page.go("/WelcomeScreen")


def main(page: ft.Page):
    page.title = "Medical Diagnosis App"
    page.window_width = 380
    page.window_height = 780
    page.window_top = 50
    page.window_left = 898
    page.window_resizable = False
    page.bgcolor = BG_COLOR


    def route_change(route):
        print(f"Route changing to: {route.route}")
        page.views.clear()
        if page.route == "/PatientInfo" or page.route == "/":
            page.views.append(PatientInfo())
        elif page.route == "/WelcomeScreen":
            if hasattr(page, 'results_data'):
                results_view = WelcomeScreen(page.results_data)
                page.views.append(results_view)
            else:
                print("No results data found")
                page.go("/PatientInfo")
        page.update()


    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop

    page.go(page.route)


if __name__ == "__main__":
    ft.app(target=main)





class SplashFirst(ft.View):
    def __init__(self):
        super().__init__(
            padding=0,
            bgcolor="white"  # تم تغيير لون الخلفية الافتراضي
        )
        
        # إنشاء العنوان
        self.__title = ft.Text(
            value="AI Health Check",
            color=ft.colors.BLACK,  # تغيير لون النص إلى الأسود ليظهر بشكل أفضل
            size=30,
            font_family="Poppins",
            weight=ft.FontWeight.BOLD,
            text_align=ft.TextAlign.CENTER
        )

        # إنشاء حاوية للشعار
        self.__logo = ft.Container(
            content=ft.Image(
                src="assets/ai.jpg",
                width=200,
                height=200,
                fit=ft.ImageFit.CONTAIN,
            ),
            margin=ft.margin.only(top=20, bottom=20),
            alignment=ft.alignment.center
        )

        # إنشاء الحاوية الرئيسية مع التدرج اللوني
        self.__container = ft.Container(
            width=380,
            height=750,
            content=ft.Column(
                controls=[
                    self.__title,
                    self.__logo
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            gradient=ft.LinearGradient(
                begin=ft.alignment.top_center,
                end=ft.alignment.bottom_center,
                colors=[
                    "#87CEEB",  # لون سماوي
                    "#D3D3D3"   # لون رمادي
                ]
            )
        )

        # إعداد موقع النافذة
        self.window_left = 898
        self.window_top = 0.5
        
        self.controls = [self.__container]

    async def did_mount_async(self):
        self.page.window_width = 380
        self.page.window_height = 750
        self.page.window_left = 898
        self.page.window_top = 0.5
        self.page.padding = 0
        self.page.update()


