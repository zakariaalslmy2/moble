
import flet as ft
import numpy as np
import pandas as pd
import pickle
from fuzzywuzzy import process
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import flet as ft
import google.generativeai as genai
import google.ai.generativelanguage as glm
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from bidi.algorithm import get_display
from arabic_paragraph import ArabicParagraph 
sym_des = pd.read_csv("symtoms_df.csv")
precautions = pd.read_csv("p.csv")
workout = pd.read_csv("w.csv")
description = pd.read_csv("des.csv")
medications = pd.read_csv('med.csv')
diets = pd.read_csv("d.csv")
test_lap = pd.read_csv("test_lap.csv") 
svc = pickle.load(open('svc.pkl', 'rb'))


def helper(dis):
    desc = description[description['Disease'] == dis]['Description'].iloc[0]
    pre = [str(p) for p in precautions[precautions['Disease'] == dis][
        ['Precaution_1', 'Precaution_2', 'Precaution_3', 'Precaution_4']].values.tolist()[0]]
    med = [str(m) for m in medications[medications['Disease'] == dis]['Medication'].values.tolist()]
    die = [str(d) for d in diets[diets['Disease'] == dis]['Diet'].values.tolist()]
    wrkout = [str(w) for w in workout[workout['disease'] == dis]['workout'].values.tolist()]
    # إضافة استرجاع الفحوصات
    tests = test_lap[test_lap['Disease'] == dis]['test_lap'].iloc[0] if not test_lap[test_lap['Disease'] == dis].empty else "لا توجد فحوصات محددة"

    return desc, pre, med, die, wrkout, tests 
# تقيؤ رجفة حمى مرتفعة تعرق صداع غثيان إسهال ألم في العضلات  مرض الملاريا
# طفح جلدي رجفة ألم المفاصل تقيؤ تعب حمى مرتفعة صداع غثيان حمئ الضنك 
# مرض الربؤ تعب سعالحمى مرتفعة ضيق التنفس
# مرض قرحة المعدة تقيؤ عسر الهضمفقدان الشهية ألم في البطن انتفاخ البطن حكة داخلية
# مرض جلطة دماغية او الشلل  تقيؤ صداع ضعف في جانب واحد من الجسم تغير في الوعي

