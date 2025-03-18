
# import flet as ft
# import pathlib
# import google.generativeai as genai
# import google.ai.generativelanguage as glm
# from reportlab.lib import colors
# from reportlab.lib.pagesizes import A4
# from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
# from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
# from reportlab.pdfbase import pdfmetrics
# from reportlab.pdfbase.ttfonts import TTFont
# import arabic_reshaper
# from bidi.algorithm import get_display

#   # Add this to go to the initial route.
# class BottomAppBar(ft.BottomAppBar):
#     def __init__(self):
#         super().__init__()
#         self.height = 60
#         self.bgcolor = "#87CEEB"
#         self.shadow_color = ft.colors.BLACK
#         self.elevation = 7
#         self.padding = ft.padding.only(left=0, right=0, bottom=0, top=8)
#         self.__bottom = ft.Container(
#             height=55,
#             bgcolor=ft.colors.WHITE,
#             border_radius=ft.border_radius.only(top_left=30, top_right=30),
#             content=ft.Row(
#                 alignment=ft.MainAxisAlignment.SPACE_EVENLY,
#                 vertical_alignment=ft.CrossAxisAlignment.CENTER,
#                 controls=[
#                     self.__icon(ft.icons.HOME, True),
#                     self.__icon(ft.icons.EMAIL),
#                     self.__icon(ft.icons.SETTINGS),
#                     self.__icon(ft.icons.PERSON),
#                 ]
#             )

#         )

#         self.content = self.__bottom


#     def __icon(self, name: str, selected: bool = False) -> ft.IconButton:
#         return ft.IconButton(
#             data=selected,
#             icon=name,
#             icon_color="#87CEEB" if selected else "#C1C1C1",
#             icon_size=40,
#             on_click=self.__clicked
#         )

#     @staticmethod
#     def __clicked(e: ft.ControlEvent) -> None:
#         for i in e.control.parent.controls:
#             i.data = False
#         e.control.data = True
#         e.control.update()
#         for i in e.control.parent.controls:
#             if i.data:
#                 i.icon_color = "#87CEEB"
#             else:
#                 i.icon_color = "#C1C1C1"
#         e.page.update()


# # At the top of your file, *before* any class definitions:



# class MedicalAnalysisApp(ft.View):
#     def __init__(self):
#         super().__init__(
#             route="/MedicalAnalysisApp",
#             bgcolor="#B0E2FF",  # Light blue background
#             padding=0
#         )
        
#         self.image_path = None
#         self.detailed_analysis = None
        
#         try:
#             genai.configure(api_key='AIzaSyDXdDHo2UfbnEjUVkJHshwbIIPetOZr0IQ')
#             self.model_vision = genai.GenerativeModel('gemini-1.5-flash')
#             self.chat_vision = self.model_vision.start_chat(history=[])
#             pdfmetrics.registerFont(TTFont('Arabic', 'Arial.ttf'))
#         except Exception as init_error:
#             print(f"Error initializing: {str(init_error)}")
#             raise

#         self.chat = ft.ListView(
#             expand=True,
#             spacing=15,
#             auto_scroll=True,
#             padding=20,
#         )

#         self.pick_files_dialog = ft.FilePicker(
#             on_result=self.pick_files_result
#         )
#         self.bottom_appbar = BottomAppBar()

#         self.setup_ui()

#     def setup_ui(self):
#         # Header container without top padding/margin
#         self.__header = ft.Container(
#             content=ft.Row(
#                 controls=[
#                     ft.IconButton(
#                         icon=ft.icons.ARROW_BACK,
#                         icon_color="white", # Changed to white
#                         on_click=lambda e: e.page.go("/")
#                     ),
#                     ft.Container(
#                         content=ft.Image(
#                             src="assets/ai.jpg",
#                             width=50,
#                             height=50,
#                         ),
#                         expand=True,
#                         alignment=ft.alignment.center,
#                     ),
#                 ],
#                 alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
#             ),
#             bgcolor="#87CEEB",  # Light blue header background
#             padding=0,  # Remove any padding
#             margin=0, 
#            # Remove any margin
#         )

#         app_header = ft.Container(
#             content=ft.Column([
#                 ft.Text(
#                     "نظام تحليل الفحوصات المختبرية",
#                     size=20,  # Slightly larger
#                     weight="bold",
#                     color="#2c3e50",  # Darker blue
#                     text_align=ft.TextAlign.CENTER
#                 ),
     
