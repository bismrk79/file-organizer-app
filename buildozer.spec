[app]

# (str) Title of your application
title = 파일정리기

# (str) Package name
package.name = fileorganizer

# (str) Package domain (needed for android/ios packaging)
package.domain = com.yourname.fileorganizer

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas

# (str) Application versioning (method 1)
version = 1.0

# (list) Application requirements
requirements = python3,kivy,android

# (str) Supported orientation (portrait, landscape, all)
orientation = portrait

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = False, 1 = True)
warn_on_root = 1

[android]

# (str) Android SDK version to use
android.sdk = 30

# (str) Android NDK version to use
android.ndk = 23b

# (list) Android app permissions
android.permissions = WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE, MANAGE_EXTERNAL_STORAGE

# (str) Android package name
android.package = com.yourname.fileorganizer

# (str) Android app theme
android.theme = @android:style/Theme.NoTitleBar

# (str) Android orientation
android.orientation = portrait

[ios]

# (str) Path to a custom kivy-ios folder
#ios.kivy_ios_dir = ../kivy-ios
# Alternately, specify the URL and branch of a git checkout:
ios.kivy_ios_url = https://github.com/kivy/kivy-ios
ios.kivy_ios_branch = master

# (bool) Whether or not to sign the code
ios.codesign.allowed = false