symptoms_dict = {

    'itching': 0, 'حكة': 0,
    'skin_rash': 1, 'طفح جلدي': 1,
    'nodal_skin_eruptions': 2, 'نتوءات جلدية عقدية': 2,
    'continuous_sneezing': 3, 'عطس مستمر': 3,
    'shivering': 4, 'قشعريرة': 4,
    'chills': 5, 'رجفة': 5, 
    'joint_pain': 6, 'ألم المفاصل': 6,
    'stomach_pain': 7, 'ألم في المعدة': 7,
    'acidity': 8, 'حموضة': 8,
    'ulcers_on_tongue': 9, 'تقرحات على اللسان': 9,
    'muscle_wasting': 10, 'ضمور العضلات': 10,
    'vomiting': 11, 'تقيؤ  طرش': 11,
    'burning_micturition': 12, 'حرقة أثناء التبول': 12,
    'spotting_ urination': 13, 'تبول متقطع': 13,
    'fatigue': 14, 'تعب': 14,
    'weight_gain': 15, 'زيادة الوزن': 15,
    'anxiety': 16, 'قلق': 16,
    'cold_hands_and_feets': 17, 'برودة اليدين والقدمين': 17,
    'mood_swings': 18, 'تقلبات المزاج': 18,
    'weight_loss': 19, 'فقدان الوزن': 19,
    'restlessness': 20, 'تململ': 20,
    'lethargy': 21, 'خمول': 21,
    'patches_in_throat': 22, 'بقع في الحلق': 22,
    'irregular_sugar_level': 23, 'مستوى سكر غير منتظم': 23,
    'cough': 24, ' سعلة سعال': 24,
    'high_fever': 25, 'حمى مرتفعة': 25,
    'sunken_eyes': 26, 'عيون غائرة': 26,
    'breathlessness': 27, 'ضيق التنفس': 27,
    'sweating': 28, 'تعرق': 28,
    'dehydration': 29, 'جفاف': 29,
    'indigestion': 30, 'عسر الهضم': 30,
    'headache': 31, ' زكام صداع': 31,
    'yellowish_skin': 32, 'جلد مصفر': 32,
    'dark_urine': 33, 'بول داكن': 33,
    'nausea': 34, 'غثيان': 34,
    'loss_of_appetite': 35, 'فقدان الشهية': 35,
    'pain_behind_the_eyes': 36, 'ألم خلف العينين': 36,
    'back_pain': 37, 'ألم الظهر': 37,
    'constipation': 38, 'إمساك': 38,
    'abdominal_pain': 39, 'ألم في البطن': 39,
    'diarrhoea': 40, 'إسهال': 40,
    'mild_fever': 41, 'حمى خفيفة': 41,
    'yellow_urine': 42, 'بول أصفر': 42,
    'yellowing_of_eyes': 43, 'اصفرار العينين': 43,
    'acute_liver_failure': 44, 'فشل كبدي حاد': 44,
    'fluid_overload': 45, 'زيادة السوائل': 45,
    'swelling_of_stomach': 46, 'انتفاخ المعدة': 46,
    'swelled_lymph_nodes': 47, 'تورم الغدد الليمفاوية': 47,
    'malaise': 48, 'توعك': 48,
    'blurred_and_distorted_vision': 49, 'رؤية مشوشة ومشوهة': 49,
    'phlegm': 50, 'بلغم': 50,
    'throat_irritation': 51, 'تهيج الحلق': 51,
    'redness_of_eyes': 52, 'احمرار العينين': 52,
    'sinus_pressure': 53, 'ضغط الجيوب الأنفية': 53,
    'runny_nose': 54, 'سيلان الأنف': 54,
    'congestion': 55, 'احتقان': 55,
    'chest_pain': 56, 'ألم في الصدر': 56,
    'weakness_in_limbs': 57, 'ضعف في الأطراف': 57,
    'fast_heart_rate': 58, 'سرعة ضربات القلب': 58,
    'pain_during_bowel_movements': 59, 'ألم أثناء التبرز': 59,
    'pain_in_anal_region': 60, 'ألم في منطقة الشرج': 60,
    'bloody_stool': 61, 'براز دموي': 61,
    'irritation_in_anus': 62, 'تهيج في الشرج': 62,
    'neck_pain': 63, 'ألم الرقبة': 63,
    'dizziness': 64, 'دوخة': 64,
    'cramps': 65, 'تقلصات': 65,
    'bruising': 66, 'كدمات': 66,
    'obesity': 67, 'سمنة': 67,
    'swollen_legs': 68, 'ساقين متورمتين': 68,
    'swollen_blood_vessels': 69, 'أوعية دموية منتفخة': 69,
    'puffy_face_and_eyes': 70, 'وجه وعيون منتفخة': 70,
    'enlarged_thyroid': 71, 'تضخم الغدة الدرقية': 71,
    'brittle_nails': 72, 'أظافر هشة': 72,
    'swollen_extremeties': 73, 'أطراف متورمة': 73,
    'excessive_hunger': 74, 'جوع مفرط': 74,
    'extra_marital_contacts': 75, 'علاقات خارج الزواج': 75,
    'drying_and_tingling_lips': 76, 'جفاف ووخز الشفاه': 76,
    'slurred_speech': 77, 'تأتأة': 77,
    'knee_pain': 78, 'ألم الركبة': 78,
    'hip_joint_pain': 79, 'ألم مفصل الورك': 79,
    'muscle_weakness': 80, 'ضعف العضلات': 80,
    'stiff_neck': 81, 'تصلب الرقبة': 81,
    'swelling_joints': 82, 'تورم المفاصل': 82,
    'movement_stiffness': 83, 'تصلب الحركة': 83,
    'spinning_movements': 84, 'حركات دورانية': 84,
    'loss_of_balance': 85, 'فقدان التوازن': 85,
    'unsteadiness': 86, 'تذبذب': 86,
    'weakness_of_one_body_side': 87, 'ضعف في جانب واحد من الجسم': 87,
    'loss_of_smell': 88, 'فقدان الشم': 88,
    'bladder_discomfort': 89, 'انزعاج المثانة': 89,
    'foul_smell_of urine': 90, 'رائحة بول كريهة': 90,
    'continuous_feel_of_urine': 91, 'الشعور المستمر بالتبول': 91,
    'passage_of_gases': 92, 'انتفاخ البطن': 92,
    'internal_itching': 93, 'حكة داخلية': 93,
    'toxic_look_(typhos)': 94, 'مظهر سام (تيفوس)': 94,
    'depression': 95, 'اكتئاب': 95,
    'irritability': 96, 'تهيج': 96,
    'muscle_pain': 97, 'ألم في العضلات': 97,
    'altered_sensorium': 98, 'تغير في الوعي': 98,
    'red_spots_over_body': 99, 'بقع حمراء على الجسم': 99,
    'belly_pain': 100, 'ألم في البطن': 100,
    'abnormal_menstruation': 101, 'دورة شهرية غير طبيعية': 101,
    'dischromic_patches': 102, 'بقع متغيرة اللون': 102,
    'watering_from_eyes': 103, 'دموع من العين': 103,
    'increased_appetite': 104, 'زيادة الشهية': 104,
    'polyuria': 105, 'تبول مفرط': 105,
    'family_history': 106, 'تاريخ عائلي': 106,
    'mucoid_sputum': 107, 'بلغم مخاطي': 107,
    'rusty_sputum': 108, 'بلغم صدئ': 108,
    'lack_of_concentration': 109, 'قلة التركيز': 109,
    'visual_disturbances': 110, 'اضطرابات بصرية': 110,
    'receiving_blood_transfusion': 111, 'تلقي نقل دم': 111,
    'receiving_unsterile_injections': 112, 'تلقي حقن غير معقمة': 112,
    'coma': 113, 'غيبوبة': 113,
    'stomach_bleeding': 114, 'نزيف في المعدة': 114,
    'distention_of_abdomen': 115, 'انتفاخ البطن': 115,
    'history_of_alcohol_consumption': 116, 'تاريخ تعاطي الكحول': 116,
    'fluid_overload.1': 117, # قد تحتاج إلى معالجة هذه التسمية المكررة
    'blood_in_sputum': 118, 'دم في البلغم': 118,
    'prominent_veins_on_calf': 119, 'أوردة بارزة في ربلة الساق': 119,
    'palpitations': 120, 'خفقان': 120,
    'painful_walking': 121, 'مشي مؤلم': 121,
    'pus_filled_pimples': 122, 'بثور مليئة بالصديد': 122,
    'blackheads': 123, 'رؤوس سوداء': 123,
    'scurring': 124, 'تقشر': 124,
    'skin_peeling': 125, 'تقشير الجلد': 125,
    'silver_like_dusting': 126, 'غبار فضي': 126,
    'small_dents_in_nails': 127, 'نقر صغير في الأظافر': 127,
    'inflammatory_nails': 128, 'التهاب الأظافر': 128,
    'blister': 129, 'بثور': 129,
    'red_sore_around_nose': 130, 'تقرحات حمراء حول الأنف': 130,
    'yellow_crust_ooze': 131, 'إفرازات صفراء متقشرة': 131,
    'حرقان أثناء التبول': 12, # إضافة النسخة العربية
    'تبول متقطع': 13, # إضافة النسخة العربية
    'الم في المعدة': 7 # إضافة النسخة العربية
}
# diseases_list = {15: 'Fungal infection', 4: 'Allergy', 16: 'GERD', 9: 'Chronic cholestasis', 14: 'Drug Reaction', 33: 'Peptic ulcer diseae', 1: 'AIDS', 12: 'Diabetes ', 17: 'Gastroenteritis', 6: 'Bronchial Asthma', 23: 'Hypertension ', 30: 'Migraine', 7: 'Cervical spondylosis', 32: 'Paralysis (brain hemorrhage)', 28: 'Jaundice', 29: 'Malaria', 8: 'Chicken pox', 11: 'Dengue', 37: 'Typhoid', 40: 'hepatitis A', 19: 'Hepatitis B', 20: 'Hepatitis C', 21: 'Hepatitis D', 22: 'Hepatitis E', 3: 'Alcoholic hepatitis', 36: 'Tuberculosis', 10: 'Common Cold', 34: 'Pneumonia', 13: 'Dimorphic hemmorhoids(piles)', 18: 'Heart attack', 39: 'Varicose veins', 26: 'Hypothyroidism', 24: 'Hyperthyroidism', 25: 'Hypoglycemia', 31: 'Osteoarthristis', 5: 'Arthritis', 0: '(vertigo) Paroymsal  Positional Vertigo', 2: 'Acne', 38: 'Urinary tract infection', 35: 'Psoriasis', 27: 'Impetigo'}
diseases_list = {
    15: 'عدوى فطرية',
    4: 'حساسية',
    16: 'ارتجاع المريء',
    9: 'ركود الصفراء المزمن',
    14: 'تفاعل دوائي',
    33: 'قرحة المعدة',
    1: 'الإيدز',
    12: 'السكري',
    17: 'التهاب المعدة والأمعاء',
    6: 'الربو الشعبي',
    23: 'ارتفاع ضغط الدم',
    30: 'الصداع النصفي',
    7: 'تآكل الفقرات العنقية',
    32: '  جلطة  (نزيف المخ)',
    28: 'اليرقان',
    29: 'الملاريا',
    8: 'جدري الماء',
    11: 'حمى الضنك',
    37: 'التيفوئيد',
    40: 'التهاب الكبد أ',
    19: 'التهاب الكبد ب',
    20: 'التهاب الكبد ج',
    21: 'التهاب الكبد د',
    22: 'التهاب الكبد ه',
    3: 'التهاب الكبد الكحولي',
    36: 'السل',
    10: 'نزلة البرد',
    34: 'الالتهاب الرئوي',
    13: 'البواسير',
    18: 'النوبة القلبية',
    39: 'الدوالي',
    26: 'قصور الغدة الدرقية',
    24: 'فرط نشاط الغدة الدرقية',
    25: 'نقص سكر الدم',
    31: 'التهاب المفاصل العظمي',
    5: 'التهاب المفاصل',
    0: 'الدوار الوضعي',
    2: 'حب الشباب',
    38: 'التهاب المسالك البولية',
    35: 'الصدفية',
    27: 'القوباء'
}


