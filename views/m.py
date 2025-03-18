
import flet as ft
import numpy as np
import pandas as pd
import pickle
from fuzzywuzzy import process
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate
import sys
import os
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import arabic_reshaper
from bidi.algorithm import get_display
from datetime import datetime
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

from arabic_paragraph import ArabicParagraph 
sym_des = pd.read_csv("symtoms_df.csv")
precautions = pd.read_csv("p.csv")
workout = pd.read_csv("w.csv")
description = pd.read_csv("des.csv")
medications = pd.read_csv('med.csv')
diets = pd.read_csv("d.csv")

# Load the trained model (make sure svc.pkl exists)
svc = pickle.load(open('svc.pkl', 'rb'))


def helper(dis):
    desc = description[description['Disease'] == dis]['Description'].iloc[0]
    pre = [str(p) for p in precautions[precautions['Disease'] == dis][
        ['Precaution_1', 'Precaution_2', 'Precaution_3', 'Precaution_4']].values.tolist()[0]]
    med = [str(m) for m in medications[medications['Disease'] == dis]['Medication'].values.tolist()]
    die = [str(d) for d in diets[diets['Disease'] == dis]['Diet'].values.tolist()]
    wrkout = [str(w) for w in workout[workout['disease'] == dis]['workout'].values.tolist()]
    return desc, pre, med, die, wrkout
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
            # Iterate through symptoms_dict to find the correct index
            for key, value in symptoms_dict.items():
                if item == key:
                    input_vector[value] = 1
                    break  # Important: Stop searching once found


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
                    on_click=lambda _: self.page.go("/home")
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
                    self.__icon(ft.icons.HOME, True, "/"),  # Home icon, selected by default, routes to "/"
                    self.__icon(ft.icons.MEDICAL_SERVICES, False, "/doctors"),  # Doctors icon, routes to "/doctors"
                    self.__icon(ft.icons.SETTINGS, False), #Settings
                    self.__icon(ft.icons.PERSON, False), #Profile
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

