from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.uix.filechooser import FileChooserIconView
from kivy.clock import Clock
from kivy.utils import platform

import os
import re
import shutil
from datetime import datetime
from pathlib import Path

class FileOrganizerApp(App):
    def __init__(self):
        super().__init__()
        self.selected_path = None
        self.log_text = ""
        self.processed_files = []
        
    def build(self):
        self.title = "파일 정리기"
        
        # 메인 레이아웃
        main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # 상단 제목
        title_label = Label(
            text='파일 정리기\n(abc-123.확장자 패턴)',
            size_hint_y=None,
            height=80,
            text_size=(None, None),
            halign='center',
            font_size=18,
            bold=True
        )
        main_layout.add_widget(title_label)
        
        # 경로 선택 영역
        path_layout = BoxLayout(size_hint_y=None, height=50, spacing=5)
        
        self.path_input = TextInput(
            text=self.get_default_path(),
            multiline=False,
            size_hint_x=0.7,
            hint_text='작업할 폴더 경로'
        )
        
        browse_btn = Button(
            text='폴더 선택',
            size_hint_x=0.3
        )
        browse_btn.bind(on_press=self.open_file_chooser)
        
        path_layout.add_widget(self.path_input)
        path_layout.add_widget(browse_btn)
        main_layout.add_widget(path_layout)
        
        # 버튼 영역
        button_layout = BoxLayout(size_hint_y=None, height=50, spacing=10)
        
        # 미리보기 버튼
        preview_btn = Button(text='미리보기', background_color=(0.2, 0.6, 1, 1))
        preview_btn.bind(on_press=self.preview_files)
        
        # 실행 버튼
        process_btn = Button(text='파일 정리 실행', background_color=(0.2, 0.8, 0.2, 1))
        process_btn.bind(on_press=self.process_files)
        
        # 로그 지우기 버튼
        clear_btn = Button(text='로그 지우기', background_color=(0.8, 0.8, 0.2, 1))
        clear_btn.bind(on_press=self.clear_log)
        
        button_layout.add_widget(preview_btn)
        button_layout.add_widget(process_btn)
        button_layout.add_widget(clear_btn)
        main_layout.add_widget(button_layout)
        
        # 로그 영역
        log_label = Label(
            text='로그:',
            size_hint_y=None,
            height=30,
            text_size=(None, None),
            halign='left'
        )
        main_layout.add_widget(log_label)
        
        # 스크롤 가능한 로그 영역
        scroll = ScrollView()
        self.log_display = Label(
            text='앱이 시작되었습니다.\n폴더를 선택하고 미리보기 또는 실행을 눌러주세요.',
            text_size=(None, None),
            halign='left',
            valign='top',
            markup=True
        )
        scroll.add_widget(self.log_display)
        main_layout.add_widget(scroll)
        
        return main_layout
    
    def get_default_path(self):
        """기본 작업 경로 설정"""
        if platform == 'android':
            from android.permissions import request_permissions, Permission
            request_permissions([
                Permission.READ_EXTERNAL_STORAGE,
                Permission.WRITE_EXTERNAL_STORAGE
            ])
            # 안드로이드 다운로드 폴더
            return '/storage/emulated/0/Download'
        else:
            # 데스크톱의 경우 현재 폴더
            return os.getcwd()
    
    def open_file_chooser(self, instance):
        """폴더 선택 팝업"""
        content = BoxLayout(orientation='vertical')
        
        file_chooser = FileChooserIconView(
            path=self.path_input.text,
            dirselect=True,
            filters=['']
        )
        
        button_layout = BoxLayout(size_hint_y=None, height=50, spacing=10)
        
        select_btn = Button(text='선택')
        cancel_btn = Button(text='취소')
        
        button_layout.add_widget(select_btn)
        button_layout.add_widget(cancel_btn)
        
        content.add_widget(file_chooser)
        content.add_widget(button_layout)
        
        popup = Popup(
            title='폴더 선택',
            content=content,
            size_hint=(0.9, 0.9)
        )
        
        def select_folder(instance):
            if file_chooser.selection:
                self.path_input.text = file_chooser.selection[0]
            popup.dismiss()
        
        def cancel_selection(instance):
            popup.dismiss()
        
        select_btn.bind(on_press=select_folder)
        cancel_btn.bind(on_press=cancel_selection)
        
        popup.open()
    
    def is_valid_pattern(self, filename):
        """파일명 패턴 검증"""
        pattern = r'^([a-zA-Z][a-zA-Z0-9]{1,11})-(\d{2,10}(?:-[a-zA-Z]+)?)$'
        match = re.match(pattern, filename)
        
        if match:
            abc_part = match.group(1)
            num_part = match.group(2)
            
            if 2 <= len(abc_part) <= 12:
                num_base = num_part.split('-')[0]
                if 2 <= len(num_base) <= 10:
                    return abc_part
        return None
    
    def add_log(self, message, color='white'):
        """로그 메시지 추가"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        colored_message = f"[color={color}]{timestamp} - {message}[/color]"
        self.log_text += colored_message + "\n"
        self.log_display.text = self.log_text
        self.log_display.text_size = (self.log_display.parent.width if self.log_display.parent else None, None)
    
    def preview_files(self, instance):
        """파일 미리보기"""
        path = self.path_input.text.strip()
        
        if not os.path.exists(path):
            self.add_log("❌ 경로가 존재하지 않습니다!", "red")
            return
        
        if not os.path.isdir(path):
            self.add_log("❌ 폴더가 아닙니다!", "red")
            return
        
        self.add_log(f"📁 미리보기: {path}", "cyan")
        
        matching_files = []
        non_matching_files = []
        folders_to_create = set()
        
        try:
            for filename in os.listdir(path):
                filepath = os.path.join(path, filename)
                
                if os.path.isfile(filepath):
                    file_base = os.path.splitext(filename)[0]
                    file_ext = os.path.splitext(filename)[1].lower()
                    
                    # 시스템 파일 제외
                    if file_ext in ['.py', '.exe', '.log', '.apk']:
                        continue
                    
                    folder_name = self.is_valid_pattern(file_base)
                    if folder_name:
                        matching_files.append((filename, folder_name))
                        folders_to_create.add(folder_name)
                    else:
                        non_matching_files.append(filename)
        
            # 결과 출력
            self.add_log(f"✅ 매칭된 파일: {len(matching_files)}개", "green")
            for filename, folder in matching_files:
                self.add_log(f"  📄 {filename} → {folder}/", "lightgreen")
            
            self.add_log(f"📁 생성될 폴더: {len(folders_to_create)}개", "yellow")
            for folder in sorted(folders_to_create):
                self.add_log(f"  📁 {folder}", "yellow")
            
            self.add_log(f"❌ 패턴 불일치: {len(non_matching_files)}개", "orange")
            for filename in non_matching_files[:5]:  # 최대 5개만 표시
                self.add_log(f"  ❌ {filename}", "orange")
            if len(non_matching_files) > 5:
                self.add_log(f"  ... 외 {len(non_matching_files)-5}개", "orange")
                
        except Exception as e:
            self.add_log(f"❌ 미리보기 오류: {str(e)}", "red")
    
    def process_files(self, instance):
        """실제 파일 정리 실행"""
        path = self.path_input.text.strip()
        
        if not os.path.exists(path) or not os.path.isdir(path):
            self.add_log("❌ 유효하지 않은 경로입니다!", "red")
            return
        
        self.add_log("🚀 파일 정리 시작...", "cyan")
        
        processed = 0
        moved = 0
        created_folders = set()
        
        try:
            original_dir = os.getcwd()
            os.chdir(path)
            
            for filename in os.listdir('.'):
                if os.path.isfile(filename):
                    file_base = os.path.splitext(filename)[0]
                    file_ext = os.path.splitext(filename)[1].lower()
                    
                    # 시스템 파일 제외
                    if file_ext in ['.py', '.exe', '.log', '.apk']:
                        continue
                    
                    processed += 1
                    folder_name = self.is_valid_pattern(file_base)
                    
                    if folder_name:
                        # 폴더 생성
                        if not os.path.exists(folder_name):
                            os.makedirs(folder_name)
                            created_folders.add(folder_name)
                            self.add_log(f"📁 폴더 생성: {folder_name}", "yellow")
                        
                        # 파일 이동
                        try:
                            shutil.move(filename, os.path.join(folder_name, filename))
                            moved += 1
                            self.add_log(f"✅ 이동: {filename} → {folder_name}/", "green")
                        except Exception as e:
                            self.add_log(f"❌ 이동 실패: {filename} - {str(e)}", "red")
                    else:
                        self.add_log(f"⏭️ 건너뜀: {filename}", "gray")
            
            os.chdir(original_dir)
            
            # 완료 요약
            self.add_log("=" * 30, "white")
            self.add_log("🎉 작업 완료!", "green")
            self.add_log(f"📊 처리된 파일: {processed}개", "white")
            self.add_log(f"📊 이동된 파일: {moved}개", "white")
            self.add_log(f"📊 생성된 폴더: {len(created_folders)}개", "white")
            self.add_log("=" * 30, "white")
            
        except Exception as e:
            self.add_log(f"❌ 처리 중 오류: {str(e)}", "red")
    
    def clear_log(self, instance):
        """로그 지우기"""
        self.log_text = ""
        self.log_display.text = "로그가 지워졌습니다."

if __name__ == '__main__':
    FileOrganizerApp().run()