def get_predicted_value(patient_symptoms):
    try:
        num_unique_symptoms = len(set(symptoms_dict.values()))
        input_vector = np.zeros(num_unique_symptoms)

        for item in patient_symptoms:
            item = item.strip()

            for key, value in symptoms_dict.items():
                if item == key:
                    input_vector[value] = 1
                    break 


        input_vector = input_vector.astype(float)
        prediction = svc.predict([input_vector])[0]
        return diseases_list[prediction]
    except Exception as e:
        raise Exception(f"Prediction failed: {str(e)}")


def suggest_symptoms(user_input):
    english_choices = [key for key in symptoms_dict if isinstance(key, str) and key.isascii()]
    arabic_choices = [key for key in symptoms_dict if isinstance(key, str) and not key.isascii()]

    english_suggestions = process.extract(user_input, english_choices, limit=5)
    arabic_suggestions = process.extract(user_input, arabic_choices, limit=5)

    suggestions = [symptom for symptom, score in english_suggestions] + [symptom for symptom, score in
                                                                         arabic_suggestions]
    return list(set(suggestions))

import flet as ft
import flet as ft
import copy  # Import the copy module

import flet as ft
import flet as ft

class DoctorsView(ft.View):
    def __init__(self):
        super().__init__(
            route="/doctors",
            padding=ft.padding.only(left=0, right=0, bottom=0, top=0),
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            bgcolor="#E6F3F3"  # Consistent background
        )

        # Mock data (replace with your actual data source)
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


        self.__header = ft.Container(
            content=ft.Row(
                controls=[
                    ft.IconButton(
                        icon=ft.icons.ARROW_BACK,
                        icon_color="#000000",
                        on_click=lambda e: e.page.go("/Splash")  # Back to main
                    ),
                   
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
             bgcolor="#87CEEB",  # Consistent header color
             padding=ft.padding.only(top=8)
        )


        self.__title = ft.Text(
            value="الأطباء",
            color=ft.colors.BLACK,
            size=22,
            font_family="Poppins",
            weight=ft.FontWeight.BOLD,
            text_align=ft.TextAlign.CENTER
        )

        self.doctors_list = ft.Column(
            scroll=ft.ScrollMode.AUTO,  # Enable scrolling if needed
            controls=self.create_doctor_cards(),
            spacing=15,
            height=550,  # Set a fixed height for the scrollable area
        )

        self.__content = ft.Container(
            content=ft.Column(
                controls=[
                    self.__title,
                    ft.Divider(height=10, color=ft.colors.GREY_300),
                    self.doctors_list,

                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=15,
            ),
            padding=20,  # Add padding around content
        )

        self.controls = [self.__header, self.__content]


    def create_doctor_cards(self):
        cards = []
        for doctor in self.doctors_data:
            card = ft.Card(
                elevation=4,
                content=ft.Container(
                    content=ft.Column(
                        [
                            ft.ListTile(
                                leading=ft.Icon(ft.icons.PERSON, size=40, color="#87CEEB"),
                                title=ft.Text(doctor["name"], size=18, weight=ft.FontWeight.BOLD),
                                subtitle=ft.Text(doctor["specialty"], size=14, color=ft.colors.GREY_700),
                                trailing= ft.IconButton(ft.icons.PHONE,icon_color="#87CEEB"), #  phone icon
                            ),
                             ft.Row([  # Display phone number under the name/specialty.  Better layout.
                                 # ft.Icon(ft.icons.PHONE, size=16, color=ft.colors.GREY_600), #Removed, it's redundant
                                 ft.Text(doctor["phone"], size=14, color=ft.colors.GREY_600)

                             ],
                             alignment=ft.MainAxisAlignment.CENTER
                            ),
                            ft.Divider(height=1, color=ft.colors.GREY_300), # Add dividers
                            
                        ],
                        spacing=5, # Reduce spacing within the card
                    ),
                    width=320,   # consistent width
                    padding=10,  # consistent padding
                    # bgcolor=ft.colors.WHITE, # Optional:  Make card background white
                    border_radius=ft.border_radius.all(10),  # Rounded corners for the card
                ),
                # margin=ft.margin.only(bottom=10) # Removed, as we're using spacing in Column

            )
            cards.append(card)
        return cards


class Settings(ft.View):
    def __init__(self):
        super().__init__(
            route="/settings",
            padding=ft.padding.only(left=0, right=0, bottom=0, top=0),
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            bgcolor="#E6F3F3"  # Same background as other views
        )
        # Assuming you have a BottomAppBar class (from your previous code)
        # self.bottom_appbar = BottomAppBar(page=self.page)

        self.__header = ft.Container(
            content=ft.Row(
                controls=[
                    ft.IconButton(
                        icon=ft.icons.HOME,
                        icon_color="#000000",
                        on_click=lambda e: e.page.go("/Splash")  
                        # on_click=lambda e: e.page.go("/Splash")  #  Navigation handled in main
                    ),
            
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
            bgcolor="#87CEEB",  # Consistent header color
        )

        self.__title = ft.Text(
            value="الإعدادات",
            color=ft.colors.BLACK,
            size=22,
            font_family="Poppins",  # Consistent font
            weight=ft.FontWeight.BOLD,
            text_align=ft.TextAlign.CENTER
        )

        # --- Example Settings (Design Only) ---

        # Language Selection
        self.language_dropdown = ft.Dropdown(
            options=[
                ft.dropdown.Option("العربية"),
                ft.dropdown.Option("English"),
            ],
            label="اللغة",
            width=200,
            # on_change=self.change_language  #  No event handling
        )

        # Theme Switch
        self.theme_switch = ft.Switch(label="الوضع الداكن", label_position=ft.LabelPosition.LEFT) # No event handling

        # Notifications Switch
        self.notifications_switch = ft.Switch(label="الإشعارات", label_position=ft.LabelPosition.LEFT) # No event handling

        # About and Version (using a Column for better layout)
        self.about = ft.Text("حول التطبيق...")
        self.version = ft.Text("الإصدار 1.0")
        self.about_section = ft.Column([self.about, self.version], alignment=ft.MainAxisAlignment.CENTER)


        # --- Layout ---

        self.__content = ft.Container(
            content=ft.Column(
                controls=[
                    self.__title,
                    ft.Divider(height=20, color=ft.colors.GREY_300), # Visual separation

                    # Language Setting
                    self.language_dropdown,

                    # Theme Setting
                    self.theme_switch,

                    # Notifications Setting
                    self.notifications_switch,

                    ft.Divider(height=20, color=ft.colors.GREY_300), # Visual separation

                    # About Section
                    self.about_section,
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=15, #Consistent spacing
            ),
            padding=20,  #  Padding
           # margin=ft.margin.only(top=20), #removed, no need
        )

        self.controls = [self.__header, self.__content]  # No bottom_appbar here, for demonstration
class ResultsView(ft.View):
    def __init__(self, results_data):
        super().__init__()
        self.route = "/results"
        self.scroll = ft.ScrollMode.ALWAYS
        self.results_data = results_data

        def generate_pdf(e):
            try:
                from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
                from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
                from reportlab.lib.enums import TA_RIGHT
                from reportlab.lib.pagesizes import letter
                import arabic_reshaper
                from bidi.algorithm import get_display
                import os
                from datetime import datetime

                # تحديد مسار حفظ الملف
                documents_path = os.path.expanduser('~/Documents')
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                pdf_path = os.path.join(documents_path, f'medical_report_{timestamp}.pdf')

                # إنشاء مستند PDF
                doc = SimpleDocTemplate(
                    pdf_path,
                    pagesize=letter,
                    rightMargin=20,
                    leftMargin=20,
                    topMargin=20,
                    bottomMargin=20
                )

                # تحضير المحتوى
                story = []

                # تعريف الأنماط
                styles = getSampleStyleSheet()
                
                arabic_style = ParagraphStyle(
                    'CustomArabic',
                    parent=styles['Normal'],
                    fontName='Helvetica',
                    fontSize=12,
                    leading=14,
                    alignment=TA_RIGHT
                )
                
                title_style = ParagraphStyle(
                    'CustomArabicTitle',
                    parent=styles['Title'],
                    fontName='Helvetica-Bold',
                    fontSize=18,
                    leading=22,
                    alignment=TA_RIGHT
                )

                def add_arabic_text(text, is_title=False):
                    # معالجة النص العربي
                    reshaped_text = arabic_reshaper.reshape(str(text))
                    bidi_text = get_display(reshaped_text)
                    
                    if is_title:
                        story.append(Paragraph(bidi_text, title_style))
                        story.append(Spacer(1, 20))
                    else:
                        story.append(Paragraph(bidi_text, arabic_style))
                        story.append(Spacer(1, 10))

                # إضافة العنوان
                add_arabic_text("تقرير التشخيص الطبي", True)

                # إضافة المحتوى
                add_arabic_text(f"المرض المتوقع: {self.results_data['disease']}")
                add_arabic_text(f"الوصف: {self.results_data['description']}")
                add_arabic_text(f"الأعراض: {', '.join(self.results_data['symptoms'])}")
                add_arabic_text(f"الاحتياطات: {', '.join(self.results_data['precautions'])}")
                add_arabic_text(f"الأدوية: {', '.join(self.results_data['medications'])}")
                add_arabic_text(f"النظام الغذائي: {', '.join(self.results_data['diet'])}")
                add_arabic_text(f"التمارين: {', '.join(self.results_data['workout'])}")
                add_arabic_text(f"الفحوصات المختبرية اللازمة: {self.results_data['tests']}")
                
                # إضافة التاريخ والوقت
                add_arabic_text(f"تاريخ التقرير: {datetime.now().strftime('%Y-%m-%d %H:%M')}")

                # بناء ملف PDF
                doc.build(story)

                # عرض رسالة نجاح
                self.page.show_snack_bar(
                    ft.SnackBar(
                        content=ft.Text(f"تم حفظ التقرير في المستندات: medical_report_{timestamp}.pdf"),
                        action="حسناً"
                    )
                )

            except Exception as e:
                print(f"Error generating PDF: {str(e)}")
                self.page.show_snack_bar(
                    ft.SnackBar(
                        content=ft.Text(f"حدث خطأ أثناء إنشاء التقرير: {str(e)}"),
                        action="حسناً"
                    )
                )

        self.controls = [
            ft.AppBar(
                leading=ft.IconButton(
                    icon=ft.icons.ARROW_BACK,
                    on_click=lambda _: self.page.go("/Splash")
                ),
                title=ft.Text("نتائج التشخيص"),
                bgcolor="#87CEEB",
                center_title=True
            ),
            ft.Container(
                content=ft.Column(
                    scroll=ft.ScrollMode.ALWAYS,
                    controls=[
                        ft.Card(
                            content=ft.Container(
                                content=ft.ListTile(
                                    leading=ft.Icon(ft.icons.MEDICAL_SERVICES, color="#87CEEB"),
                                    title=ft.Text("المرض المتوقع", style=ft.TextStyle(weight=ft.FontWeight.BOLD)),
                                    subtitle=ft.Text(results_data['disease'])
                                ),
                                padding=10
                            )
                        ),
                        ft.Card(
                            content=ft.Container(
                                content=ft.ListTile(
                                    leading=ft.Icon(ft.icons.DESCRIPTION, color="#87CEEB"),
                                    title=ft.Text("الوصف", style=ft.TextStyle(weight=ft.FontWeight.BOLD)),
                                    subtitle=ft.Text(results_data['description'])
                                ),
                                padding=10
                            )
                        ),
                        ft.Card(
                            content=ft.Container(
                                content=ft.ListTile(
                                    leading=ft.Icon(ft.icons.HEALING, color="#87CEEB"),
                                    title=ft.Text("الأعراض", style=ft.TextStyle(weight=ft.FontWeight.BOLD)),
                                    subtitle=ft.Text(", ".join(results_data['symptoms']))
                                ),
                                padding=10
                            )
                        ),
                        ft.Card(
                            content=ft.Container(
                                content=ft.ListTile(
                                    leading=ft.Icon(ft.icons.WARNING, color="#87CEEB"),
                                    title=ft.Text("الاحتياطات", style=ft.TextStyle(weight=ft.FontWeight.BOLD)),
                                    subtitle=ft.Text(", ".join(results_data['precautions']))
                                ),
                                padding=10
                            )
                        ),
                        ft.Card(
                            content=ft.Container(
                                content=ft.ListTile(
                                    leading=ft.Icon(ft.icons.MEDICATION, color="#87CEEB"),
                                    title=ft.Text("الأدوية", style=ft.TextStyle(weight=ft.FontWeight.BOLD)),
                                    subtitle=ft.Text(", ".join(results_data['medications']))
                                ),
                                padding=10
                            )
                        ),
                        ft.Card(
                            content=ft.Container(
                                content=ft.ListTile(
                                    leading=ft.Icon(ft.icons.RESTAURANT_MENU, color="#87CEEB"),
                                    title=ft.Text("النظام الغذائي", style=ft.TextStyle(weight=ft.FontWeight.BOLD)),
                                    subtitle=ft.Text(", ".join(results_data['diet']))
                                ),
                                padding=10
                            )
                        ),
                        ft.Card(
                            content=ft.Container(
                                content=ft.ListTile(
                                    leading=ft.Icon(ft.icons.FITNESS_CENTER, color="#87CEEB"),
                                    title=ft.Text("التمارين", style=ft.TextStyle(weight=ft.FontWeight.BOLD)),
                                    subtitle=ft.Text(", ".join(results_data['workout']))
                                ),
                                padding=10
                            )
                        ),
                  ft.Card(
    content=ft.Container(
        content=ft.ListTile(
            leading=ft.Icon(ft.icons.SCIENCE, color="#87CEEB"),  # تم التصحيح
            title=ft.Text("الفحوصات المختبرية اللازمة", style=ft.TextStyle(weight=ft.FontWeight.BOLD)),
            subtitle=ft.Text(results_data['tests'])
        ),
        padding=10
    )
),
                        # زر الطباعة
                        ft.Container(
                            content=ft.ElevatedButton(
                                "طباعة التقرير",
                                icon=ft.icons.PRINT,
                                on_click=generate_pdf,
                                style=ft.ButtonStyle(
                                    color="white",
                                    bgcolor="#87CEEB",
                                ),
                            ),
                            alignment=ft.alignment.center,
                            padding=20,
                        ),
                    ],
                    spacing=10
                ),
                padding=20,
                expand=True
            )
        ]

        # تعيين ارتفاع ثابت للحاوية
        self.height = 600

import flet as ft


class BottomAppBar(ft.BottomAppBar):
    def __init__(self, page: ft.Page):  # Add page as an argument
        super().__init__()
        self.page = page # Store the page instance
        self.height = 60
        self.bgcolor = "#87CEEB"
        self.shadow_color = ft.colors.BLACK
        self.elevation = 7
        self.padding = ft.padding.only(left=0, right=0, bottom=0, top=8)
        self.__bottom = ft.Container(
            height=55,
            bgcolor=ft.colors.WHITE,
            border_radius=ft.border_radius.only(top_left=30, top_right=30),
            content=ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_EVENLY,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    self.__icon(ft.icons.HOME, True, "/Splash"),  # Home icon, selected by default, routes to "/"
                    self.__icon(ft.icons.HEALING, False, "/home"),  # Doctors icon, routes to "/doctors"
                    self.__icon(ft.icons.HEALING, False,"/home2"),
                     self.__icon(ft.icons.VERIFIED_USER, False ,"/doctors"), # #Settings
                    self.__icon(ft.icons.SETTINGS, False ,"/settings"), #Settings
                 
                ]
            )

        )

        self.content = self.__bottom

    def __icon(self, name: str, selected: bool = False, route: str = None) -> ft.IconButton:
        return ft.IconButton(
            data={"selected": selected, "route": route}, # Store selected state and route
            icon=name,
            icon_color="#87CEEB" if selected else "#C1C1C1",
            icon_size=40,
            on_click=self.__clicked,
        )

    def __clicked(self, e: ft.ControlEvent) -> None:
        for i in e.control.parent.controls:
            i.data["selected"] = False  # Deselect all icons
            if i.data["selected"]: # Fix: Check i.data["selected"] instead of i.data
              i.icon_color = "#C1C1C1"

        e.control.data["selected"] = True  # Select the clicked icon
        e.control.icon_color = "#87CEEB"
        e.control.update()

        for i in e.control.parent.controls:
            if i.data["selected"]:
                i.icon_color = "#87CEEB"
            else:
                i.icon_color = "#C1C1C1"
            i.update() #update each icon

        if e.control.data["route"]:  # Check if the icon has a route
            e.page.go(e.control.data["route"])  # Navigate to the specified route
        e.page.update()


class Home(ft.View):
    def __init__(self):
        super().__init__(
            route="/home",
            padding=ft.padding.only(left=0, right=0, bottom=0, top=0),
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            bgcolor="#E6F3F3"
        )
        self.bottom_appbar = BottomAppBar(page=self.page)


        self.__header = ft.Container(
            content=ft.Row(
                controls=[
                    ft.IconButton(
                        icon=ft.icons.ARROW_BACK,
                        icon_color="#000000",
                        on_click=lambda e: e.page.go("/Splash")  # Corrected route
                    ),
                    ft.Container(
                        content=ft.Image(
                            src="assets/ai.jpg",
                            width=50,
                            height=50,
                        ),
                        expand=True,
                        alignment=ft.alignment.center,
                    ),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
            bgcolor="#87CEEB",
        )

        self.__title = ft.Text(
            value="اكتب الاعراض التي تشعر بها",
            color=ft.colors.BLACK,
            size=22,
            font_family="Poppins",
            weight=ft.FontWeight.BOLD,
            text_align=ft.TextAlign.CENTER
        )

        # Store selected symptoms
        self.selected_symptoms = []
        self.selected_symptoms_display = ft.Text("", text_align=ft.TextAlign.RIGHT)

        # Dropdown for suggestions (initially hidden)
        self.suggestions_dropdown = ft.Dropdown(
            options=[],
            visible=False,
            on_change=self.add_selected_symptom,
            width=300,
        )

        self.__search = ft.TextField(
            width=300,
            height=60,
            border_radius=10,
            bgcolor="white",
            border_color="#A0B4C7",
            hint_text="ابحث عن عرض...",
            text_align=ft.TextAlign.RIGHT,
            on_change=self.update_suggestions,
        )

        self.__submit_button = ft.ElevatedButton(
            text="تقديم الاعراض",
            style=ft.ButtonStyle(
                bgcolor="#87CEEB",
                color="black",
                shape=ft.RoundedRectangleBorder(radius=30),
            ),
            on_click=self.predict_disease,
            width=300,
            height=60
        )
        self.error_message = ft.Text("", color=ft.colors.RED)

        self.__content = ft.Container(
            content=ft.Column(
                controls=[
                    self.__title,
                    self.__search,
                    self.suggestions_dropdown,
                    self.selected_symptoms_display,
                    self.__submit_button,
                    self.error_message

                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=15,
            ),
            padding=10,
            margin=ft.margin.only(top=20),
        )

        self.controls = [self.__header, self.__content, self.bottom_appbar]

    def update_suggestions(self, e):
        """Provides suggestions based on user input."""
        user_input = self.__search.value
        if user_input:
            suggestions = suggest_symptoms(user_input)
            self.suggestions_dropdown.options = [
                ft.dropdown.Option(text=s) for s in suggestions
            ]
            self.suggestions_dropdown.visible = True
        else:
            self.suggestions_dropdown.visible = False
            self.suggestions_dropdown.options = []
        self.update()

    def add_selected_symptom(self, e):
        """Adds the selected symptom to the list and updates the display."""
        selected = self.suggestions_dropdown.value
        if selected and selected not in self.selected_symptoms:
            self.selected_symptoms.append(selected)
        self.selected_symptoms_display.value = ", ".join(
            self.selected_symptoms)
        self.__search.value = ""
        self.suggestions_dropdown.visible = False
        self.suggestions_dropdown.value = None
        self.update()

    def predict_disease(self, e):
        try:
            if len(self.selected_symptoms) < 4:
                # استخدام نافذة منبثقة بدلاً من مجرد تغيير نص الخطأ
                self.page.show_dialog(
                    ft.AlertDialog(
                        modal=True,
                        title=ft.Text("عدد الأعراض غير كافٍ"),
                        content=ft.Text("للحصول على نتائج أكثر دقة، يرجى إدخال أربعة أعراض أو أكثر."),
                        actions=[
                            ft.TextButton("حسناً", on_click=lambda _: self.page.close_dialog()),
                        ],
                    )
                )
                return  # لا تكمل التشخيص


            predicted_disease = get_predicted_value(self.selected_symptoms)
            description, precautions, medications, diet, workout, tests = helper(predicted_disease)

            self.page.results_data = {
                "disease": predicted_disease,
                "description": description,
                "symptoms": self.selected_symptoms,
                "precautions": precautions,
                "medications": medications,
                "diet": diet,
                "workout": workout,
                "tests": tests,
            }

            self.page.go("/results")
            self.error_message.value = ""
            self.selected_symptoms = []
            self.selected_symptoms_display.value = ""
            self.page.update()


        except Exception as e:
            print(f"Error: {str(e)}")
            # استخدام نافذة منبثقة لعرض رسالة الخطأ أيضًا
            self.page.show_dialog(
                ft.AlertDialog(
                    modal=True,
                    title=ft.Text("حدث خطأ"),
                    content=ft.Text(f"حدث خطأ غير متوقع: {str(e)}"),
                    actions=[
                        ft.TextButton("حسناً", on_click=lambda _: self.page.close_dialog()),
                    ],
                )
            )
            self.update()
class Home2(ft.View):
    def __init__(self):
        super().__init__(
            route="/home2",
            padding=ft.padding.only(left=0, right=0, bottom=0, top=0),
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            bgcolor="#E6F3F3"
        )
        self.bottom_appbar = BottomAppBar(page=self.page)  # Pass the page instance

        self.__header = ft.Container(
            content=ft.Row(
                controls=[
                    ft.IconButton(
                        icon=ft.icons.ARROW_BACK,
                        icon_color="#000000",
                        on_click=lambda e: e.page.go("/Splash")  # Or any appropriate previous route
                    ),
                    ft.Container(
                        content=ft.Image(
                            src="assets/ai.jpg",
                            width=50,
                            height=50,
                        ),
                        expand=True,
                        alignment=ft.alignment.center,
                    ),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
            bgcolor="#87CEEB",
        )

        self.__title = ft.Text(
            value="اختر الأعراض التي تعاني منها",
            color=ft.colors.BLACK,
            size=22,
            font_family="Poppins",
            weight=ft.FontWeight.BOLD,
            text_align=ft.TextAlign.CENTER
        )

        self.symptom_checkboxes = []
        arabic_symptoms = [k for k in symptoms_dict if isinstance(k, str) and not k.isascii()]

        symptom_controls = []
        for symptom in arabic_symptoms:
            checkbox = ft.Checkbox(label=symptom, value=False, label_position=ft.LabelPosition.LEFT)
            self.symptom_checkboxes.append(checkbox)

            symptom_container = ft.Container(
                content=checkbox,
                border=ft.border.all(1, ft.colors.GREY_400),
                border_radius=ft.border_radius.all(8),
                padding=ft.padding.all(10),
                alignment=ft.alignment.center_right,
                width=280,
            )
            symptom_controls.append(symptom_container)

        self.selected_symptoms_display = ft.Text("", text_align=ft.TextAlign.RIGHT)

        self.__submit_button = ft.ElevatedButton(
            text="تشخيص",
            style=ft.ButtonStyle(
                bgcolor="#87CEEB",
                color="black",
                shape=ft.RoundedRectangleBorder(radius=30),
            ),
            on_click=self.predict_disease,
            width=300,
            height=60
        )
        self.error_message = ft.Text("", color=ft.colors.RED)

        self.scrollable_symptoms = ft.Column(
            scroll=ft.ScrollMode.ALWAYS,
            controls=symptom_controls,
            height=300,
            horizontal_alignment=ft.CrossAxisAlignment.END,
            spacing=10,
        )

        self.__content = ft.Container(
            content=ft.Column(
                controls=[
                    self.__title,
                    self.scrollable_symptoms,
                    self.selected_symptoms_display,
                    self.__submit_button,
                    self.error_message

                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=15,
            ),
            padding=10,
            margin=ft.margin.only(top=20),
        )

        self.controls = [self.__header, self.__content, self.bottom_appbar]


    def predict_disease(self, e):
        try:
            self.selected_symptoms = [
                cb.label for cb in self.symptom_checkboxes if cb.value
            ]

            if len(self.selected_symptoms) < 4:  # Check for at least 4 symptoms
                self.page.show_dialog(
                    ft.AlertDialog(
                        modal=True,
                        title=ft.Text("عدد الأعراض غير كافٍ"),
                        content=ft.Text("للحصول على نتائج أكثر دقة، يرجى اختيار أربعة أعراض أو أكثر."),
                        actions=[
                            ft.TextButton("حسناً", on_click=lambda _: self.page.close_dialog()),
                        ],
                    )
                )
                return  # Stop execution if fewer than 4 symptoms

            predicted_disease = get_predicted_value(self.selected_symptoms)
            description, precautions, medications, diet, workout, tests = helper(predicted_disease)

            self.page.results_data = {
                "disease": predicted_disease,
                "description": description,
                "symptoms": self.selected_symptoms,
                "precautions": precautions,
                "medications": medications,
                "diet": diet,
                "workout": workout,
                "tests": tests,
            }
            self.page.go("/results")  # Move go() before update()
            self.error_message.value = ""

            for cb in self.symptom_checkboxes:
                cb.value = False
            self.selected_symptoms_display.value = ""
            self.page.update() # update after go() and resetting


        except Exception as e:
            print(f"Error: {str(e)}")
            self.page.show_dialog(    # Show error in a dialog
                ft.AlertDialog(
                    modal=True,
                    title=ft.Text("حدث خطأ"),
                    content=ft.Text(f"حدث خطأ: {str(e)}"),
                    actions=[
                        ft.TextButton("OK", on_click=lambda x: self.page.close_dialog())
                    ]
                )
            )
            self.update()


def main(page: ft.Page):
    page.window.width = 360
    page.window.height = 750
    page.window.top = 0.5
    page.window.left = 898
    page.window.resizable = False

    def route_change(route):
        print(f"Route changing to: {route}")
        page.views.clear()
        try:
            if page.route == "/home" or page.route == "/":
                page.views.append(Home())
            elif page.route == "/results":
                if hasattr(page, 'results_data'):
                    results_view = ResultsView(page.results_data)
                    page.views.append(results_view)
                else:
                    print("No results data found")
                    page.go("/home")

            page.update()
        except Exception as e:
            print(f"Error in route_change: {str(e)}")

    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    # تسجيل معالجات التوجيه
    page.on_route_change = route_change
    page.on_view_pop = view_pop

    page.go(page.route)

if __name__ == "__main__":

    ft.app(target=main)






# def generate_pdf(e):
#     try:
#         from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
#         from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
#         from reportlab.lib.enums import TA_RIGHT
#         from reportlab.lib.pagesizes import letter
#         from reportlab.pdfbase import pdfmetrics
#         from reportlab.pdfbase.ttfonts import TTFont
#         import os
#         from datetime import datetime
        
#         # تسجيل الخط العربي
#         # تأكد من وجود ملف الخط في المسار الصحيح
#         pdfmetrics.registerFont(TTFont('Arabic', 'path/to/arabic-font.ttf'))  # استبدل بمسار الخط العربي لديك
        
#         documents_path = os.path.expanduser('~/Documents')
#         timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
#         pdf_path = os.path.join(documents_path, f'medical_report_{timestamp}.pdf')

#         doc = SimpleDocTemplate(
#             pdf_path,
#             pagesize=letter,
#             rightMargin=72,
#             leftMargin=72,
#             topMargin=72,
#             bottomMargin=72
#         )

#         styles = getSampleStyleSheet()
#         arabic_style = ParagraphStyle(
#             'Arabic',
#             fontName='Arabic',  # استخدام الخط العربي المسجل
#             fontSize=14,
#             leading=16,
#             alignment=TA_RIGHT,  # محاذاة النص إلى اليمين
#             rtl=True  # تفعيل الكتابة من اليمين إلى اليسار
#         )
        
#         title_style = ParagraphStyle(
#             'ArabicTitle',
#             fontName='Arabic',  # استخدام الخط العربي المسجل
#             fontSize=18,
#             leading=22,
#             alignment=TA_RIGHT,
#             rtl=True
#         )

#         content = []
        
#         # إضافة العنوان
#         title_text = "تقرير التشخيص الطبي"
#         content.append(Paragraph(title_text, title_style))
#         content.append(Spacer(1, 20))

#         # إضافة المحتوى
#         def add_section(title, text):
#             content.append(Paragraph(f"{title}: {text}", arabic_style))
#             content.append(Spacer(1, 12))

#         add_section("المرض المتوقع", self.results_data['disease'])
#         add_section("الوصف", self.results_data['description'])
#         add_section("الأعراض", '، '.join(self.results_data['symptoms']))
#         add_section("الاحتياطات", '، '.join(self.results_data['precautions']))
#         add_section("الأدوية", '، '.join(self.results_data['medications']))
#         add_section("النظام الغذائي", '، '.join(self.results_data['diet']))
#         add_section("التمارين", '، '.join(self.results_data['workout']))
        
#         # إضافة التاريخ
#         date_text = f"تاريخ التقرير: {datetime.now().strftime('%Y-%m-%d %H:%M')}"
#         content.append(Spacer(1, 20))
#         content.append(Paragraph(date_text, arabic_style))

#         doc.build(content)

#         self.page.show_snack_bar(
#             ft.SnackBar(
#                 content=ft.Text(f"تم حفظ التقرير في المستندات: medical_report_{timestamp}.pdf"),
#                 action="حسناً"
#             )
#         )

#     except Exception as e:
#         print(f"Error generating PDF: {str(e)}")
#         self.page.show_snack_bar(
#             ft.SnackBar(
#                 content=ft.Text(f"حدث خطأ أثناء إنشاء التقرير: {str(e)}"),
#                 action="حسناً"
#             )
#         )

