import flet as ft
import copy  # Import the copy module

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
        self.current_edit_index = None  # Track which doctor is being edited

        # TextFields for adding/editing
        self.name_field = ft.TextField(label="اسم الطبيب", text_align=ft.TextAlign.RIGHT)
        self.phone_field = ft.TextField(label="رقم الهاتف", text_align=ft.TextAlign.RIGHT)
        self.specialty_field = ft.TextField(label="التخصص", text_align=ft.TextAlign.RIGHT)

    def build(self):
        self.update_list()  # Initial list build
        return ft.Column(
            controls=[
                ft.Container(
                    content=ft.Text("الأطباء", size=24, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER),
                    alignment=ft.alignment.top_center,
                    padding=ft.padding.only(top=10, bottom=5)
                ),
                self.doctors_list,
                ft.Divider(),
                ft.Column(
                  [
                    self.name_field,
                    self.phone_field,
                    self.specialty_field,
                    ft.Row(
                        [
                            ft.ElevatedButton("إضافة طبيب", on_click=self.add_doctor),
                            ft.ElevatedButton("حفظ التعديلات", on_click=self.save_edit, visible=False), # Initially hidden
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,

                    )

                  ],
                    visible=True # Keep the add/edit controls visible
                )
            ],
            expand=True
        )

    def update_list(self):
      """Refreshes the doctor list view."""
      self.doctors_list.controls.clear()
      for i, doctor in enumerate(self.doctors_data):
          self.doctors_list.controls.append(
              ft.Container(
                  content=ft.Column(
                      [
                          ft.Text(doctor["name"], size=18, weight=ft.FontWeight.BOLD),
                          ft.Text(doctor["specialty"], size=14, color=ft.colors.GREY_500),
                          ft.Row(
                              [
                                  ft.Icon(ft.icons.PHONE),
                                  ft.Text(doctor["phone"], size=14),
                              ],
                              alignment=ft.MainAxisAlignment.START
                          ),
                          ft.Row( # Edit and Delete Buttons
                              [
                                  ft.IconButton(ft.icons.EDIT, on_click=lambda e, index=i: self.edit_doctor(index)),
                                  ft.IconButton(ft.icons.DELETE, on_click=lambda e, index=i: self.delete_doctor(index)),
                              ],
                              alignment=ft.MainAxisAlignment.END
                          )
                      ]
                  ),
                  bgcolor=ft.colors.WHITE,
                  border=ft.border.all(1, ft.colors.GREY_300),
                  border_radius=ft.border_radius.all(10),
                  padding=15,
                  shadow=ft.BoxShadow(
                      spread_radius=1,
                      blur_radius=5,
                      color=ft.colors.GREY_400,
                      offset=ft.Offset(0, 2),
                  )
              )
          )
      self.update()


    def add_doctor(self, e):
        """Adds a new doctor to the list."""
        if all([self.name_field.value, self.phone_field.value, self.specialty_field.value]):
          self.doctors_data.append({
              "name": self.name_field.value,
              "phone": self.phone_field.value,
              "specialty": self.specialty_field.value,
          })
          self.name_field.value = ""
          self.phone_field.value = ""
          self.specialty_field.value = ""
          self.update_list()
        else:
          # Show error if fields are empty.  Better UX
          self.page.show_dialog(
              ft.AlertDialog(
                modal=True,
                title=ft.Text("خطأ"),
                content=ft.Text("يرجى ملء جميع الحقول"),
                actions=[ft.TextButton("حسنا", on_click=lambda _: self.page.close_dialog())]
              )
          )

    def edit_doctor(self, index):
        """Prepares the UI for editing a doctor."""
        doctor = self.doctors_data[index]
        self.current_edit_index = index
        self.name_field.value = doctor["name"]
        self.phone_field.value = doctor["phone"]
        self.specialty_field.value = doctor["specialty"]
        # Show the "Save Edit" button, hide the "Add" button.
        self.controls[2].controls[3].controls[0].visible = False #add button
        self.controls[2].controls[3].controls[1].visible = True  #save button
        self.update()


    def save_edit(self, e):
        """Saves the changes made to a doctor's information."""
        if self.current_edit_index is not None:
            if all([self.name_field.value, self.phone_field.value, self.specialty_field.value]):
              self.doctors_data[self.current_edit_index] = {
                  "name": self.name_field.value,
                  "phone": self.phone_field.value,
                  "specialty": self.specialty_field.value,
              }
              self.current_edit_index = None  # Reset edit index
              self.name_field.value = ""
              self.phone_field.value = ""
              self.specialty_field.value = ""
              # Show Add button, hide Save button.
              self.controls[2].controls[3].controls[0].visible = True  # Add button
              self.controls[2].controls[3].controls[1].visible = False # Save button

              self.update_list()
            else:
               # Show error if fields are empty.  Better UX
               self.page.show_dialog(
                   ft.AlertDialog(
                       modal=True,
                       title=ft.Text("خطأ"),
                       content=ft.Text("يرجى ملء جميع الحقول"),
                       actions=[ft.TextButton("حسنا", on_click=lambda _: self.page.close_dialog())]
                    )
                )



    def delete_doctor(self, index):
        """Deletes a doctor from the list."""
        del self.doctors_data[index]
        self.update_list()

# Example of how to use it in your main app:





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
                        on_click=lambda e: e.page.go("/")
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
            visible=False,  # Hidden by default
            on_change=self.add_selected_symptom,
            width=300,
        )

        self.__search = ft.TextField(
            width=300,
            height=60,  # Single line for input
            border_radius=10,
            bgcolor="white",
            border_color="#A0B4C7",
            hint_text="ابحث عن عرض...",
            text_align=ft.TextAlign.RIGHT,
            on_change=self.update_suggestions,  # Call update_suggestions on text change
        )

        self.__submit_button = ft.ElevatedButton(
            text="تقديم الاعراض",
            style=ft.ButtonStyle(
                bgcolor="#87CEEB",
                color="black",
                shape=ft.RoundedRectangleBorder(radius=30),
            ),
            on_click=self.predict_disease,  # predict_disease function
            width=300,
            height=60
        )
        self.error_message = ft.Text("", color=ft.colors.RED)

        self.__content = ft.Container(
            content=ft.Column(
                controls=[
                    self.__title,
                    self.__search,
                    self.suggestions_dropdown,  # Add the dropdown to the layout
                    self.selected_symptoms_display,  # Display selected symptoms
                    self.__submit_button,
                    self.error_message

                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=15,
            ),
            padding=10,
            margin=ft.margin.only(top=20),
        )

        self.controls = [self.__header, self.__content,self.bottom_appbar ]

    def update_suggestions(self, e):
        """Provides suggestions based on user input."""
        user_input = self.__search.value
        if user_input:
            suggestions = suggest_symptoms(user_input)
            self.suggestions_dropdown.options = [
                ft.dropdown.Option(text=s) for s in suggestions
            ]
            self.suggestions_dropdown.visible = True  # Show the dropdown
        else:
            self.suggestions_dropdown.visible = False  # Hide if no input
            self.suggestions_dropdown.options = []
        self.update()

    def add_selected_symptom(self, e):
        """Adds the selected symptom to the list and updates the display."""
        selected = self.suggestions_dropdown.value
        if selected and selected not in self.selected_symptoms:
            self.selected_symptoms.append(selected)
        self.selected_symptoms_display.value = ", ".join(
            self.selected_symptoms)  # Show as comma-separated string
        self.__search.value = ""  # Clear the search field
        self.suggestions_dropdown.visible = False  # Hide dropdown
        self.suggestions_dropdown.value = None  # Reset selected value
        self.update()

    def predict_disease(self, e):
        try:
            if not self.selected_symptoms:
                self.error_message.value = "الرجاء إدخال عرض واحد على الأقل."
                self.update()
                return

            predicted_disease = get_predicted_value(self.selected_symptoms)
            description, precautions, medications, diet, workout = helper(predicted_disease)

            self.page.results_data = {
                "disease": predicted_disease,


                "description": description,
                "symptoms": self.selected_symptoms,
                "precautions": precautions,
                "medications": medications,
                "diet": diet,
                "workout": workout
            }

            self.page.update()
            self.page.go("/results")
            self.error_message.value = ""  # Clear error on success.
            self.selected_symptoms = []  # reset
            self.selected_symptoms_display.value = ""


        except Exception as e:
            print(f"Error: {str(e)}")
            self.error_message.value = f"حدث خطأ: {str(e)}"
            self.update()
class Home2(ft.View):
    def __init__(self):
        super().__init__(
            route="/home2",
            padding=ft.padding.only(left=0, right=0, bottom=0, top=0),
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,  # Vertically center
            bgcolor="#E6F3F3"
        )
        self.bottom_appbar = BottomAppBar()

        self.__header = ft.Container(
            content=ft.Row(
                controls=[
                    ft.IconButton(
                        icon=ft.icons.ARROW_BACK,
                        icon_color="#000000",
                        on_click=lambda e: e.page.go("/")
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

        # Create a list of symptom containers.  This is the KEY change.
        symptom_controls = []
        for symptom in arabic_symptoms:
            checkbox = ft.Checkbox(label=symptom, value=False, label_position=ft.LabelPosition.LEFT)
            self.symptom_checkboxes.append(checkbox)  # Keep track of ALL checkboxes

            symptom_container = ft.Container(
                content=checkbox,
                border=ft.border.all(1, ft.colors.GREY_400),  # Add a border
                border_radius=ft.border_radius.all(8),      # Rounded corners
                padding=ft.padding.all(10),                 # Padding inside the container
                alignment=ft.alignment.center_right,        # Align content to the right
                width=280,                               # Consistent width
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

        # Use a Column for the scrollable symptoms, with explicit alignment
        self.scrollable_symptoms = ft.Column(
            scroll=ft.ScrollMode.ALWAYS,
            controls=symptom_controls,  # Use the list of CONTAINERS
            height=300,
            horizontal_alignment=ft.CrossAxisAlignment.END, # Right-align the *Column*
            spacing=10, # Add spacing BETWEEN the containers.
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

            if not self.selected_symptoms:
                self.error_message.value = "الرجاء اختيار عرض واحد على الأقل."
                self.update()
                return

            predicted_disease = get_predicted_value(self.selected_symptoms)
            description, precautions, medications, diet, workout = helper(predicted_disease)

            self.page.results_data = {
                "disease": predicted_disease,
                "description": description,
                "symptoms": self.selected_symptoms,
                "precautions": precautions,
                "medications": medications,
                "diet": diet,
                "workout": workout
            }

            self.page.update()
            self.page.go("/results")
            self.error_message.value = ""

            for cb in self.symptom_checkboxes:
                cb.value = False
            self.selected_symptoms_display.value = ""
            self.update()

        except Exception as e:
            print(f"Error: {str(e)}")
            self.error_message.value = f"حدث خطأ: {str(e)}"  # Display error in the UI
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

