#             ], spacing=10),
#             padding=ft.padding.only(bottom=20),  # Remove top padding, keep bottom padding
#             alignment=ft.alignment.center
#         )

#         chat_container = ft.Container(
#             content=self.chat,
#             # border=ft.border.all(1, "#233554"),  # Remove border
#             border_radius=15,
#             padding=10,
#             margin=ft.margin.symmetric(horizontal=20),
#             expand=True,
#             bgcolor="#B0E2FF", # same as background
#         )

#         button_style = ft.ButtonStyle(
#             color="white", # Changed button text color
#             bgcolor="#87CEFA",  # Light blue button background
#             padding=15,
#             animation_duration=300,
#             shape=ft.RoundedRectangleBorder(radius=20), # More rounded corners
#         )

#         buttons = ft.Row(
#             [
#                 ft.ElevatedButton(
#                     "رفع صورة الفحص",
#                     icon=ft.icons.UPLOAD_FILE,
#                     on_click=self.pick_file,
#                     style=button_style
#                 ),
#                 ft.ElevatedButton(
#                     "مسح المحادثة",
#                     icon=ft.icons.CLEAR_ALL,
#                     on_click=self.clear_chat,
#                     style=button_style
#                 ),
#             ],
#             alignment=ft.MainAxisAlignment.CENTER,
#             spacing=20,
#         )

#         button_container = ft.Container(
#             content=buttons,
#             padding=ft.padding.symmetric(vertical=20),
#         )

#         # Main container with no padding/margin at the top
#         self.controls = [
#         self.pick_files_dialog,
#         ft.Container(
#         content=ft.Column(
#             [
#                 self.__header,
#                 app_header,
#                 chat_container,
#                 button_container,
   
#             ],
#             spacing=0,
#             tight=True
#         ),
#         expand=True,
#         padding=0,
#         margin=0,
   
#                 )
#             ]
#         # self.controls = [
#         #     self.pick_files_dialog,
#         #     ft.Container(
#         #         content=ft.Column(
#         #             [
#         #                 self.__header,
#         #                 app_header,
#         #                 chat_container,
#         #                 button_container,
                     
#         #             ],
#         #             spacing=0,  # Remove spacing between elements
#         #             tight=True  # Make the column tight
#         #         ),
#         #         expand=True,
#         #         padding=0,  # Remove padding
#         #         margin=0    # Remove margin
#         #     )
#         # ]
#     async def did_mount_async(self):
#         self.page.pubsub.subscribe(self.on_message)
        
#         self.page.bgcolor = "#B0E2FF" # Same background color
#         self.page.window_width = 360
#         self.page.window_height = 750
#         self.page.window_resizable = False
#         self.page.window.top = 0
#         self.page.window.left = 898
#         self.page.padding = 0
        
#         if self.pick_files_dialog not in self.page.overlay:
#             self.page.overlay.append(self.pick_files_dialog)
            
#         await self.page.update_async()

#     def pick_files_result(self, e: ft.FilePickerResultEvent):
#         if e.files:
#             try:
#                 self.image_path = e.files[0].path
#                 self.add_message("Me", self.image_path, is_image=True)
                
#                 summary = self.analyze_image()
#                 if summary:
#                     result_container = self.create_result_container(summary)
#                     self.add_message("AI", result_container)

#             except Exception as error:
#                 self.add_message("AI", f"خطأ في تحليل الصورة: {str(error)}")

#     def add_message(self, user_name: str, content, is_image: bool = False):
#         message = self.create_chat_message(user_name, content, is_image)
#         self.chat.controls.append(message)
#         self.page.update()

#     def create_chat_message(self, user_name: str, content, is_image: bool = False):
#         avatar_color = "#ADD8E6" if user_name == "Me" else "#87CEFA"  # Lighter blues for avatars
        
#         avatar = ft.CircleAvatar(
#             content=ft.Text(
#                 user_name[:1].capitalize(),
#                 size=16,
#                 weight="bold"
#             ),
#             color="white", # White text
#             bgcolor=avatar_color,
#             radius=20,
#         )

#         message_container = ft.Container(
#             bgcolor="#B0E2FF", # Same as background
#             border_radius=12,
#             padding=15,
#             animate=ft.animation.Animation(300, "easeOut"),
#         )

