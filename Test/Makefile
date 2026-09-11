TARGET := iphone:clang:latest:12.4
# TARGET := simulator:clang:latest:12.4
INSTALL_TARGET_PROCESSES = SpringBoard

# TEST_USE_SUBSTRATE = 0

include $(THEOS)/makefiles/common.mk

TWEAK_NAME = Test

Test_FILES = Tweak.x
Test_CFLAGS = -fobjc-arc

include $(THEOS_MAKE_PATH)/tweak.mk
