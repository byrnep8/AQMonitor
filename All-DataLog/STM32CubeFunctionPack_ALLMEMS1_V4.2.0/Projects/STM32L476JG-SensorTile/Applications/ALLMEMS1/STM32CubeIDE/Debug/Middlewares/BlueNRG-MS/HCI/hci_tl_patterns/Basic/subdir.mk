################################################################################
# Automatically-generated file. Do not edit!
# Toolchain: GNU Tools for STM32 (10.3-2021.10)
################################################################################

# Add inputs and outputs from these tool invocations to the build variables 
C_SRCS += \
C:/Users/Patrick/Documents/DCU/Masters\ Project/masters_project/All-DataLog/STM32CubeFunctionPack_ALLMEMS1_V4.2.0/Middlewares/ST/BlueNRG-MS/hci/hci_tl_patterns/Basic/hci_tl.c 

C_DEPS += \
./Middlewares/BlueNRG-MS/HCI/hci_tl_patterns/Basic/hci_tl.d 

OBJS += \
./Middlewares/BlueNRG-MS/HCI/hci_tl_patterns/Basic/hci_tl.o 


# Each subdirectory must supply rules for building sources it contributes
Middlewares/BlueNRG-MS/HCI/hci_tl_patterns/Basic/hci_tl.o: C:/Users/Patrick/Documents/DCU/Masters\ Project/masters_project/All-DataLog/STM32CubeFunctionPack_ALLMEMS1_V4.2.0/Middlewares/ST/BlueNRG-MS/hci/hci_tl_patterns/Basic/hci_tl.c Middlewares/BlueNRG-MS/HCI/hci_tl_patterns/Basic/subdir.mk
	arm-none-eabi-gcc "$<" -mcpu=cortex-m4 -std=c99 -g3 -DDEBUG -DUSE_HAL_DRIVER -DSTM32L476xx -DUSE_STM32L4XX_NUCLEO -DSTM32_SENSORTILE -c -I../../Inc -I../../Inc/FatFS_Template -I../../../../../../Drivers/CMSIS/Device/ST/STM32L4xx/Include -I../../../../../../Drivers/STM32L4xx_HAL_Driver/Inc -I../../../../../../Drivers/BSP/SensorTile -I../../../../../../Drivers/CMSIS/Include -I../../../../../../Drivers/BSP/Components/Common -I../../../../../../Drivers/BSP/Components/lsm6dsm -I../../../../../../Drivers/BSP/Components/hts221 -I../../../../../../Drivers/BSP/Components/lps22hb -I../../../../../../Drivers/BSP/Components/lsm303agr -I../../../../../../Drivers/BSP/Components/pcm1774 -I../../../../../../Drivers/BSP/Components/stc3115 -I../../../../../../Middlewares/ST/BlueNRG-MS/includes -I../../../../../../Middlewares/ST/BlueNRG-MS/utils -I../../../../../../Middlewares/ST/BlueNRG-MS/hci/hci_tl_patterns/Basic -I../../../../../../Middlewares/Third_Party/FatFs/src -I../../../../../../Middlewares/Third_Party/FatFs/src/drivers -I../../../../../../Middlewares/ST/STM32_MetaDataManager -I../../../../../../Middlewares/ST/STM32_BlueVoiceADPCM_Library/Inc -I../../../../../../Middlewares/ST/STM32_MotionAR_Library/Inc -I../../../../../../Middlewares/ST/STM32_MotionCP_Library/Inc -I../../../../../../Middlewares/ST/STM32_MotionFA_Library/Inc -I../../../../../../Middlewares/ST/STM32_MotionFX_Library/Inc -I../../../../../../Middlewares/ST/STM32_MotionGR_Library/Inc -I../../../../../../Middlewares/ST/STM32_MotionID_Library/Inc -I../../../../../../Middlewares/ST/STM32_MotionPE_Library/Inc -I../../../../../../Middlewares/ST/STM32_MotionSD_Library/Inc -I../../../../../../Middlewares/ST/STM32_MotionTL_Library/Inc -I../../../../../../Middlewares/ST/STM32_MotionVC_Library/Inc -I../../../../../../Middlewares/ST/STM32_USB_Device_Library/Class/CDC/Inc -I../../../../../../Middlewares/ST/STM32_USB_Device_Library/Core/Inc -I"C:/Users/Patrick/Documents/DCU/Masters Project/All-DataLog/STM32CubeFunctionPack_ALLMEMS1_V4.2.0/Projects/STM32L476JG-SensorTile/Applications/ALLMEMS1/Inc" -I"C:/Users/Patrick/Documents/DCU/Masters Project/ds3231" -I"C:/Users/Patrick/STM32CubeIDE/workspace_all_data/i2c_prototype/Core/Src/SPS30_Git" -I"C:/Users/Patrick/Documents/DCU/Masters Project/masters_project/i2c_prototype/Core/Src/SPS30_Git" -I"C:/Users/Patrick/Documents/DCU/Masters Project/masters_project/MICS4514_Git" -I"C:/Users/PByrne/Documents/GitHub/masters_project/i2c_prototype/Core/Src/SPS30_Git" -I"C:/Users/PByrne/Documents/GitHub/masters_project/i2c_prototype/Core/Src/MiCS4154" -Og -ffunction-sections -Wall -fstack-usage -fcyclomatic-complexity -MMD -MP -MF"Middlewares/BlueNRG-MS/HCI/hci_tl_patterns/Basic/hci_tl.d" -MT"$@" --specs=nano.specs -mfpu=fpv4-sp-d16 -mfloat-abi=softfp -mthumb -o "$@"

clean: clean-Middlewares-2f-BlueNRG-2d-MS-2f-HCI-2f-hci_tl_patterns-2f-Basic

clean-Middlewares-2f-BlueNRG-2d-MS-2f-HCI-2f-hci_tl_patterns-2f-Basic:
	-$(RM) ./Middlewares/BlueNRG-MS/HCI/hci_tl_patterns/Basic/hci_tl.cyclo ./Middlewares/BlueNRG-MS/HCI/hci_tl_patterns/Basic/hci_tl.d ./Middlewares/BlueNRG-MS/HCI/hci_tl_patterns/Basic/hci_tl.o ./Middlewares/BlueNRG-MS/HCI/hci_tl_patterns/Basic/hci_tl.su

.PHONY: clean-Middlewares-2f-BlueNRG-2d-MS-2f-HCI-2f-hci_tl_patterns-2f-Basic