#         if is_image:
#             message_container.content = ft.Column([
#                 ft.Text(user_name, weight="bold", color="#2c3e50"), # Dark blue
#                 ft.Image(
#                     src=content,
#                     width=200,
#                     height=200,
#                     fit=ft.ImageFit.CONTAIN,
#                     border_radius=10,
#                 ),
#             ], tight=True, spacing=8)
#         else:
#             if isinstance(content, ft.Container):
#                 message_container.content = content
#             else:
#                 message_container.content = ft.Column([
#                     ft.Text(user_name, weight="bold", color="#2c3e50"), # Dark blue
#                     ft.Text(
#                         str(content),
#                         selectable=True,
#                         size=14,
#                         color="black", # black text
#                     ),
#                 ], tight=True, spacing=8)

#         return ft.Row(
#             [avatar, ft.Container(content=message_container, expand=True)],
#             vertical_alignment="start",
#             spacing=10,
#         )

#     def analyze_image(self):
#         try:
#             detailed_prompt = """
#             قم بتحليل صورة الفحص المختبري وقدم:
#             1. قراءة القيم المختبرية الموجودة
#             2. تحديد إذا كانت القيم طبيعية أم لا
#             3. شرح مبسط لمعنى هذه النتائج
#             4. أي توصيات عامة بناءً على النتائج 

#             اريد النتيجة باللغة العربية
#             """

#             summary_prompt = """
#             قم بتحليل صورة الفحص المختبري وقدم نتيجة مختصرة جداً (سطر أو سطرين) 
#             تشير فقط إلى وجود أو عدم وجود مشاكل صحية واضحة.

#             اريد النتيجة باللغة العربية
#             """

#             image_data = pathlib.Path(self.image_path).read_bytes()
            
#             detailed_response = self.model_vision.generate_content(
#                 glm.Content(
#                     parts=[
#                         glm.Part(text=detailed_prompt),
#                         glm.Part(
#                             inline_data=glm.Blob(
#                                 mime_type='image/jpeg',
#                                 data=image_data
#                             )
#                         ),
#                     ],
#                 ))
#             self.detailed_analysis = detailed_response.text

#             summary_response = self.model_vision.generate_content(
#                 glm.Content(
#                     parts=[
#                         glm.Part(text=summary_prompt),
#                         glm.Part(
#                             inline_data=glm.Blob(
#                                 mime_type='image/jpeg',
#                                 data=image_data
#                             )
#                         ),
#                     ],
#                 ))

#             return summary_response.text

#         except Exception as e:
#             print(f"Error in analyze_image: {str(e)}")
#             raise

#     def create_result_container(self, summary):
#         return ft.Container(
#             content=ft.Column([
#                 ft.Card(
#                     content=ft.Container(
#                         content=ft.Column([
#                             ft.Text(
#                                 "النتيجة المختصرة:",
#                                 size=18,
#                                 weight=ft.FontWeight.BOLD,
#                                 color="#2c3e50", # Darker blue
#                             ),
#                             ft.Container(
#                                 content=ft.Text(
#                                     summary,
#                                     size=16,
#                                     color="black", # Black text
#                                 ),
#                                 padding=ft.padding.symmetric(vertical=10),
#                             ),
#                             ft.ElevatedButton(
#                                 "تحميل التقرير الكامل",
#                                 on_click=self.download_report,
#                                 style=ft.ButtonStyle(
#                                     bgcolor="#87CEFA",  # Light blue button
#                                     color="white",       # White text
#                                     padding=15,
#                                     shape=ft.RoundedRectangleBorder(radius=20), # rounded corner
#                                 )
#                             )
#                         ]),
#                         padding=20,
#                     ),
#                     color="#B0E2FF", # Same as main background
#                 ),
#             ]),
#             padding=10,
#         )

#     def create_pdf_report(self, detailed_analysis, filename="medical2_report.pdf"):
#         doc = SimpleDocTemplate(
#             filename,
#             pagesize=A4,
#             rightMargin=72,
#             leftMargin=72,
#             topMargin=72,
#             bottomMargin=72
#         )
        
#         styles = getSampleStyleSheet()
#         arabic_style = ParagraphStyle(
#             'Arabic',
#             fontName='Arabic',
#             fontSize=14,
#             leading=16,
#             alignment=1
#         )

#         content = []
#         title_text = get_display(arabic_reshaper.reshape("تقرير التحليل المخبري"))
#         content.append(Paragraph(title_text, arabic_style))
#         content.append(Spacer(1, 12))
        
