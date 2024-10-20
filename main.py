from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.list import OneLineIconListItem, MDList
from kivymd.uix.button import MDFloatingActionButton, MDIconButton
from kivymd.uix.card import MDCard
from kivy.uix.image import Image

KV = '''
Screen:
    MDBoxLayout:
        orientation: 'vertical'

        # Profile Section
        MDBoxLayout:
            orientation: 'vertical'
            size_hint_y: 0.4
            padding: dp(20)
            spacing: dp(20)
            md_bg_color: [1, 0.9, 0.8, 1]  # Background color similar to the design

            MDBoxLayout:
                size_hint_y: None
                height: dp(100)
                spacing: dp(10)
                pos_hint: {"center_x": 0.5}

                # Profile Image
                Image:
                    source: 'profile_picture.png'  # Use a placeholder image or your own
                    size_hint: None, None
                    size: dp(100), dp(100)
                    allow_stretch: True
                    keep_ratio: True
                    radius: [dp(50),]  # Circular shape

            MDLabel:
                text: "Monica Gamage"
                halign: "center"
                font_style: "H6"

            MDLabel:
                text: "@monicagamage"
                halign: "center"
                font_style: "Subtitle2"

            MDRaisedButton:
                text: "Log Out"
                pos_hint: {"center_x": 0.5}
                md_bg_color: [1, 0.7, 0.5, 1]  # Button color

        # Clock and Greeting Section
        MDBoxLayout:
            orientation: 'vertical'
            padding: dp(10)
            spacing: dp(10)
            size_hint_y: None
            height: dp(200)
            MDLabel:
                text: "Good Afternoon"
                halign: "center"
                font_style: "H5"

            # Placeholder for Clock Image or Widget
            Image:
                source: 'clock.png'  # Placeholder clock image

        # Task List Section
        MDBoxLayout:
            orientation: 'vertical'
            padding: dp(10)
            spacing: dp(10)
            size_hint_y: 0.4

            MDLabel:
                text: "Tasks List"
                font_style: "H6"
                halign: "center"

            # Card containing tasks
            MDCard:
                orientation: 'vertical'
                padding: dp(10)
                size_hint: None, None
                size: dp(300), dp(300)
                elevation: 10
                radius: [dp(20),]

                ScrollView:
                    MDList:
                        id: task_list
                        OneLineIconListItem:
                            text: "Cook Rice and Chicken at 10 am"
                            IconLeftWidget:
                                icon: "checkbox-blank-circle-outline"

                        OneLineIconListItem:
                            text: "Learn ReactJS at 12 pm"
                            IconLeftWidget:
                                icon: "checkbox-blank-circle-outline"

                        OneLineIconListItem:
                            text: "Have Lunch at 1 pm"
                            IconLeftWidget:
                                icon: "checkbox-blank-circle-outline"

                        OneLineIconListItem:
                            text: "Learn HTML and CSS at 3 pm"
                            IconLeftWidget:
                                icon: "checkbox-blank-circle-outline"

                        OneLineIconListItem:
                            text: "Have Dinner at 8 pm"
                            IconLeftWidget:
                                icon: "checkbox-blank-circle-outline"

            MDFloatingActionButton:
                icon: "plus"
                pos_hint: {"center_x": 0.9, "center_y": 0.5}
'''

class TaskApp(MDApp):
    def build(self):
        return Builder.load_string(KV)

if _name_ == "_main_":
    TaskApp().run()