#         analysis_text = get_display(arabic_reshaper.reshape(detailed_analysis))
#         content.append(Paragraph(analysis_text, arabic_style))
        
#         doc.build(content)
#         return filename

#     def download_report(self, e):
#         if self.detailed_analysis:
#             try:
#                 report_path = self.create_pdf_report(self.detailed_analysis)
#                 self.add_message("AI", "تم إنشاء التقرير بنجاح! يمكنك العثور عليه في: " + report_path)
#             except Exception as err:
#                 self.add_message("AI", f"حدث خطأ أثناء إنشاء التقرير: {str(err)}")

#     def pick_file(self, e):
#         self.pick_files_dialog.pick_files(allowed_extensions=["png", "jpg", "jpeg"])

#     def clear_chat(self, e):
#         self.chat.controls.clear()
#         self.page.update()

#     def on_message(self, message):
#         if hasattr(message, 'user_name') and hasattr(message, 'text'):
#             self.add_message(message.user_name, message.text, 
#                            is_image=getattr(message, 'is_image', False))
# def main():
#     app = MedicalAnalysisApp()
#     ft.app(target=lambda page: page.go(app.route))

# if __name__ == "__main__":
#     main()









import flet as ft
import pathlib
import google.generativeai as genai
import google.ai.generativelanguage as glm
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import arabic_reshaper
from bidi.algorithm import get_display


class MedicalAnalysisApp(ft.View):
    def __init__(self):
        super().__init__(
            route="/MedicalAnalysisApp",
            bgcolor="#E6F3F3",  # Consistent background color
            padding=0
        )

        self.image_path = None
        self.detailed_analysis = None

        try:
            genai.configure(api_key='AIzaSyDXdDHo2UfbnEjUVkJHshwbIIPetOZr0IQ')  # Replace with your API key
            self.model_vision = genai.GenerativeModel('gemini-1.5-flash')  # Or your preferred model
            self.chat_vision = self.model_vision.start_chat(history=[])
            pdfmetrics.registerFont(TTFont('Arabic', 'Arial.ttf'))  # Or your preferred Arabic font
        except Exception as init_error:
            print(f"Error initializing: {str(init_error)}")
            raise

        self.chat = ft.ListView(
            expand=True,
            spacing=10,  # Reduced spacing
            auto_scroll=True,
            padding=ft.padding.all(15), # Consistent padding
        )

        self.pick_files_dialog = ft.FilePicker(
            on_result=self.pick_files_result
        )

        self.setup_ui()

    def setup_ui(self):
        # --- Header ---
        self.__header = ft.Container(
            content=ft.Row(
                controls=[
                    ft.IconButton(
                        icon=ft.icons.ARROW_BACK,
                        icon_color="#004AAD",  # Dark blue
                        on_click=lambda e: e.page.go("/")  # Or appropriate back route
                    ),
                    ft.Text(
                        "تحليل الفحوصات",
                        size=20,
                        weight=ft.FontWeight.BOLD,
                        color="#004AAD",
                        font_family="Cairo", # Consistent font
                    ),
                    # Placeholder to center the title (using expanded container)
                    ft.Container(expand=True)
                ],
                alignment=ft.MainAxisAlignment.START,  # Align to start
            ),
            bgcolor="#87CEEB",  # Light blue
            padding=ft.padding.symmetric(vertical=10),  # Vertical padding only
            height=70,
            alignment=ft.alignment.center, # Center-align content
        )

        # --- Chat container ---
        chat_container = ft.Container(
            content=self.chat,
            border_radius=15,
            padding=0,  # Padding handled by chat itself
            margin=ft.margin.symmetric(horizontal=20),
            expand=True,
            bgcolor="#FFFFFF", # White background for the chat
            # Optional subtle shadow
            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=5,
                color=ft.colors.GREY_300,
                offset=ft.Offset(0, 2),
            )
        )

        # --- Buttons ---
        button_style = ft.ButtonStyle(
            color="#FFFFFF",  # White text
            bgcolor={
                ft.MaterialState.DEFAULT: "#007BFF",  # Blue
                ft.MaterialState.HOVERED: "#0056b3",   # Darker blue on hover
            },
            padding=ft.padding.all(12), # Consistent padding
            animation_duration=300,
            shape=ft.RoundedRectangleBorder(radius=10), # Rounded corners
            elevation={ # Shadow
                ft.MaterialState.DEFAULT: 2,
                ft.MaterialState.HOVERED: 4
            }
        )

        buttons = ft.Row(
            [
                ft.ElevatedButton(
                    "رفع صورة الفحص",
                    icon=ft.icons.UPLOAD_FILE,
                    on_click=self.pick_file,
                    style=button_style
                ),
                ft.ElevatedButton(
                    "مسح المحادثة",
                    icon=ft.icons.CLEAR_ALL,
                    on_click=self.clear_chat,
                    style=button_style
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=15,  # Consistent spacing
        )

        button_container = ft.Container(
            content=buttons,
            padding=ft.padding.symmetric(vertical=15),  # Vertical padding only
        )


        # --- Main layout ---
        self.controls = [
            self.pick_files_dialog,  # For file picking
            ft.Column(
                [
                    self.__header,
                    # app_header,  <-- Removed, title is now in header
                    chat_container,
                    button_container,
                ],
                spacing=0,  # Remove spacing between major sections
                expand=True,  # Expand to fill the screen
                # tight=True  <-- Not needed with expand=True
            )
        ]

    async def did_mount_async(self):
        self.page.pubsub.subscribe(self.on_message)
        self.page.bgcolor = "#E6F3F3"
        self.page.window_width = 360
        self.page.window_height = 750
        self.page.window_resizable = False
        self.page.window.top = 0
        self.page.window.left = 898
        self.page.padding = 0
        if self.pick_files_dialog not in self.page.overlay:
             self.page.overlay.append(self.pick_files_dialog)
        await self.page.update_async()

    def pick_files_result(self, e: ft.FilePickerResultEvent):
      if e.files:
        try:
            self.image_path = e.files[0].path
            self.add_message("Me", self.image_path, is_image=True)
            summary = self.analyze_image() # Get the summary
            if summary:
                result_container = self.create_result_container(summary)
                self.add_message("AI", result_container) # Display the summary

        except Exception as error:
             self.add_message("AI", f"خطأ في تحليل الصورة: {str(error)}")
             print(f"Error in pick_files_result: {str(error)}") # For debugging


    def add_message(self, user_name: str, content, is_image: bool = False):
        message = self.create_chat_message(user_name, content, is_image)
        self.chat.controls.append(message)
        self.page.update()

    def create_chat_message(self, user_name: str, content, is_image: bool = False):
        avatar_color = "#87CEEB" if user_name == "Me" else "#007BFF"  # Distinct colors
        avatar = ft.CircleAvatar(
            content=ft.Text(
                user_name[:1].capitalize(),
                size=14,
                weight="bold"
            ),
            color="white",
            bgcolor=avatar_color,
            radius=18,  # Slightly smaller avatar
        )

        message_container = ft.Container(
            bgcolor="#FFFFFF", # White message background
            border_radius=10,  # Rounded corners
            padding=ft.padding.all(10),  # Consistent padding
            # animate=ft.animation.Animation(300, "easeOut"), # Optional animation
        )

        if is_image:
            message_container.content = ft.Column([
                ft.Text(user_name, weight="bold", color="#004AAD"),
                ft.Image(
                    src=content,
                    width=250,  # Larger image display
                    height=250,
                    fit=ft.ImageFit.CONTAIN,
                    border_radius=8, # Rounded image corners
                ),
            ], tight=True, spacing=5)
        else:
            if isinstance(content, ft.Container):
                message_container.content = content  # If it's already a container, use it directly
            else:
                message_container.content = ft.Column([
                    ft.Text(user_name, weight="bold", color="#004AAD"),
                    ft.Text(
                        str(content),
                        selectable=True,
                        size=14,
                        color="black",
                    ),
                ], tight=True, spacing=5)


        return ft.Row(
            [avatar, ft.Container(content=message_container, expand=True)],
            vertical_alignment=ft.CrossAxisAlignment.START,  # Align to top
            spacing=8,  # Reduced spacing
        )

    def analyze_image(self):
        try:
            detailed_prompt = """
            قم بتحليل صورة الفحص المختبري وقدم:
            1. قراءة القيم المختبرية الموجودة
            2. تحديد إذا كانت القيم طبيعية أم لا
            3. شرح مبسط لمعنى هذه النتائج
            4. أي توصيات عامة بناءً على النتائج 

            اريد النتيجة باللغة العربية
            """

            summary_prompt = """
            قم بتحليل صورة الفحص المختبري وقدم نتيجة مختصرة جداً (سطر أو سطرين) 
            تشير فقط إلى وجود أو عدم وجود مشاكل صحية واضحة.

            اريد النتيجة باللغة العربية
            """
            image_data = pathlib.Path(self.image_path).read_bytes()
            
            detailed_response = self.model_vision.generate_content(
                glm.Content(
                    parts=[
                        glm.Part(text=detailed_prompt),
                        glm.Part(
                            inline_data=glm.Blob(
                                mime_type='image/jpeg',
                                data=image_data
                            )
                        ),
                    ],
                ))
            self.detailed_analysis = detailed_response.text

            summary_response = self.model_vision.generate_content(
                glm.Content(
                    parts=[
                        glm.Part(text=summary_prompt),
                        glm.Part(
                            inline_data=glm.Blob(
                                mime_type='image/jpeg',
                                data=image_data
                            )
                        ),
                    ],
                ))

            return summary_response.text

        except Exception as e:
            print(f"Error in analyze_image: {str(e)}")
            # Don't raise here, return an error message instead
            return "حدث خطأ أثناء تحليل الصورة.  يرجى المحاولة مرة أخرى."

    def create_result_container(self, summary):
      return ft.Container(
        content=ft.Column([
            ft.Card(
                content=ft.Container(
                    content=ft.Column([
                        ft.Text(
                            "النتيجة المختصرة:",
                            size=16,  # Consistent size
                            weight=ft.FontWeight.BOLD,
                            color="#004AAD",
                        ),
                        ft.Container(
                            content=ft.Text(
                                summary,
                                size=14,
                                color="black",
                            ),
                            padding=ft.padding.symmetric(vertical=8), # Reduced padding
                        ),
                        ft.ElevatedButton( # Button inside the card
                            "تحميل التقرير الكامل",
                            on_click=self.download_report,
                            style=ft.ButtonStyle(
                                bgcolor="#007BFF",
                                color="white",
                                padding=ft.padding.all(10), # Consistent padding
                                shape=ft.RoundedRectangleBorder(radius=8)
                            )
                        )
                    ]),
                    padding=ft.padding.all(15), # Consistent padding
                ),
               color="white", # White card background
                elevation=3,  # Subtle elevation

            ),
        ]),
        padding=ft.padding.only(top=10, bottom=10, left=20, right=20),  # Consistent padding
      )

    def create_pdf_report(self, detailed_analysis, filename="medical2_report.pdf"):
        doc = SimpleDocTemplate(
            filename,
            pagesize=A4,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=72
        )

        styles = getSampleStyleSheet()
        # Use a ParagraphStyle that supports Arabic and set alignment to right
        arabic_style = ParagraphStyle(
            'Arabic',
            fontName='Arabic',  # Make sure 'Arabic' font is registered
            fontSize=14,
            leading=20,  # Adjust leading as needed
            alignment=4,  # TA_JUSTIFY (4) for justified text
            rightIndent=20,
            leftIndent=20,
        )

        content = []
        # Reshape and display text for proper Arabic rendering
        title_text = get_display(arabic_reshaper.reshape("تقرير التحليل المخبري"))
        content.append(Paragraph(title_text, arabic_style))
        content.append(Spacer(1, 12))

        analysis_text = get_display(arabic_reshaper.reshape(detailed_analysis))
        content.append(Paragraph(analysis_text, arabic_style))

        doc.build(content)
        return filename

    def download_report(self, e):
        if self.detailed_analysis:
            try:
                report_path = self.create_pdf_report(self.detailed_analysis)
                self.add_message("AI", "تم إنشاء التقرير بنجاح! يمكنك العثور عليه في: " + report_path)
            except Exception as err:
                self.add_message("AI", f"حدث خطأ أثناء إنشاء التقرير: {str(err)}")
                print(f"Error in download_report: {str(err)}") # For debugging


    def pick_file(self, e):
        self.pick_files_dialog.pick_files(allowed_extensions=["png", "jpg", "jpeg"])

    def clear_chat(self, e):
        self.chat.controls.clear()
        self.page.update()

    def on_message(self, message):
        if hasattr(message, 'user_name') and hasattr(message, 'text'):
            self.add_message(message.user_name, message.text,
                           is_image=getattr(message, 'is_image', False))

def main():
    app = MedicalAnalysisApp()
    ft.app(target=lambda page: page.go(app.route))

if __name__ == "__main__":
    main()
